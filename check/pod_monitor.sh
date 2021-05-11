#!/bin/bash

#  测试环境未安装aquila的情况下，用于监控资源占用情况

service_name=$1   # 需要监视的服务
pod_name=$2  # 需要查看的pod的名称

s_pid=`ps -ef | grep ${service_name} | grep ${pod_name} | awk '{print $2}'`
s_pid=`echo ${s_pid} | awk '{print $3}'`
#echo $s_pid
echo ${service_name},${pod_name},${s_pid} >> ${service_name}_${pod_name}.txt
echo "*******`date`*******" >> ${service_name}_${pod_name}.txt
top -p ${s_pid} -b -n 1 -d 1 >> ${service_name}_${pod_name}.txt

#  top -b -n 1 -d 3 >> file.txt
#  -b：batch模式，可以重定向到文件
#  -n 1：一共取一次top 数据。后边加数字，表示次数
#  -d 3：每次top 时间间隔是3