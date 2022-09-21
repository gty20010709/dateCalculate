# 使用手册

## 程序功能说明
资料室图书借阅时长为14天，如果超过14天，在读者归还图书时，需要缴纳违约金。但资料室闭馆的时间，是不算入读者借阅时间的。
资料室闭馆的时间，包括寒暑假，法定节假日等。人工计算图书违约时间比较麻烦，且不甚准确。
此程序就是为了辅助资料室管理员计算图书违约的时间。

## 主程序
主程序运行时，会要求用户输入：<br>
- 图书借阅日期<br>
图书借阅日期的读取，设计了容错功能，如果输入错误，程序会提示重新输入。<br>
日期格式参见"杂项-日期格式"。

- 图书归还日期<br>
图书归还日期的缺省值是程序运行的当天，但如果运行该程序的计算机本地的日期有误，则需要用户手动输入日期。<br>
如果系统时间有误，或不需要使用当天日期作为还书时间，在日期输入错误的时候，需要重新运行程序。<br>
日期格式参见"杂项-日期格式"。<br>


## 配置文件 
- 注释<br>
注释以'#'开头，需单独一行。
- 单天<br>
设定“单天”日期的内容，需要写在 'single day:'之下，这么安排，只是为了便于管理，实际上写在哪里都不影响。<br>
“单天”用于指定需要排出借阅时间的日期，比如中秋（2022年9月10～12）三天，图书室闭馆，可以手动将这三天的日期加入配置文件中。<br>
周日惯例闭馆，系统已自动将其排除，不需要手动将周日添加到排除列表。<br>
日期格式参见"杂项-日期格式"。

``` txt
2022/10/10
2022/10/11
2022/10/12

```

- 时间段<br>
设定“时间段”日期的内容，需要写在'time range:'之下，也只是为了管理的方便，写在任何地方都不影响。<br>
“时间段”用于指定资料是长时间闭馆的时间，比如暑假（2022年6月26日 至 2022年9月4日），在两个时间点中用' - ' （注意 `-` 两侧的空格）<br>
两个时间点的日期格式参见"杂项-日期格式"。
```txt
2022/6/26 - 2022/9/4
```


## 杂项
- 日期格式
YYYY/MM/DD<br>
example1: 2022/9/20<br>
example2: 2022/09/20<br>
PS: 日期中的 / （斜杠）需要是半角字符，将输入法切换到英文格式即可

- 程序维护与改进<br>
小程序花了一个晚上和早上，匆匆写出，可能会存在不足，日后更新会同步在：https://github.com/gty20010709/dateCalculate
<br> 
对程序使用存在疑问，或有意见和建议，请联系zlz_gty@foxmail.com