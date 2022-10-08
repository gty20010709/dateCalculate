#!/bin/python3
# -*_ coding: utf-8 _*_


README = '''
    这个小程序用来计算违约图书违约的时长
    并自动计算应缴违约金

    程序的使用方法如下：
    1. 首先需要在config中配置需要排除的日期（闭馆日期）
    config 文件中的配置分两个部分
    一是'single day'：即需要跳过的单天，如因为节假日，某个未开馆的周一
    PS：不需要录入周日，周日闭馆，已经自动排除

    二是'time range': 即需要跳过的时间段，如暑假
    至于配置的详细写法，config中有详细的写法
    2. 在使用程序是时候，程序会要求输入借书开始的时期
    和还书的日期

'''


import datetime
import logging
import time

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
logging.disable(logging.CRITICAL)

print(README)

# 控制台输出红色，参见：https://blog.51cto.com/wenyule/2838791


def getInput():
    tips = '''
    开始日期和结束日期的格式如下：
    2022/9/10
    PS: 注意中间的斜杠需要是半角字符（输入法切换到英文状态即可）
    - 如果不输入还书日期，直接回车，默认还书时间是程序运行当天
      但如果运行此程序的电脑，日期有误，还是需要手动输入
    - 如果还书日期手动输入错误，程序会采用当天日期
      但如果电脑本地时间有误，请重新运行程序，并输入正确日期
    '''
    print(tips)
    while True:
        try:
            startTime = datetime.datetime.strptime(input('请输入借书的日期：'),'%Y/%m/%d')
            logging.debug(startTime)
            break
        except:
            print("\033[31m日期格式错误，请重新输入！\033[0m")

    # 如果结束日期不输入的话，默认是当天
    # PS： 如果运行该程序的电脑之日期不正确的话，还需要手动输入
    try:
        endTime = datetime.datetime.strptime(input('请输入还书的日期：'),'%Y/%m/%d')
        logging.debug(endTime)
    except:
        endTime = datetime.datetime.today()
    
    totalDays = endTime - startTime
    logging.debug(totalDays)
    return startTime,endTime,totalDays

def parseConfig() -> list :
    fi = open('config.txt','r',encoding='utf8')

    flag = 0
    specialDay = []
    singleDay = []
    timeRange = []

    for line in fi:
        line = line.strip()
        if len(line) < 7:
            continue

        # 为配置文件中的行标记flag
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
            # 转换str日期对象为datetime对象
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
    return specialDay,singleDay,timeRange




def main():
    logging.debug('Program Start')

    startTime,endTime,totalDays=  getInput()
    specialDay,singleDay,timeRange = parseConfig()

    # calculate the count of days
    count = 0
    unitday = datetime.timedelta(days=1)

    # 下面的遍历会修改 startTime， 
    # 而结果需要使用 startTime， 这里借助一个第三方变量
    startDay = startTime
    # 对从借书到还书中的每一天进行遍历
    while startTime <= endTime:
        # 如果日期在排除列表中，或日期是星期天，则跳过
        if (startTime not in timeRange) and (datetime.datetime.weekday(startTime) != 6): 
            count += 1
        if startTime in specialDay:
            count += 1
        startTime += unitday
    logging.debug('The reuslt is {} day(s).'.format(count))

    if count <= 14:
        print('''
    自图书借出({})至图书归还({}),历时{}
    排除的日期详见配置文件。

    读者借阅图书时间为{}天

    \033[31m图书未逾期！\033[0m
        '''.format(startDay.strftime('%Y/%m%d'),endTime.strftime('%Y/%m%d'),totalDays.days,count))
    elif count > 14:
        fine = (count - 14) * 0.5
        print('''
    自图书借出({})至图书归还({}),历时{}天
    排除的日期详见配置文件。

    读者借阅图书时间为{}天

    \033[31m图书逾期{}天，应缴纳违约金：{}元！\033[0m
        '''.format(startDay.strftime('%Y/%m%d'),endTime.strftime('%Y/%m%d'),totalDays.days,count,count-14,fine))

    logging.debug('Program End')

if __name__ == "__main__":
    main()
    time.sleep(120)