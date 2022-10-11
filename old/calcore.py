import datetime
import logging
import time
logging.basicConfig(filename = 'log.txt',level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s')
logging.disable(logging.CRITICAL)



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
