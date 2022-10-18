import tkinter as tk
import datetime
import logging

logging.basicConfig(filename = 'log.txt',level=logging.DEBUG,format='%(levelname)s:%(message)s',encoding='utf8')
# logging.disable(logging.CRITICAL)




class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        
        self.pack()
        self.createWidget()
    
    def createWidget(self):
        tk.Button(self,text='保存配置',font=(5),command=self.saveConfig).grid(row=0,column=0)
        tk.Button(self,text="加载配置",font=(5),command=self.loadConfig).grid(row=0,column=1)
        tk.Button(self,text='加载日志',font=(5),command=self.loadLog).grid(row=0,column=2)
        tk.Button(self,text='帮助信息',font=(5),command=self.loadHelp).grid(row=0,column=3)
        tk.Button(self,text='重置配置文件',font=(5),command=self.resetConfig).grid(row=0,column=4)
        

        self.configFile = tk.StringVar()
        # self.configFile.set(open('config.txt','r',encoding='utf8').read())
        self.editor_title = tk.Label(self,text="配置文件编辑区",font=(10))
        self.editor_title.grid(row=1,column=0,columnspan=5)
        self.editor = tk.Text(self,bg='#E1FFFF')
        self.editor.grid(row=2,column=0,columnspan=5)


        self.output_title = tk.Label(self,text='信息输出区',font=(10))
        self.output_title.grid(row=3,column=0,columnspan=5)
        self.output = tk.Label(self,bg='#FFFFE0',text='请确认配置文件后，输入借书和还书日期，\n再点击“计算”按钮，此处将输出结果！\n\
如果修改了配置，计算前请先点击保存配置！',font=(5))
        self.output.grid(row=4,column=0,columnspan=5)

        self.start_lable = tk.Label(self,text='开始日期是',font=(8)).grid(row=5,column=0)
        self.startDay = tk.StringVar()
        self.start_entry = tk.Entry(self,textvariable=self.startDay)
        self.start_entry.grid(row=5,column=1)
        self.startDay.set(datetime.datetime.strftime(datetime.datetime.today(),'%Y/%m/%d'))

        self.end_lable = tk.Label(self,text='结束日期是',font=(8)).grid(row=5,column=2)
        self.endDay = tk.StringVar()
        self.end_entry = tk.Entry(self,textvariable=self.endDay)
        self.end_entry.grid(row=5,column=3)
        self.endDay.set(datetime.datetime.strftime(datetime.datetime.today(),'%Y/%m/%d'))

        self.start_button = tk.Button(self,text='计算',font='8',command=self.getResult).grid(row=5,column=5)

        # bind shortcuts
        root.bind('<Control-s>',self.saveConfig)
        root.bind('<Control-o>',self.loadConfig)
        root.bind('<Control-l>',self.loadLog)
        root.bind('<Control-r>',self.loadConfig)
        root.bind('<Control-h>',self.loadHelp)


    def saveConfig(self,event=None):
        content = self.editor.get(1.0,tk.END)
        fi = open('config.txt','w',encoding='utf8')
        fi.write(content)
        fi.close()

    def loadConfig(self,event=None):
        self.editor.delete(1.0,tk.END)
        fi = open('config.txt','r',encoding='utf8')
        content = fi.read()
        self.editor.insert(1.0,content)
        fi.close()
    
    def parseConfig(self,path):
        specialDay = [] # 需要手动加入计算的日期
        singleDay = [] # 需要手动排除的日期
        timeRange = [] # 需要手动排除的时间段
        
        fi = open(path,'r',encoding='utf8')
        logging.debug('Start to parase config file')
        for line in fi:
            line = line.strip()
            if len(line) < 7:
                continue

            if line.startswith('#'):
                continue
            elif line == 'include special day:':
                flag = 'special day'
                continue
            elif line == 'single day:':
                flag = 'single day'
                continue
            elif line == 'time range:':
                flag = 'time range'
                continue
            else:
                pass

            if flag == 'special day' :
                line = datetime.datetime.strptime(line,'%Y/%m/%d')
                specialDay.append(line)
            elif flag == 'single day':
                line = datetime.datetime.strptime(line,'%Y/%m/%d')
                singleDay.append(line)
            elif flag == 'time range':
                rangeStart,rangeEnd = tuple(line.split(' - ')) # 将'time range'的开始日期和结束日期分离
                    
                # 解析出datatime对象 
                rangeStart = datetime.datetime.strptime(rangeStart,'%Y/%m/%d')
                rangeEnd = datetime.datetime.strptime(rangeEnd,'%Y/%m/%d')

                # 创建一个时间单位，以便于下面将时间段中的时期加入排除列表中
                unitDay = datetime.timedelta(days=1)
                while rangeStart <= rangeEnd:
                    timeRange.append(rangeStart)
                    rangeStart += unitDay
            else:
                pass
            passDay = timeRange + singleDay

        fi.close()
        logging.debug("Finish to parse config file")
        return specialDay,passDay


    def calculate(self,startDay,endDay,passDay,specialDay):
        logging.debug('Start to Calculate')
        # startDay = datetime.datetime.strptime(startDay,'%Y/%m/%d')
        # endDay = datetime.datetime.strptime(endDay,'%Y/%m/%d')
        totalDays = endDay - startDay

        timeUnit = datetime.timedelta(days=1)
        count = 0
        pointDay = startDay # 当作一个指针
        while pointDay <= endDay:
            if pointDay in passDay:
                logging.debug(f'{pointDay} 在passDay中，排除')
                pointDay += timeUnit
                continue
            elif pointDay in specialDay:
                logging.debug(f'{pointDay} 在special中，计入有效时间')
                count += 1
                pointDay += timeUnit
                continue
            elif (datetime.datetime.weekday(pointDay) == 6):
                # logging.debug(f'周几：{datetime.datetime.weekday(pointDay)}')
                logging.debug(f'{pointDay} 是周日，排除')
                pointDay += timeUnit
                continue
            else:
                logging.debug(f'{pointDay} 是有效借阅时间')
                count += 1
                pointDay += timeUnit
        
        logging.debug('Finish to calculate')
        return count,totalDays
    
    def getResult(self,event=None):
        self.resetLog()
        path = 'config.txt'
        specialDay,passDay = self.parseConfig(path)
        startDay = datetime.datetime.strptime(str(self.startDay.get()),'%Y/%m/%d')
        endDay = datetime.datetime.strptime(str(self.endDay.get()),'%Y/%m/%d')
        count,totalDays = self.calculate(startDay,endDay,passDay,specialDay)
        result = f'''书籍持有时间{totalDays.days}天
有效借阅时间{count}天
逾期{count - 14}天
应缴违约金{0.5*(count - 14)}
        '''
        self.output.config(text=result)

    def loadLog(self,event = None):
        self.editor.delete(1.0,tk.END)
        fi = open('log.txt','r',encoding='utf8')
        content = fi.read()
        self.editor.insert(1.0,content)
        fi.close()
        
    def loadHelp(self,event = None):
        self.editor.delete(1.0,tk.END)
        fi = open('help.txt','r',encoding='utf8')
        content = fi.read()
        self.editor.insert(1.0,content)
        fi.close()

    def resetConfig(self,event=None):
        with open('rawConfig','r',encoding='utf8') as fi:
            with open('config.txt','w',encoding='utf8') as fo:
                fo.write(fi.read())
        self.loadConfig()

    def resetLog(self,event=None):
        with open('log.txt','w',encoding='utf8') as f:
            f.write('')

        


if __name__ == '__main__':
    root = tk.Tk()
    root.title('图书逾期计算程序')
    root.geometry('900x700')

    app = Application(master=root)

    root.mainloop()