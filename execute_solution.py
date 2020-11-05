# -*- coding: utf-8 -*-

from library.tdt_request import TDTRequest


class ExecuteSolution(object):
    """
    任务流操作，多任务流上线、下线
    """

    def __init__(self, tdt_protocol, tdt_host, tdt_port, federation_token):
        self.tdt = TDTRequest(federation_token, tdt_protocol, tdt_host, tdt_port)

    def online(self, solution_list):
        online_result = self.tdt.online_solution(solution_list)
        if online_result != 0:
            exit(-1)

    def offline(self, solution_list):
        offline_result = self.tdt.offline_solution(solution_list)
        if offline_result != 0:
            exit(-1)

    def online_file(self, solution_uuid_path):
        taskflow_uuid_list = open(solution_uuid_path, 'r', encoding='utf-8').read().split(",")
        self.online(taskflow_uuid_list)

    def offline_file(self, solution_uuid_path):
        taskflow_uuid_list = open(solution_uuid_path, 'r', encoding='utf-8').read().split(",")
        self.offline(taskflow_uuid_list)
