import datetime

fi = open('config.txt','r',encoding='utf8')

flag = 0
specialDay = []
singleDay = []
timeRange = []

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

print(specialDay)
print(singleDay)
print(timeRange)

    

