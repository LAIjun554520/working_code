#!/bin/bash

taskflow_uuid=$1
navigator=$2
oauth2_token=$3

echo "taskflow_uuid file: ${taskflow_uuid}"
echo "navigator address: ${navigator}:28183，navigator端口变更请更改脚本"
echo "oauth2_token: ${oauth2_token}"

flows_list=`cat ${taskflow_uuid}`
flows_array=(${flows_list//,/ })
flows="["
for uuid in ${flows_array[@]}
do
  flow=\\\"$uuid\\\"
  flows=$flows$flow,
done
flows=${flows%?}
flows=${flows}"]"
#echo $flows
curl -k -X POST "https://${navigator}:28183/studio/api/navigator/v1/common/delete" -H "accept: application/json" -H "authorization: bearer ${oauth2_token}" -H "Content-Type: application/json" -d "${flows}"
