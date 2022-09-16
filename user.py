
import requests
import json
import datetime



class HttpsClient(object):

    def __init__(self):
        pass

    @staticmethod
    def get(_url, _json):
        _resp = requests.get(_url, _json)
        return _resp.content


    def http_get(_url,headers):
        _resp = requests.get(_url,verify=False, headers=headers)
        return _resp.content

    @staticmethod
    def https_post(_url, _json_dict, headers):
        _resp = requests.post(_url, _json_dict, verify=False, headers=headers)
        return _resp.text




if __name__ == '__main__':
    for i in range(20):
        username = str('user') + str(i)
        email = 'qa' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) + '@qq.com'
        url = 'https://172.26.0.88:28191/studio/api/auth/v1/user/add'
        json_dict = {"username": username, "realName": username, "password": "123", "telephone": "13312341234",
                     "email": email, "roleIds": []}
        str_json_dict = json.dumps(json_dict)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'authorization': 'bearer d6148ad6-aac3-4b19-ad24-65654bf3439b'}
        result = HttpsClient.https_post(url, str_json_dict, headers)
        print(result)
        re_json = json.loads(result)
        re_json_data = re_json['data']
        user_id = re_json_data['id']
        user_name = re_json_data['username']
        print(user_id, user_name)
        print('----创建用户' + str(username) + '完成-----')
