
import tkinter as tk
from calculate import getInput,parseConfig

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master = master
        
        self.pack()
        self.createWidget()
    
    def createWidget(self):
        self.editor_title = tk.Label(self,text="配置文件编辑区")
        self.editor_title.pack()
        self.editor = tk.Text(self,bg='#E1FFFF')
        self.editor.pack()

        self.output_title = tk.Label(self,text='信息输出区')
        self.output_title.pack()
        self.output = tk.Label(self,bg='#FFFFE0')
        self.output.pack()

        




if __name__ == '__main__':
    root = tk.Tk()
    root.title('图书逾期计算程序')
    root.geometry('800x500')

    app = Application(master=root)

    root.mainloop()