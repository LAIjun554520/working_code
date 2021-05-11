# -*- coding: utf-8 -*-

#  根据文件 taskflow_uuid中记录的uuid，查询每个任务流的一些执行信息并存放在文件中（待优化）

import pymysql
import os
import time

conn = pymysql.connect('172.26.0.88', user="root", passwd="623842918", port=3316, db="workflow_workflow1")
cursor = conn.cursor()
# conn.select_db('pythondb')
# 获取游标
# cur=conn.cursor()


taskflow_uuid_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "taskflow_uuid")
taskflow_uuid_list = open(taskflow_uuid_path, 'r', encoding='utf-8').read().split(",")


cur_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
check_count_result = "workflow_check_schedule_count" + cur_time
check_state_result = "workflow_check_state" + cur_time
check_time = "workflow_time" + cur_time
total_schedule = 0

with open(check_count_result, 'w', encoding='utf-8') as f:
    f.write("**********任务流调度数量***********")
    f.write(os.linesep)

with open(check_state_result, 'w', encoding='utf-8') as f:
    f.write("**********任务流执行状态分布*************")
    f.write(os.linesep)

with open(check_time, 'w', encoding='utf-8') as f:
    f.write("*********任务流执行时间情况*************")
    f.write(os.linesep)

print("获取任务流调度数量")
for taskflow in taskflow_uuid_list:
    sql = "select count(*) from WORKFLOW_FLOW_EXECUTION where hex(flowId) = \"" + taskflow + "\""
    # print(sql)
    cursor.execute(sql)
    res = cursor.fetchone()
    taskflow_schedule_count = res[0]
    schedule_count = "任务流" + taskflow + " 调度总数：" + str(taskflow_schedule_count)
    # print(schedule_count)
    with(open(check_count_result, 'a', encoding='utf-8')) as f:
        f.write(schedule_count)
        f.write(os.linesep)
    total_schedule = total_schedule + taskflow_schedule_count

with(open(check_count_result, 'a', encoding='utf-8')) as f:
    f.write("所有任务流总调度数量： " + str(total_schedule))
    f.write(os.linesep)

print("获取任务流不同执行状态的数量")
for taskflow in taskflow_uuid_list:
    flow_state_num = "select count(*), executionState from WORKFLOW_FLOW_EXECUTION " \
          "where hex(flowId) = \"" + taskflow + "\" group by executionState"
    # print(sql)
    state_list = []
    cursor.execute(flow_state_num)
    while 1:
        res = cursor.fetchone()
        if res is None:
            # 表示已经取完结果集
            break
        state_list.append(str(res))
    task_state_list = []
    task_state_num = "select count(*), executionState from WORKFLOW_TASK_EXECUTION " \
                     "where taskId in (select id from WORKFLOW_TASK " \
                     "where hex(parentFlowId) = \"" + taskflow + "\") group by executionState"
    cursor.execute(task_state_num)
    while 1:
        res = cursor.fetchone()
        if res is None:
            break
        task_state_list.append(str(res))
    with(open(check_state_result, 'a', encoding='utf-8')) as f:
        f.write("任务流 " + taskflow + "，不同状态的执行数量" + ",".join(state_list) + "；其中任务不同状态执行统计" + ",".join(task_state_list))
        f.write("\n")

print("获取任务流执行的最早开始时间，最晚开始时间，最小执行时间及最长执行时间")
for taskflow in taskflow_uuid_list:
    min_start = "select min(startTime) from WORKFLOW_FLOW_EXECUTION where hex(flowId) = \"" + taskflow + "\""
    max_start = "select max(startTime) from WORKFLOW_FLOW_EXECUTION where hex(flowId) = \"" + taskflow + "\""
    max_end = "select max(endTime) from WORKFLOW_FLOW_EXECUTION where hex(flowId) = \"" + taskflow + "\""
    min_duration = "select min(UNIX_TIMESTAMP(endTime) - UNIX_TIMESTAMP(startTime)) from WORKFLOW_FLOW_EXECUTION " \
                   "where hex(flowId) = \"" + taskflow + "\""
    max_duration = "select max(UNIX_TIMESTAMP(endTime) - UNIX_TIMESTAMP(startTime)) from WORKFLOW_FLOW_EXECUTION " \
                   "where hex(flowId) = \"" + taskflow + "\""
    # print(sql)
    cursor.execute(min_start)
    res = cursor.fetchone()
    min_start_time = str(res[0])
    cursor.execute(max_start)
    res = cursor.fetchone()
    max_start_time = str(res[0])
    cursor.execute(min_duration)
    res = cursor.fetchone()
    min_duration = str(res[0])
    cursor.execute(max_duration)
    res = cursor.fetchone()
    max_duration = str(res[0])
    cursor.execute(max_end)
    res = cursor.fetchone()
    max_end_time = str(res[0])
    message = "任务流 " + taskflow + "，最早开始执行：" + min_start_time + "，最晚开始执行：" + max_start_time + "，最小执行时长：" + min_duration + "，最长执行时长：" + max_duration + "，最晚结束时间：" + max_end_time
    with(open(check_time, 'a', encoding='utf-8')) as f:
        f.write(message)
        f.write("\n")

cursor.close()
conn.commit()
conn.close()
print('sql执行成功')
