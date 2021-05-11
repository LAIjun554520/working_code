#!/bin/bash

# 监控workflow scheduler、executor以及workflow用户对txsql操作进程占用的资源情况，将执行命令在scheduler、executor所在节点上执行

# ps -ef | grep workflow-scheduler，获取scheduler运行进程
# nohup top -p <scheduler_process> -b -n <次数> -d <时间间隔，单位s> >> <输出文件路径>  &
# 如 nohup top -p 22031 -b -n 80 -d 600 >> workflow_executor_top_22031.txt  &，为将executor进程资源占用情况，每10分钟获取一次，一共获取80次，结果重定向到workflow_executor_top_22031.txt文件中

# ps -ef | grep workflow-executor
# nohup top -p <executor_process> -b -n <times> -d <time_interval,s>  >>  <file_path>  &

# ps -ef | grep txsql | grep workflow | grep 13306
# nohup top -p <txsql_workflow_process> -p -n <times> -d <time_interval>  >>  <file_path>  &