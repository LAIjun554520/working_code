# -*- coding: utf-8 -*-


import json
import os


def _combine_dic_data(new_info, old_info):
    result = {}
    for key in old_info:
        result[key] = old_info[key]
    for key in new_info:
        result[key] = new_info[key]
    return result


class TaskflowResolve(object):
    """
    获取创建任务流请求信息
    """

    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        pattern_tmp = os.path.join(root_path, "pattern_tmp")
        if not os.path.exists(pattern_tmp):
            os.mkdir(pattern_tmp)
        self.tmp_path = pattern_tmp
        base_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "base_pattern.json")
        self.base_taskflow = json.loads(open(base_pattern_path, 'r').read())

    def get_common_pattern(self, taskflow_list):
        """
        将用例文件中定义的任务流配置信息替换基础模板，得到此次用例执行使用的模板文件
        :param taskflow_list: 用例文件中定义的任务流配置信息
        :return: 利用用例文件中定义的任务流配置信息替换基础模板文件之后，生成的模板文件路径及该配置下任务流的数量
        """
        # 利用case.yml中定义的信息替换基础模板信息
        common_pattern_list = []
        for taskflow in taskflow_list:
            taskflow_name = taskflow["name"]
            pattern_file_name = taskflow_name + ".json"
            common_pattern_path = os.path.join(self.tmp_path, pattern_file_name)  # 生成的模板文件路径

            # 利用用例配置信息替换基础模板配置
            taskflow_cron_conf = taskflow["cron_conf"]
            taskflow_basic_new = {"name": taskflow_name, "cronType": taskflow_cron_conf["cron_type"],
                                  "schedulePriority": taskflow["schedule_priority"],
                                  "executorGroupId": taskflow["executor_group_id"]}
            taskflow_conf_new = {"cronPattern": taskflow_cron_conf["cron_Pattern"],
                                 "cronHour": taskflow_cron_conf["cron_Hour"],
                                 "cronMinute": taskflow_cron_conf["cron_Minute"],
                                 "dependLastPolicy": taskflow["dependLastPolicy"]}

            taskflow_task_list = taskflow["task_list"]
            taskflow_custom_pattern = taskflow["custom_pattern"]

            if taskflow_task_list != " " and taskflow_custom_pattern == " ":
                # 获取作为基本模板的sample.json的配置信息（待替换）
                base_flow_message = self.base_taskflow["flow"]
                base_flow_configuration = base_flow_message["configuration"]
                base_task_message = self.base_taskflow["tasks"][0]

                # 获取新任务配置list
                task_list_new = []
                task_count = 0
                for task in taskflow_task_list:
                    task_num = task["num"]
                    for i in range(task_num):
                        task_new = {"taskType": task["type"], "execSpec": task["execSpec"]}
                        task_name = task["name_pattern"]
                        task_new["name"] = task_name + str(i)
                        task_new["id"] = task_count
                        task_count += 1
                        task_list_new.append(task_new)
                result_task_list = []
                for task in task_list_new:
                    task_execSpec_new = _combine_dic_data(task["execSpec"], base_task_message["execSpec"])
                    task["execSpec"] = task_execSpec_new
                    result_task = _combine_dic_data(task, base_task_message)
                    result_task_list.append(result_task)

                result_taskflow_configuration = _combine_dic_data(taskflow_conf_new, base_flow_configuration)
                taskflow_basic_new["configuration"] = result_taskflow_configuration
                result_taskflow_message = _combine_dic_data(taskflow_basic_new, base_flow_message)
                pattern_new = {"flow": result_taskflow_message, "tasks": result_task_list}
                result_pattern = _combine_dic_data(pattern_new, self.base_taskflow)
            elif taskflow_task_list == " " and taskflow_custom_pattern != " ":
                # 获取使用的模板
                custom_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "firm_pattern",
                                                   taskflow_custom_pattern)
                custom_firm_taskflow = json.loads(open(custom_pattern_path, 'r').read())
                custom_firm_flow_message = custom_firm_taskflow["flow"]
                custom_firm_flow_configuration = custom_firm_flow_message["configuration"]
                custom_firm_task_message = custom_firm_taskflow["tasks"]
                result_taskflow_configuration = _combine_dic_data(taskflow_conf_new, custom_firm_flow_configuration)
                taskflow_basic_new["configuration"] = result_taskflow_configuration
                result_taskflow_message = _combine_dic_data(taskflow_basic_new, custom_firm_flow_message)
                pattern_new = {"flow": result_taskflow_message, "tasks": custom_firm_task_message}
                result_pattern = _combine_dic_data(pattern_new, custom_firm_taskflow)
                print(result_pattern)

            with open(common_pattern_path, 'w') as wp:
                wp.write(json.dumps(result_pattern))
            item = {"num": taskflow["num"], "name": taskflow_name, "path": common_pattern_path}
            common_pattern_list.append(item)

        return common_pattern_list

    def replace_message(self, original_taskflow, target_name, target_id, preDependencies):
        """
        替换模版中的任务流的名称及id，得到用于生成任务流的模板
        :param original_taskflow: 解析用例配置得到的模板文件的路径
        :param target_name: 新生成的任务流的具体名称
        :param target_id: 新生成的任务流的id
        :param preDependencies: 上游任务流信息（如果有）
        :return: 用于生成任务流的信息
        """
        original_taskflow = json.loads(original_taskflow)
        original_taskflowflow_message = original_taskflow["flow"]
        original_task_list = original_taskflow["tasks"]
        target_taskflow_message = _combine_dic_data({"name": target_name, "id": target_id},
                                                    original_taskflowflow_message)
        target_task_list = []
        for task in original_task_list:
            target_task = _combine_dic_data({"parentFlowId": target_id}, task)
            print(type(task))
            target_task_list.append(target_task)
        target_taskflow = {"flow": target_taskflow_message, "tasks": target_task_list}
        if preDependencies is not None:
            target_taskflow = {"flow": target_taskflow_message, "tasks": target_task_list,
                               "preDependencies": preDependencies}
        result_taskflow = json.dumps(_combine_dic_data(target_taskflow, original_taskflow))
        return result_taskflow
