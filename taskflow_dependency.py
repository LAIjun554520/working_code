# -*- coding: utf-8 -*-


import argparse
import configparser
import os
from execute_taskflow import ExecuteTaskflow

from pattern.file_pattern.resolve import FileResolve
from pattern.taskflow_pattern.resolve import TaskflowResolve
from library.navigator_request import NavigatorRequest
from library.workflow_request import WorkflowRequest


def start_taskflow():
    generate = GenerateTaskflow(federation_token, navigator_protocol, navigator_host, navigator_port,
                                workflow_protocol, workflow_host, workflow_port)

    execute = ExecuteTaskflow(workflow_protocol, workflow_host, workflow_port, federation_token)

    if operation == "create":
        taskflow_list = generate.generate()
        # taskflow_list = generate.generate_flow_dep_1_1()
        print("任务流已创建： ", taskflow_list)

    if operation == "online" and uuid_file_path is None:
        taskflow_list = generate.generate()
        # taskflow_list = generate.generate_flow_dep_1_1()
        print("任务流已创建： ", taskflow_list)
        execute.online(taskflow_list)

    if operation == "online" and uuid_file_path is not None:
        execute.online_file(uuid_file_path)

    if operation == "offline":
        if uuid_file_path is None:
            print("缺少任务流id信息")
            exit(-1)
        execute.offline_file(uuid_file_path)


class GenerateTaskflow(object):
    def __init__(self,federation_token, navigator_protocol, navigator_host, navigator_port,
                                workflow_protocol, workflow_host, workflow_port):
        self.navigator = NavigatorRequest(federation_token, navigator_protocol, navigator_host, navigator_port)
        self.workflow = WorkflowRequest(federation_token, workflow_protocol, workflow_host, workflow_port)
        self.file_resolve = FileResolve()
        self.taskflow_resolve = TaskflowResolve()

    def generate(self):

        pass



if __name__ == '__main__':
    print("性能测试，任务流依赖测试，任务流创建、发布、下线操作，执行前请先更新conf文件")
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="create: 只创建; online: 创建并发布或者只发布; offline: 只下线", type=str)
    parser.add_argument("-p", help="任务uuid文件路径,在不需要创建任务的情况下，发布任务需要提供任务uuid文件。"
                                   "如果选择的操作方式为online且提供了uuid文件路径，则只进行发布操作；如果选择的操作方式为online但没有"
                                   "提供uuid文件路径，会先创建任务再发布。", type=str, default=None)
    parser.add_argument("-n", help="创建多少组", type=int)

    args = parser.parse_args()
    operation = args.t
    uuid_file_path = args.p
    group_number = args.n

    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf")
    config.read(config_path)

    tenant = config.get("user", "tenant")
    username = config.get("user", "username")
    password = config.get("user", "password")

    manager_ip = config.get("manager", "host")
    manager_username = config.get("manager", "username")
    manager_password = config.get("manager", "password")
    cluster_root_pass = config.get("manager", "cluster_root_password")
    navigator_protocol = config.get("navigator", "protocol")
    navigator_host = config.get("navigator", "host")
    navigator_port = config.get("navigator", "port")
    connector_protocol = config.get("connector", "protocol")
    connector_host = config.get("connector", "host")
    connector_port = config.get("connector", "port")

    tdt_protocol = config.get("tdt", "protocol")
    tdt_host = config.get("tdt", "host")
    tdt_port = config.get("tdt", "port")
    workflow_protocol = config.get("workflow", "protocol")
    workflow_host = config.get("workflow", "host")
    workflow_port = config.get("workflow", "port")
    federation_token = config.get("user", "federation_token")
    access_token = config.get("user", "access_token")


