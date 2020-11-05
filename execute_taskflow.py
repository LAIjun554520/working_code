# -*- coding: utf-8 -*-

from library.workflow_request import WorkflowRequest


class ExecuteTaskflow(object):
    """
    任务流操作，多任务流上线、下线
    """

    def __init__(self, workflow_protocol, workflow_host, workflow_port, federation_token):
        self.workflow = WorkflowRequest(federation_token, workflow_protocol, workflow_host, workflow_port)

    def online(self, taskflow_list):
        for item in taskflow_list:
            online_result = self.workflow.online_taskflow(item)
            if online_result == 1:
                exit(-1)

    def offline(self, taskflow_list):
        for item in taskflow_list:
            offline_result = self.workflow.offline_taskflow(item)
            if offline_result == 1:
                exit(-1)

    def online_file(self, taskflow_uuid_path):
        taskflow_uuid_list = open(taskflow_uuid_path, 'r', encoding='utf-8').read().split(",")
        self.online(taskflow_uuid_list)

    def offline_file(self, taskflow_uuid_path):
        taskflow_uuid_list = open(taskflow_uuid_path, 'r', encoding='utf-8').read().split(",")
        self.offline(taskflow_uuid_list)
