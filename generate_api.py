# -*- coding: utf-8 -*-


import json
import requests
from pattern.file_pattern.resolve import FileResolve
from library.navigator_request import NavigatorRequest
from library.midgard_request import MidgardRequest
from library.bpm_request import BPMRequest
from pattern.midgard_pattern.resolve import MidgardResolve


class GenerateAPI(object):
    """
    解析用例文件，创建需要的任务流
    """

    def __init__(self, service_token, navigator_protocol, navigator_host, navigator_port,
                 midgard_protocol, midgard_host, midgard_port, bpm_protocol, bpm_host, bpm_port):
        self.navigator = NavigatorRequest(service_token, navigator_protocol, navigator_host, navigator_port)
        self.midgard = MidgardRequest(service_token, midgard_protocol, midgard_host, midgard_port)
        self.file_resolve = FileResolve()
        self.bpm = BPMRequest(service_token, bpm_protocol, bpm_host, bpm_port)
        self.midgard_resolve = MidgardResolve()
        self.midgard_protocol = midgard_protocol
        self.midgard_host = midgard_host
        self.midgard_port = midgard_port
        self.midgard_url = midgard_protocol + "://" + midgard_host + ":" + str(midgard_port)

    def generate_api(self, dir_uuid, api_name, api_pattern_file, datasource_id, route_pattern_file, dynamic_host):
        api_id = self.generate_file(api_name, dir_uuid)
        new_api = self.midgard_resolve.replace_api_message(api_pattern_file, api_name, api_id, datasource_id)
        print(new_api)
        self.midgard.update_api(new_api)  # 配置保存API
        publish_message = {"title": "1", "reason": "1"}
        self.midgard.publish_api(api_id, json.dumps(publish_message))  # 申请发布API
        # API发布审批
        bpm_list_api_publish = self.bpm.get_pending_task('MIDGARD_API_PUBLISH')  # 获取api发布待审批流程
        for item in bpm_list_api_publish:
            print(item)
            json_data = self.bpm.get_api_publish_content(item)
            approve_message = {"action": "APPROVE", "processDefinitionKey": "MIDGARD_API_PUBLISH",
                               "processInstanceId": item, "jsonData": json_data}
            self.bpm.approve_api_publish(item, json.dumps(approve_message))
        # API管理，添加路由
        route_path = '/dc_test/' + api_name
        new_route = self.midgard_resolve.replace_route_message(route_pattern_file, api_id, api_name, dynamic_host, route_path)
        self.midgard.add_route(new_route)
        # API管理，上线API
        self.midgard.online_api(api_id, self.midgard_resolve.replace_online_version_message('online_version.json'))
        # 申请使用
        apply_message = {"apiId": api_id, "applyReason": "test", "title": "test"}
        user_list = json.loads(open('user_list.json', encoding='utf-8').read())  # 需要申请API使用的用户
        print(user_list)
        for user in user_list:
            user_message = {"clientId": "gateway", "clientSecret": "secret", "userName": user['userName'],
                            "password": user['password']}
            print(json.dumps(user_message))
            request_headers = {"accept": "application/json", "Content-Type": "application/json"}
            token_response = requests.post("https://172.26.2.15:28190/studio/api/auth/v1/token/getTestToken",
                                           data=json.dumps(user_message), verify=False, headers=request_headers)
            user_token = token_response.text
            token_response.close()
            midgard_apply_request = MidgardRequest(user_token, self.midgard_protocol, self.midgard_host,
                                                   self.midgard_port)
            midgard_apply_request.apply_request(json.dumps(apply_message))
            midgard_apply_request.midgard_session.close()
        # API使用申请审批
        bpm_list_api_apply = self.bpm.get_pending_task('MIDGARD_API_APPLY')
        for item in bpm_list_api_apply:
            apply_basic_content = json.loads(self.bpm.get_api_apply_content(item))
            route_request_size = {"page": 1, "size": 10, "searchText": ""}
            api_route = self.midgard.get_api_route(api_id, json.dumps(route_request_size))[0]['id']  # 暂定使用第一个路由
            apply_basic_content['routeId'] = api_route
            approve_message = {"action": "APPROVE", "processDefinitionKey": "MIDGARD_API_APPLY",
                               "processInstanceId": item, "jsonData": json.dumps(apply_basic_content)}
            print(json.dumps(approve_message))
            self.bpm.approve_api_apply(item, json.dumps(approve_message))

    def generate_dir(self, dir_num, dir_name):
        dir_list = []
        for i in range(dir_num):
            new_dir = dir_name + str(i)
            dir_pattern = self.file_resolve.get_pattern(new_dir, "-", "dir", "SERVICE")
            dir_uuid = self.navigator.create_dir(dir_pattern)
            dir_list.append(dir_uuid)
        return dir_list

    def generate_file(self, api_name, dir_uuid):
        file_pattern = self.file_resolve.get_pattern(api_name, dir_uuid, "file", "SERVICE")
        print(file_pattern)
        file_uuid = self.navigator.create_file(file_pattern)
        return file_uuid


if __name__ == '__main__':
    generate_api = GenerateAPI('09c7ec54-6aae-4875-88ca-47ef826beaf4', 'https', '172.26.2.15', '28183', 'https',
                               '172.26.2.13', '28141', 'https', '172.26.2.13', '28188')
    base_name = 'auto_test'
    num = 100
    dir_uuid = generate_api.generate_dir(1, 'test')[0]
    for i in range(1):
        api_name = base_name + str(i)
        generate_api.generate_api(dir_uuid, api_name, 'api_sample.json', 'f88e9578dc254948871fb193d6184d95',
                                  'route.json', 'node215')
