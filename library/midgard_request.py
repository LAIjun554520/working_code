# -*- coding: utf-8 -*-

import requests
import json
from .utils import authorization_headers


class MidgardRequest(object):
    """
    Midgard api操作，包括服务创建、发布、申请使用、上线/配置路由
    """
    def __init__(self, token, protocol, host, port):
        self.midgard_session = requests.Session()
        self.midgard_session.headers = authorization_headers(service_token=token)
        self.midgard_url = protocol + "://" + host + ":" + str(port)
        if protocol == 'https':
            self.midgard_session.verify = False
        pass

    def update_api(self, api_message):
        # SQL模式
        api = self.midgard_url + "/studio/api/midgard/v1/apiConf/update"
        response = self.midgard_session.put(api, data=api_message)
        if response.status_code == 200:
            print("成功更新API，文件：", json.loads(api_message)["baseInfo"]["name"])
            return 0
        else:
            print("更新API失败，文件：", json.loads(api_message)["baseInfo"]["name"])
            print(response.text)
            return 1

    def update_api_table(self, api_message):
        # 向导模式
        api = self.midgard_url + "/studio/api/midgard/v1/apiConf/table/update"
        response = self.midgard_session.put(api, data=api_message)
        if response.status_code == 200:
            print("成功更新API，文件：", json.loads(api_message)["baseInfo"]["name"])
            return 0
        else:
            print("更新API失败，文件：", json.loads(api_message)["baseInfo"]["name"])
            print(response.text)
            return 1

    def publish_api(self, api_uuid, pulish_message):
        # 更新SQL模式的API
        api = self.midgard_url + "/studio/api/midgard/v1/apiConf/version/publish/%s" % api_uuid
        response = self.midgard_session.post(api, pulish_message)
        if response.status_code == 200:
            print("API ", api_uuid, "发布申请提交成功")
            return 0
        else:
            print("API ", api_uuid, "发布申请提交失败")
            return 1

    def add_route(self, routeMessage):
        api = self.midgard_url + "/studio/api/midgard/v1/route"
        response = self.midgard_session.put(api, routeMessage)
        if response.status_code == 200:
            print("成功添加路由")
            return 0
        else:
            print("添加路由失败")
            return 1

    def online_api(self, apiId, onlineMessage):
        api = self.midgard_url + "/studio/api/midgard/v1/api/online/%s" % apiId
        response = self.midgard_session.post(api, onlineMessage)
        if response.status_code == 200:
            print("API ", apiId, " 已上线")
            return 0
        else:
            print("API ", apiId, " 上线处理异常")
            return 1

    def apply_request(self, applyMessage):
        api = self.midgard_url + "/studio/api/midgard/v1/api/apply"
        response = self.midgard_session.post(api, applyMessage)
        if response.status_code == 200:
            print("使用申请已提交")
            return 0
        else:
            print("使用申请提交失败")
            print(response.text)
            return 1

    def get_api_route(self, apiId, message):
        api = self.midgard_url + "/studio/api/midgard/v1/route/%s" % apiId
        response = self.midgard_session.post(api, message)
        if response.status_code == 200:
            return json.loads(response.text)['data']
        else:
            print("获取API路由列表失败")
            print(response.text)
            return 1
