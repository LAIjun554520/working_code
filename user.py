
import requests
import json
import datetime


# user_web_ip = '172.26.0.88:28191'
# authorization = 'bearer 3532d9e4-3df2-4441-bd3c-6660dc17d326'

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
    for i in range(1):
        username = str('ssa') + str(i)
        email = 'qa' + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) + '@qq.com'
        url = 'https://172.26.0.88:28191/studio/api/auth/v1/user/add'
        json_dict = {"username": username, "realName": username, "password": "123", "telephone": "13312341234",
                     "email": email, "roleIds": ["2"], "organCode": "rootOrgan"}
        str_json_dict = json.dumps(json_dict)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'authorization': 'bearer e8968b06-c4d2-40c9-8582-d45b30c9fe49'}
        result = HttpsClient.https_post(url, str_json_dict, headers)
        print(result)
        re_json = json.loads(result)
        re_json_data = re_json['data']
        user_id = re_json_data['id']
        user_name = re_json_data['username']
        print(user_id, user_name)
        print('----创建用户' + str(username) + '完成-----')
