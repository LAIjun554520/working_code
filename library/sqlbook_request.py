import requests
import json



class Sqlbook_Test(object):

    def __init__(self):
        pass

    def open_instance(sqlbook_ip, token):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/instance/open"
        print("请求地址：", api)
        headers = {'Accept': 'application/json', 'authorization': token}
        result = requests.post(api, verify=False, headers=headers)
        return result.text



    def close_instance(sqlbook_ip, instanceUuid, token):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/instance/close"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token, 'Content-Type': 'application/json'}
        json_dict = {"instanceUuid": instanceUuid}
        data = json.dumps(json_dict)
        result = requests.post(api, data=data, verify=False, headers=headers)
        return result.text


    def sql_value(sqlbook_ip, token, file_uuid):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/file/" + file_uuid + "/content"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token}
        result = requests.get(api, verify=False, headers=headers)
        return result.text

    def sql_register(sqlbook_ip, token,dataSourceUuid, fileUuid, instanceUuid, value):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/execution/register"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token, 'Content-Type': 'application/json'}
        json_dict = {"dataSourceUuid": dataSourceUuid, "fileUuid": fileUuid,"instanceUuid": instanceUuid, "value": value}
        data = json.dumps(json_dict)
        print(data)
        result = requests.post(api, data=data, verify=False, headers=headers)
        return result.text

    def get_result(sqlbook_ip, token, registerId):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/execution/register/" + str(registerId) + "/items"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token}
        result = requests.get(api, verify=False, headers=headers)
        return result.text


    def get_result_count(sqlbook_ip, token, registerId):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/execution/register/" + str(registerId) + "/statistics"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token}
        result = requests.get(api, verify=False, headers=headers)
        return result.text

    def get_session(sqlbook_ip, token):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/instance/list"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token}
        result = requests.post(api, verify=False, headers=headers)
        return result.text

    def retry_datasource(sqlbook_ip, token, dataSourceUuid, fileUuid, instanceUuid):
        api = 'https://' + sqlbook_ip + "/studio/api/sqlbook/v2/instance/datasource/retry"
        print("请求地址：", api)
        headers= {'Accept': 'application/json', 'authorization': token}
        json_dict = {"dataSourceUuid": dataSourceUuid, "fileUuid": fileUuid,"instanceUuid": instanceUuid}
        data = json.dumps(json_dict)
        print(data)
        result = requests.post(api, data=data, verify=False, headers=headers)
        return result.text




