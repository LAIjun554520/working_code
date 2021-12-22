#!/bin/bash

dir_uuid=$1
mysql_host=$2
mysql_port=$3
mysql_root_password=$4
workflow_database=$5

echo "update cron of flows in dir, dir list ${dir_uuid}"
echo "mysql_host: ${mysql_host}, port: ${mysql_port}"
echo "mysql_password: $mysql_root_password"
echo "workflow_database: ${workflow_database}"
echo "在有mysql客户端的环境上执行"

dir_list=`cat ${dir_uuid}`
dir_array=(${dir_list//,/ })
for uuid in ${dir_array[@]}
do
  echo dir:${uuid}
  mysql -h ${mysql_host} -P ${mysql_port} -u root -p${mysql_root_password} -e "update ${workflow_database}.WORKFLOW_TASK set execSpec = \"\{\\\"taskExecSpecType\\\"\:\\\"SCRIPT\\\",\\\"scriptCommands\\\"\:\\\"echo a\\\nsleep 900\\\nhostname\\\"\}\" where lower(hex(parentFlowId)) in (select uuid from navigator_foundation1.navigation where parent_uuid = \"${uuid}\")"
done


