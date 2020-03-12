# TraceFileAnalyser

@[TOC]


==本人不是程序猿，写程序只是学习==
#### 程序源码
https://github.com/ericzhong2010/TraceFileAnalyser

#### 概要说明
10046事件是Oracle提供的一个用于分析性能的工具，它能帮助我们解析一条/多条SQL、PL/SQL语句的运行状态，这些状态包括 ：Parse/Fetch/Execute三个阶段中遇到的等待事件、消耗的物理和逻辑读、CPU时间、执行计划等等。

Oracle数据库遇到程序需要做性能追踪时，通常会用10046事件进行日志收集。10046事件启用、日志查询、分析可以参考如下文章。
[Oracle 10046事件相关](https://blog.csdn.net/weixin_38623994/article/details/102262538)

此工具可以针对最终的TKPROF格式化日志进行快速排序定位，否则将需要在批量的日志中寻找问题语句。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200312223330872.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODYyMzk5NA==,size_16,color_FFFFFF,t_70)

#### 程序截图
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200312223701478.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl8zODYyMzk5NA==,size_16,color_FFFFFF,t_70)