#!/bin/bash

# 在有mysql客户端的机器上定时执行，预期任务流和任务执行并发数达到当前配置上限

txsql_ip=$1
txsql_root_password=$2
database=$3

# 工作流并发执行数量
taskflow_num=`mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*), executionState from ${database}.WORKFLOW_FLOW_EXECUTION group by executionState"`
task_num=`mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*), executionState from ${database}.WORKFLOW_TASK_EXECUTION group by executionState"`
echo "********`date`*******" >> /tmp/workflow_execution_sta.txt
echo "taskflow execution" >> /tmp/workflow_execution_sta.txt
echo running: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_FLOW_EXECUTION where executionState = 4"` >> /tmp/workflow_execution_sta.txt
echo waiting: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_FLOW_EXECUTION where executionState < 4"` >> /tmp/workflow_execution_sta.txt
echo completed: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_FLOW_EXECUTION where executionState = 5"` >> /tmp/workflow_execution_sta.txt
echo failed: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_FLOW_EXECUTION where executionState = 6"` >> /tmp/workflow_execution_sta.txt
echo blocked: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_FLOW_EXECUTION where executionState = 8"` >> /tmp/workflow_execution_sta.txt
echo "task execution" >> /tmp/workflow_execution_sta.txt
echo running: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 3"` >> /tmp/workflow_execution_sta.txt
echo waiting: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState < 3"` >> /tmp/workflow_execution_sta.txt
echo completed: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 4"` >> /tmp/workflow_execution_sta.txt
echo failed: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 5"` >> /tmp/workflow_execution_sta.txt
echo cancelled: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 6"` >> /tmp/workflow_execution_sta.txt
echo skipped: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 7"` >> /tmp/workflow_execution_sta.txt
echo filtered: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 8"` >> /tmp/workflow_execution_sta.txt
echo blocked: `mysql -h ${txsql_ip} -P 3316 -u root -p${txsql_root_password} -e "select count(*) from ${database}.WORKFLOW_TASK_EXECUTION where executionState = 9"` >> /tmp/workflow_execution_sta.txt
echo "" >> /tmp/workflow_execution_sta.txt