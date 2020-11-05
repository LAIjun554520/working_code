# -*- coding: utf-8 -*-


import json
import os


class FileResolve(object):
    """
    解析获取待创建的文件夹、文件模板
    """
    def __init__(self):
        dir_base_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dir.json")
        file_base_pattern_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file.json")
        self.base_dir = json.loads(open(dir_base_pattern_path, 'r').read())
        self.base_file = json.loads(open(file_base_pattern_path, 'r').read())

    def get_pattern(self, name, parent_uuid, file_type, task_type):
        """
        获取用于建立文件或文件夹的信息
        :param name: 文件/文件夹名称
        :param parent_uuid: 父目录uuid，某类型下根目录，parent_uuid为“-”
        :param file_type: 文件 file 还是文件夹 dir
        :param task_type: 待创建的目录/文件夹对应的任务类型，如WORKFLOW或DATALOAD
        :return:
        """
        new_message = {"name": name, "parentUUID": parent_uuid, "category": task_type, "type": task_type}
        if file_type == "dir":
            pattern = self.base_dir
        elif file_type == "file":
            pattern = self.base_file
        else:
            print("待获取的模版应该是文件夹或文件，需要重新输入!")
            return -1
        for key in new_message:
            pattern[key] = new_message[key]
        return json.dumps(pattern)

    def replace_name(self, original_pattern_path, name_number):
        pass

    def replace_parent_uuid(self, original_pattern, target_uuid):
        pass
