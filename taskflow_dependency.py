# -*- coding: utf-8 -*-


import argparse
import configparser
import os
import json

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
        dir_num = group_number // 200 + 1
        print("dir_num:", dir_num)
        group_in_one_dir = 200  # 一个文件夹内的任务流数量
        group_remain = group_number % 200
        print("group_remain, ", group_remain)
        dir_list = self.generate_dir(dir_num, "other_service_8_add_re")
        taskflow_uuid_list = []
        for i in range(dir_num):
            print(i)
            dir_uuid = dir_list[i]
            print(dir_uuid)
            group_tmp_num = group_in_one_dir
            if i == dir_num - 1:
                group_tmp_num = group_remain
            for j in range(group_tmp_num):
                flowA_name = "flowA_" + str(j)
                flowB_name = "flowB_" + str(j)
                flowC_name = "flowC_" + str(j)
                flowA_uuid = self.generate_flowA(flowA_name, dir_uuid)
                flowB_preDependencies = [{"id": flowA_uuid, "name": flowA_name}]
                flowB_uuid = self.generate_flowB(flowB_name, dir_uuid, flowB_preDependencies)
                # flowC_preDependencies = [{"id": flowA_uuid, "name": flowA_name}, {"id": flowB_uuid, "name": flowB_name}]
                # flowC_uuid = self.generate_flowC(flowC_name, dir_uuid, flowC_preDependencies)
                taskflow_uuid_list.append(flowA_uuid)
                taskflow_uuid_list.append(flowB_uuid)
                # taskflow_uuid_list.append(flowC_uuid)

        with open("taskflow_uuid_taskflow_dep", 'w') as uw:
            uw.write(",".join(taskflow_uuid_list))

        return taskflow_uuid_list

    def generate_flowA(self, taskflow_name, dir_uuid, preDependencies=None):
        file_pattern = self.file_resolve.get_pattern(taskflow_name, dir_uuid, "file", "WORKFLOW")
        file_uuid = self.navigator.create_file(file_pattern)
        original_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pattern", "taskflow_pattern",
                                             "other_service_8", "flowA.json")
        original_pattern = open(original_pattern_path, 'r').read()
        target_taskflow = self.taskflow_resolve.replace_message(original_pattern, taskflow_name, file_uuid, preDependencies)
        update_result = self.workflow.update_taskflow(target_taskflow)
        if update_result == 0:
            return file_uuid
        else:
            exit(-1)

    def generate_flowB(self, taskflow_name, dir_uuid, preDependencies=None):
        file_pattern = self.file_resolve.get_pattern(taskflow_name, dir_uuid, "file", "WORKFLOW")
        file_uuid = self.navigator.create_file(file_pattern)
        original_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pattern", "taskflow_pattern",
                                             "other_service_8", "flowB.json")
        original_pattern = open(original_pattern_path, 'r').read()
        target_taskflow = self.taskflow_resolve.replace_message(original_pattern, taskflow_name, file_uuid, preDependencies)
        update_result = self.workflow.update_taskflow(target_taskflow)
        if update_result == 0:
            return file_uuid
        else:
            exit(-1)

    def generate_flowC(self, taskflow_name, dir_uuid, preDependencies):
        file_pattern = self.file_resolve.get_pattern(taskflow_name, dir_uuid, "file", "WORKFLOW")
        file_uuid = self.navigator.create_file(file_pattern)
        original_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pattern", "taskflow_pattern",
                                             "per_exec_basic_change_17", "flowC.json")
        original_pattern = open(original_pattern_path, 'r').read()
        target_taskflow = self.taskflow_resolve.replace_message(original_pattern, taskflow_name, file_uuid,
                                                                preDependencies)
        update_result = self.workflow.update_taskflow(target_taskflow)
        if update_result == 0:
            return file_uuid
        else:
            exit(-1)

    def generate_dir(self, dir_num, dir_name):
        dir_list = []
        for i in range(dir_num):
            new_dir = dir_name + str(i)
            dir_pattern = self.file_resolve.get_pattern(new_dir, "-", "dir", "WORKFLOW")
            dir_uuid = self.navigator.create_dir(dir_pattern)
            dir_list.append(dir_uuid)
        return dir_list


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

    start_taskflow()
