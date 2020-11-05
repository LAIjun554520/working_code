# -*- coding: utf-8 -*-


import yaml
from pattern.file_pattern.resolve import FileResolve
from pattern.taskflow_pattern.resolve import TaskflowResolve
from library.navigator_request import NavigatorRequest
from library.workflow_request import WorkflowRequest


class GenerateTaskflow(object):
    """
    解析用例文件，创建需要的任务流
    """
    def __init__(self, case_path, federation_token, navigator_protocol, navigator_host, navigator_port,
                 workflow_protocol, workflow_host, workflow_port):
        self.case_content = yaml.load(open(case_path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)
        self.navigator = NavigatorRequest(federation_token, navigator_protocol, navigator_host, navigator_port)
        self.workflow = WorkflowRequest(federation_token, workflow_protocol, workflow_host, workflow_port)
        self.file_resolve = FileResolve()
        self.taskflow_resolve = TaskflowResolve()

    def _resolve_case(self):
        """
        解析case.yml文件，获取配置信息
        :return:如果case.yml中，各任务流中定义的数量之和与case.yml中定义的总任务流数量不匹配，返回-1，用例定义存在问题；否则返回（文件夹名称，任务流配置定义）
        """
        # 解析case.yml，提取新任务流配置信息
        dir_name = self.case_content.get("dir_name")
        dir_num = self.case_content.get("dir_num")
        taskflow_total = self.case_content.get("taskflow_num")
        taskflow_list_tmp = self.case_content.get("taskflow_message")
        taskflow_list = []
        taskflow_total_tmp = 0
        for item in taskflow_list_tmp:
            taskflow_num = item.get("num")
            taskflow_total_tmp = taskflow_total_tmp + taskflow_num
            print(item.get("cron_conf"))
            taskflow_message = {"num": item.get("num"), "name": item.get("name_pattern"), "cron_conf": item.get("cron_conf"),
                                "schedule_priority": item.get("schedulePriority"), "executor_group_id": item.get("executorGroupId"),
                                "dependLastPolicy": item.get("dependLastPolicy"), "task_list": item.get("task_message")}
            taskflow_list.append(taskflow_message)
        if taskflow_total != taskflow_total_tmp:
            print("任务流总数与实际每种任务流数量之和不匹配！")
            return None, -1, None
        else:
            return dir_name, dir_num, taskflow_list

    def generate(self):
        (dir_name, dir_num, taskflow_list) = self._resolve_case()
        common_taskflow = self.taskflow_resolve.get_common_pattern(taskflow_list)

        dir_list = self.generate_dir(dir_num, dir_name)

        taskflow_uuid_list = []
        for item in common_taskflow:
            num = item["num"]
            taskflow_in_one_dir = num // dir_num  # 一个文件夹内的任务流数量
            taskflow_remain = num % dir_num  # 任务流数量/文件夹数量，无法整除时，计算所得余数，补充建立到最后一个文件夹中
            pattern_path = item["path"]
            base_name = item['name']
            original_pattern = open(pattern_path, 'r', encoding='utf-8').read()
            for i in range(dir_num):
                dir_uuid = dir_list[i]
                taskflow_tmp_num = taskflow_in_one_dir
                if i == 0:
                    taskflow_tmp_num += taskflow_remain
                taskflow_uuid_list_tmp = self.generate_taskflow(original_pattern, base_name, taskflow_tmp_num, dir_uuid)
                taskflow_uuid_list = taskflow_uuid_list + taskflow_uuid_list_tmp

        with open("taskflow_uuid", 'w') as uw:
            uw.write(",".join(taskflow_uuid_list))

        return taskflow_uuid_list

    def generate_dir(self, dir_num, dir_name):
        dir_list = []
        for i in range(dir_num):
            new_dir = dir_name + str(i)
            dir_pattern = self.file_resolve.get_pattern(new_dir, "-", "dir", "WORKFLOW")
            dir_uuid = self.navigator.create_dir(dir_pattern)
            dir_list.append(dir_uuid)
        return dir_list

    def generate_taskflow(self, original_pattern, original_name, taskflow_num, dir_uuid):
        """
        在一个文件夹下创建一定数量的任务流
        :param original_pattern: 任务流模板信息
        :param original_name: 任务流名称
        :param taskflow_num: 任务流数量
        :param dir_uuid: 文件夹uuid
        :return: 创建的任务流的uuid
        """
        taskflow_uuid_list = []
        for i in range(taskflow_num):
            taskflow_name = original_name + str(i)
            file_pattern = self.file_resolve.get_pattern(taskflow_name, dir_uuid, "file", "WORKFLOW")
            file_uuid = self.navigator.create_file(file_pattern)
            target_taskflow = self.taskflow_resolve.replace_message(original_pattern, taskflow_name, file_uuid)
            update_result = self.workflow.update_taskflow(target_taskflow)
            if update_result == 0:
                taskflow_uuid_list.append(file_uuid)
            else:
                exit(-1)
        return taskflow_uuid_list
