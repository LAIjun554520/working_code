#!/bin/bash

flows_list=`cat taskflow_uuid`
curl -k -X POST 'https://172.26.0.87:28183/studio/api/navigator/v1/common/delete' --data "[${flows_list}]" -H "accept: application/json" -H "authorization: bearer t9jpLK5Nwb09KrwBMFzK-FEDERATION" -H "Content-Type: application/json"
