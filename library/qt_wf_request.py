import requests
import json
import re


class WF_Test(object):

    def __init__(self):
        pass

    def get_token(ip):
        ip = 'https://' + ip + ":28190/studio/api/auth/v1/token/getTestToken"
        headers= {'accept': 'application/json', 'Content-Type': 'application/json'}
        user_server_ip = "http://" + ip + ":28180/login/oauth2/code/foundation-gateway"
        json_dict = { "clientId": "gateway", "clientSecret": user_server_ip, "password": "admin", "userName": "admin" }
        data = json.dumps(json_dict)
        token = requests.post(ip, headers=headers, data=data, verify=False)
        return token.text

    def create_dir(navigator_ip, token, name,parentUUID):
        api = 'https://' + navigator_ip + ":28183/studio/api/navigator/v1/common/newDir"
        headers = {'accept': 'application/json', 'Content-Type': 'application/json','authorization': "Bearer %s" % token}
        json_dict = {"category": "WORKFLOW","description":"","name":name,"parentUUID":parentUUID,"nodeType":"DIR"}
        data = json.dumps(json_dict)
        response = requests.post(api, headers=headers, data=data, verify=False)
        if response.status_code == 200:
            new_dir_message = json.loads(response.text)
            new_dir_uuid = new_dir_message['uuid']
            print("成功创建文件夹，文件夹uuid: ", new_dir_uuid)
            return new_dir_uuid
        else:
            print("创建文件夹失败， 报错信息： ", response.text)
            return None

    def create_file(navigator_ip, token, file_name,dir_parentUUID):
        api = 'https://' + navigator_ip + ":28183/studio/api/navigator/v1/common/newFile"
        headers = {'accept': 'application/json', 'Content-Type': 'application/json','authorization': "Bearer %s" % token}
        json_dict = {"category": "WORKFLOW","datasources":"[]","name":file_name,"parentUUID":dir_parentUUID,"nodeType":"FILE","loadingType":"database"}
        data = json.dumps(json_dict)
        response = requests.post(api, headers=headers, data=data, verify=False)
        print(response)
        if response.status_code == 200:
            new_dir_message = json.loads(response.text)
            new_dir_uuid = new_dir_message['uuid']
            print("成功创建文件，文件uuid: ", new_dir_uuid)
            return new_dir_uuid
        else:
            print("创建文件失败， 报错信息： ", response.text)
            return None

    def flow_schemes(wf_server_ip,token,flow_scheme):
        api = 'http://' + wf_server_ip + ":28911/studio/api/workflow/v1/schemes"
        headers = {'accept': '*/*', 'Content-Type': 'application/json',
                   'authorization': "Bearer %s" % token}
        response = requests.put(api, data=flow_scheme, headers=headers)
        print(response.text)
        if response.status_code == 200:
            schemes_message = json.loads(response.text)
            succeed_message = schemes_message['message']
            print("成功更新文件，返回信息: ", succeed_message)
        else:
            print("更新文件失败， 报错信息： ", response.text)
            return None


    def get_flows(navigator_ip,token, uuid):
        api = 'https://' + navigator_ip + ":28183/studio/api/navigator/v1/common/data"
        headers = {'accept': 'application/json', 'Content-Type': 'application/json',
                   'authorization': "Bearer %s" % token}
        data = {"category": "WORKFLOW", "page": "1", "size": "100", "searchText": "", "uuid": uuid,"catalogFlag": False}
        json_dict = json.dumps(data)
        response = requests.post(api, data=json_dict, headers=headers, verify=False)
        print(response.text)
        if response.status_code == 200:
            flow_message = json.loads(response.text)
            file_total = flow_message['pagination']['total']
            print("成功获取文件，返回文件数量: ", file_total)
        else:
            print("获取文件失败， 报错信息： ", response.text)
        return response



if __name__ == '__main__':
    WF_Test.create_dir('172.26.0.87','bearer 4982b097-dc49-45bf-9b30-299a55b169cd','look3','D0C9AED6286E81A0D77DB237883614B4')

