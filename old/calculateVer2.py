import datetime
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
# logging.disable(logging.CRITICAL)


def getInput():
    startDay = datetime.datetime.strptime(input('图书借出的日期是：'),'%Y/%m/%d')
    try:
        endDay = datetime.datetime.strptime(input('（不输入就是程序运行当天）\n图书归还的日期是：'),'%Y/%m/%d')
    except:
        endDay = datetime.datetime.today()
    return startDay,endDay

def parseConfig(path):
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


def calculate(startDay,endDay,passDay,specialDay):
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





def main():
    logging.debug('Program Start')
    # Test datetime
    # startDay = '2022/9/15'
    # endDay = '2022/10/11'
    startDay,endDay = getInput()

    configPath = 'config.txt'
    specialDay,passDay = parseConfig(configPath)
    # logging.debug(specialDay)
    # logging.debug(singelDay)
    # logging.debug(timeRange)
    count,totalDays = calculate(startDay,endDay,passDay,specialDay)
    print(f'''
书籍持有时间{totalDays}
有效借阅时间{count}天
逾期{count - 14}天
应缴违约金{0.5*(count - 14)}
''')


if __name__ == '__main__':
    main()