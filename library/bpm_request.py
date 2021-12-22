# -*- coding: utf-8 -*-

import requests
import json
from .utils import authorization_headers


class BPMRequest(object):
    """
    Midgard api操作，包括服务创建、发布、申请使用、上线/配置路由
    """
    def __init__(self, token, protocol, host, port):
        self.bpm_session = requests.Session()
        self.bpm_session.headers = authorization_headers(service_token=token)
        self.bpm_url = protocol + "://" + host + ":" + str(port)
        if protocol == 'https':
            self.bpm_session.verify = False
        pass

    def get_pending_task(self, applyType):
        # 根据申请类型过滤所有待办流程
        api = self.bpm_url + "/studio/api/bpm/v1/hq/assignee/%s/pending/task?type=%s&page=1&size=10" % (applyType, applyType)
        response = self.bpm_session.get(api)
        content = json.loads(response.text)
        process_instance_list = []
        for item in content['data']['data']:
            print(item)
            process_instance_list.append(item['processInstanceId'])
        return process_instance_list

    def get_api_publish_content(self, processInstanceId):
        # 根据processInstanceId获取发布待审批的API详情
        api = self.bpm_url + "/studio/api/bpm/v1/hq/MIDGARD_API_PUBLISH/task/%s" % processInstanceId
        response = self.bpm_session.get(api)
        print(response.text)
        content = json.loads(response.text)['data']['content']
        # print(content)
        return content

    def approve_api_publish(self, processInstanceId, approveMessage):
        # 根据processInstanceId通过API发布审批
        api = self.bpm_url + "/studio/api/bpm/v1/hq/MIDGARD_API_PUBLISH/approve/%s" % processInstanceId
        response = self.bpm_session.post(api, approveMessage)
        if response.status_code == 200:
            print("API发布审批成功")
            return 0
        else:
            print("API发布审批异常")
            print(response.text)
            return 1

    def get_api_apply_content(self, processInstanceId):
        # 根据processInstanceId获取申请使用待审批的流程详情
        api = self.bpm_url + "/studio/api/bpm/v1/hq/MIDGARD_API_APPLY/task/%s" % processInstanceId
        response = self.bpm_session.get(api)
        content = json.loads(response.text)['data']['content']
        print(content)
        return content

    def approve_api_apply(self, processInstanceId, approveMessage):
        api = self.bpm_url + "/studio/api/bpm/v1/hq/MIDGARD_API_APPLY/approve/%s" % processInstanceId
        response = self.bpm_session.post(api, approveMessage)
        if response.status_code == 200:
            print("API使用申请审批成功")
            print(response.text)
            return 0
        else:
            print("API使用申请审批异常")
            print(response.text)
            return 1
