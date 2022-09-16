# import requests
#
# headers = {
#     'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
#     'Accept': '*/*',
#     'Content-Type': 'application/json',
#     'Authorization': 'Bearer 7ce096b1-cd04-4429-a556-1840d57daf6b',
# }
import json

data = { "flow": { "id": {uuid}, "name": "test1", "description": "flow-created-from-dir", "flowType": "INTERNAL", "cronType": "CRON_EXPRESSION", "configuration": { "cronPattern": "0 0 0 ? * * *", "cronHour": 0, "cronMinute": 0, "executionTimeoutCancelEnable": "false", "executionTimeoutCancel": 0, "executionTimeoutCancelUnit": "MINUTES", "executionTimeoutAlarmEnable": "false", "executionTimeoutAlarm": 7200, "dependLastPolicy": "NO", "globalParameters": [], "workspaceParameters": [] }, "schedulePriority": "LOW_PRIORITY", "scheduleCalendarId": "NO_CALENDAR", "deployState": "DEV", "executorGroupId": -1, "parameters": [], "operator": "null", "createDateTime": 1661506313187, "businessId": "null", "businessType": "null" }, "preDependencies": [], "tasks": [{ "id": "1ccb348d20764cc3ba3ed81476faec36", "name": "new task", "description": "", "taskType": "SCRIPT", "configuration": { "cronEnabled": "false", "cronType": "CRON_EXPRESSION", "cronPattern": "0 0 0 ? * * *", "cronHour": 0, "cronMinute": 0, "executionTimeoutCancelEnabled": "false", "executionTimeoutCancel": 0, "executionTimeoutCancelUnit": "MINUTES", "executionRetryEnabled": "false", "executionMaxRetryCount": 0, "executionRetryInterval": 15, "executionRetryIntervalUnit": "MINUTES" }, "execSpec": { "scriptMode": "SCRIPT_SENTENCE", "scriptCommands": "null", "scriptExecFileName": "null", "scriptExecArgs": "null" }, "parentFlowId": "bd2356d58fab4e03b1b5ebd076e24bdb", "upstreamRelations": {}, "downstreamRelations": {}, "executorGroupId": -1, "position": { "x": 201, "y": 212 }, "parameters": [], "tdtParameters": [], "preCondition": "null", "execEnvironmentId": "NO_ENVIRONMENT", "scriptFileId": "null", "scriptFileChecksum": "null", "refExternalResourceId": "NO_REF_RESOURCE", "businessId": "null", "businessType": "null" }], "scheduleCalendarEnabled": "false" }


# response = requests.put('http://172.26.0.88:28911/studio/api/workflow/v1/schemes', headers=headers, data=data)
print(type(data))