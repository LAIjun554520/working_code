#!/bin/bash

dir_uuid=$1
mysql_host=$2
mysql_port=$3
mysql_root_password=$4
workflow_database=$5
cron_pattern=$6

echo "update cron of flows in dir, dir list ${dir_uuid}"
echo "mysql_host: ${mysql_host}, port: ${mysql_port}"
echo "mysql_password: $mysql_root_password"
echo "workflow_database: ${workflow_database}"
echo "更新后的cron表达式：${cron_pattern}"
echo "在有mysql客户端的环境上执行"

#mysql -h ${mysql_host} -P ${mysql_port} -u root -p${mysql_root_password} -e "use ${workflow_database};show tables;"

dir_list=`cat ${dir_uuid}`
dir_array=(${dir_list//,/ })
for uuid in ${dir_array[@]}
do
  echo dir:${uuid}
  mysql -h ${mysql_host} -P ${mysql_port} -u root -p${mysql_root_password} -e "update ${workflow_database}.WORKFLOW_FLOW set configuration = \"\{\\\"cronPattern\\\"\:\\\"${cron_pattern}\\\",\\\"cronHour\\\"\:0,\\\"cronMinute\\\"\:0,\\\"executionTimeoutCancelEnable\\\"\:false,\\\"executionTimeoutCancel\\\":0,\\\"executionTimeoutCancelUnit\\\"\:\\\"MINUTES\\\",\\\"executionTimeoutAlarmEnable\\\"\:false,\\\"executionTimeoutAlarm\\\"\:7200,\\\"dependLastPolicy\\\"\:\\\"NO\\\"\}\" where lower(hex(id)) in (select uuid from navigator_foundation1.navigation where parent_uuid = \"${uuid}\")"
#  mysql -h ${mysql_host} -P ${mysql_port} -u root -p${mysql_root_password} -e "update ${workflow_database}.WORKFLOW_FLOW set configuration = '{'cronPattern':'${cron_pattern}','cronHour':0,'cronMinute':0,'executionTimeoutCancelEnable':false,'executionTimeoutCancel':0,'executionTimeoutCancelUnit':'MINUTES','executionTimeoutAlarmEnable':false,'executionTimeoutAlarm':7200,'dependLastPolicy':'NO'}' where hex(id) = ${uuid}"
#  mysql -h ${mysql_host} -P ${mysql_port} -u root -p${mysql_root_password} -e "update ${workflow_database}.WORKFLOW_FLOW set configuration = '\{\'cronPattern\'\:\'${cron_pattern}\',\'cronHour\'\:0,\'cronMinute\'\:0,\'executionTimeoutCancelEnable\'\:false,\'executionTimeoutCancel\'\:0,\'executionTimeoutCancelUnit\'\:\'MINUTES\',\'executionTimeoutAlarmEnable\'\:false,\'executionTimeoutAlarm\'\:7200,\'dependLastPolicy\'\:\'NO\'\}' where hex\(id\) = ${uuid}"
done