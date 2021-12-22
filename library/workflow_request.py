# -*- coding: utf-8 -*-

import requests
import json
from .utils import authorization_headers


class WorkflowRequest(object):
    """
    workflow api操作，包括更新任务流设计，发布、下线任务流
    """
    def __init__(self, token, protocol, host, port):  # workflow不再直接访问guardian，改用foundation-user-server
        self.workflow_session = requests.Session()
        self.workflow_session.headers = authorization_headers(service_token=token)
        self.workflow_url = protocol + "://" + host + ":" + str(port)
        if protocol == 'https':
            self.workflow_session.verify = False
        pass

    def update_taskflow(self, taskflow_message):
        api = self.workflow_url + "/studio/api/workflow/v1/schemes"
        response = self.workflow_session.put(api, data=taskflow_message)
        if response.status_code == 200:
            print("成功更新任务流，任务流：", json.loads(taskflow_message)["flow"]["name"])
            return 0
        else:
            print("更新任务流失败，任务流：", json.loads(taskflow_message)["flow"]["name"])
            print(response.text)
            return 1

    def online_taskflow(self, taskflow_uuid):
        api = self.workflow_url + "/studio/api/workflow/v1/flows/%s/actions/deploy" % taskflow_uuid
        response = self.workflow_session.put(api)
        if response.status_code == 200:
            print("任务流", taskflow_uuid, "已发布")
            return 0
        else:
            print("任务流", taskflow_uuid, "发布失败")
            return 1

    def offline_taskflow(self, taskflow_uuid):
        api = self.workflow_url + "/studio/api/workflow/v1/flows/%s/actions/retire" % taskflow_uuid
        response = self.workflow_session.put(api)
        if response.status_code == 200:
            print("任务流", taskflow_uuid, "已下线")
            return 0
        else:
            print("任务流", taskflow_uuid, "下线失败")
            print("失败信息:", response.text)
            return 1
