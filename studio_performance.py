# -*- coding: utf-8 -*-
import argparse
import configparser
import os
from generate_solution import GenerateSolution
from execute_solution import ExecuteSolution
from library.guardian_request import GuardianRequest
from generate_taskflow import GenerateTaskflow
from execute_taskflow import ExecuteTaskflow


def start_dataload():
    generate = GenerateSolution(case_path, federation_token, access_token, navigator_protocol, navigator_host,
                                navigator_port, connector_protocol, connector_host, connector_port, tdt_protocol,
                                tdt_host, tdt_port)

    execute = ExecuteSolution(tdt_protocol, tdt_host, tdt_port, federation_token)

    if operation == "create":
        solution_list = generate.generate()
        print("数据加载任务已创建： ", solution_list)

    if operation == "online" and uuid_file_path is None:
        solution_list = generate.generate()
        print("数据加载任务已创建： ", solution_list)
        execute.online(solution_list)

    if operation == "online" and uuid_file_path is not None:
        execute.online_file(uuid_file_path)

    if operation == "offline":
        if uuid_file_path is None:
            print("缺少数据加载任务uuid信息")
            exit(-1)
        execute.offline_file(uuid_file_path)


def start_taskflow():
    generate = GenerateTaskflow(case_path, federation_token, navigator_protocol, navigator_host, navigator_port,
                                workflow_protocol, workflow_host, workflow_port)

    execute = ExecuteTaskflow(workflow_protocol, workflow_host, workflow_port, federation_token)

    if operation == "create":
        taskflow_list = generate.generate()
        print("任务流已创建： ", taskflow_list)

    if operation == "online" and uuid_file_path is None:
        taskflow_list = generate.generate()
        print("任务流已创建： ", taskflow_list)
        execute.online(taskflow_list)

    if operation == "online" and uuid_file_path is not None:
        execute.online_file(uuid_file_path)

    if operation == "offline":
        if uuid_file_path is None:
            print("缺少任务流id信息")
            exit(-1)
        execute.offline_file(uuid_file_path)


if __name__ == '__main__':
    print("******studio 性能测试，所需任务准备及操作，不包含数据校验******")
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="待执行的用例名称（用例文件名：用例名称.yml）", type=str)
    parser.add_argument("-t", help="create: 只创建; online: 创建并发布或者只发布e; offline: 只下线", type=str)
    parser.add_argument("-p", help="任务uuid文件路径", type=str, default=None)
    parser.add_argument("-a", help="是否重新获取federation token、access token，y or n，如果不需要重新获取，将从配置文件中"
                                   "获取token信息", type=str)
    parser.add_argument("-k", help="任务类型，dataload或者workflow", type=str)

    args = parser.parse_args()
    operation = args.t
    uuid_file_path = args.p
    task_type = args.k
    case_file = args.c + ".yml"
    case_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_cases", task_type, case_file)
    token_update = args.a

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

    if token_update == 'n':
        federation_token = config.get("user", "federation_token")
        access_token = config.get("user", "access_token")
    else:
        guardian_request = GuardianRequest(manager_ip, cluster_root_pass, manager_username, manager_password, username,
                                           password, tenant)
        federation_token = guardian_request.get_federation_token()
        access_token = guardian_request.get_access_token()

    print("本次执行用例类型：", task_type, "，用例文件：", case_path)
    if task_type == "dataload":
        start_dataload()
    if task_type == "workflow":
        start_taskflow()
