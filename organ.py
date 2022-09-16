import requests
import json

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

# if __name__ == '__main__':
#     for i in range(1):
#         username = str('jwss111') + str(i)
#         url = 'https://172.26.2.15:28191/studio/api/auth/v1/organ/add'
#         json_dict = { "name": username, "parentId": "c06789c6-1e57-5bd6-1993-a388c6f9d25c" }
#         str_json_dict = json.dumps(json_dict)
#         headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
#                    'authorization': 'bearer bf8b5898-b506-4611-987f-682426f30eb2'}
#         result = HttpsClient.https_post(url, str_json_dict, headers)
#         print(result)
#         re_json = json.loads(result)
#         children = re_json[0]['children']
#         print(children)
#         son_children = children[15]['name']
#         print(son_children)


if __name__ == '__main__':
    for i in range(100):
        username = str('test') + str(i)
        url = 'https://172.26.2.15:28191/studio/api/auth/v1/organ/add'
        json_dict = { "name": username, "parentId": "ce7ce4cd-bb66-79ec-f881-805283f206fc" }
        str_json_dict = json.dumps(json_dict)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'authorization': 'bearer bf8b5898-b506-4611-987f-682426f30eb2'}
        result = HttpsClient.https_post(url, str_json_dict, headers)
        print(result)
        re_json = json.loads(result)
        children = re_json[0]['code']
        print('----' + str(i) + '----')
        # print(children)
        # son_children = children[15]['name']
        # print(son_children)