#!/bin/python3


README = '''
    这个小程序用来计算违约图书违约的时长；
    进一步给出应交付的罚金

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
from shutil import which

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
# logging.disable(logging.CRITICAL)

print(README)



def getInput():
    tips = '''
    开始日期和结束日期的格式如下：
    2022/9/10
    PS: 注意中间的斜杠需要是半角字符（输入法切换到英文状态即可）\n
    '''
    print(tips)
    startTime = datetime.datetime.strptime(input('请输入借书的日期：'),'%Y/%m/%d')
    logging.debug(startTime)
    endTime = datetime.datetime.strptime(input('请输入还书的日期：'),'%Y/%m/%d')
    logging.debug(endTime)
    totalDays = endTime - startTime
    logging.debug(totalDays)
    return startTime,endTime,totalDays

def parseConfig() -> list :
    configFile = open('config.txt','r')
    passDate = []
    for line in configFile:
        line = line.strip() # 去除非必要空白字符
        if line.startswith('#') or len(line) == 0 or line.startswith('single day') or line.startswith('time range'):
            # ignore useless lines
            continue
        logging.debug(line)
        if len(line) < 10:
            logging.debug(f'The line is {line}.')
            singleDay = datetime.datetime.strptime(line,'%Y/%m/%d')
            logging.debug(f'singleDay is {singleDay}')
            passDate.append(singleDay)
        #     continue
        if len(line) > 16:
            rangeStart,rangeEnd = tuple(line.split(' - ')) # 将'time range'的开始日期和结束日期分离
            
            # 解析出datatime对象 
            rangeStart = datetime.datetime.strptime(rangeStart,'%Y/%m/%d')
            rangeEnd = datetime.datetime.strptime(rangeEnd,'%Y/%m/%d')
            logging.debug(rangeStart)
            logging.debug(rangeEnd)

            # 创建一个时间单位，以便于下面将时间段中的时期加入排除列表中
            unitDay = datetime.timedelta(days=1)
            while rangeStart <= rangeEnd:
                passDate.append(rangeStart)
                rangeStart += unitDay
        # logging.debug(passDate)
    return passDate




def main():
    logging.debug('Program Start')

    startTime,endTime,totalDays=  getInput()
    passDate = parseConfig()

    # calculate the count of days
    count = 0
    unitday = datetime.timedelta(days=1)
    # 对从借书到还书中的每一天进行遍历
    while startTime <= endTime:
        # 如果日期在排除列表中，或日期是星期天，则跳过
        if (startTime not in passDate) and (datetime.datetime.weekday(startTime) != 6): 
            count += 1
        startTime += unitday
    logging.debug(f'The reuslt is {count} day(s).')

    if count <= 14:
        print('图书未逾期！')
    elif count > 14:
        fine = (count - 14) * 0.5
        print(f'图书逾期{count - 14}天，应缴纳违约金：{fine}元！')

    logging.debug('Program End')

if __name__ == "__main__":
    main()

