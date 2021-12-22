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


class MidgardResolve(object):
    """
    获取创建任务流请求信息
    """

    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.midgard_pattern_root = os.path.join(root_path, 'pattern', 'midgard_pattern')

    def replace_api_message(self, pattern_file, target_name, target_id, datasource_id):
        """
        替换API模板中的id、name、数据源id信息
        :param pattern_file: 使用的模板文件名称
        :param target_name: 新建的API的名称
        :param target_id: 新建的API文件的uuid
        :param datasource_id: 使用的数据源的uuid
        :return: 新建的API的配置
        """
        pattern_path = os.path.join(self.midgard_pattern_root, pattern_file)
        api_pattern = json.loads(open(pattern_path, encoding='utf-8').read())
        new_base_info = _combine_dic_data({"name": target_name}, api_pattern['baseInfo'])
        new_develop_config = _combine_dic_data({"dataSourceId": datasource_id, "upstreamId": target_id},
                                               api_pattern['developConfig'])
        new_content = {"baseInfo": new_base_info, "developConfig": new_develop_config, "id": target_id}
        target_api = _combine_dic_data(new_content, api_pattern)
        return json.dumps(target_api)

    def replace_route_message(self, pattern_file, api_id, route_name, dynamic_host, route_path):
        """
        为API增加路由，生成路由信息
        :param pattern_file: 路由配置模板文件名称，需要在pattern/midgard_pattern文件夹下
        :param api_id: 这个路由为哪个API配置，这个API的ID
        :param route_name: 路由名称，这里就直接使用API名称（暂时一个API给一个路由）
        :param dynamic_path: 动态路由地址，根据集群信息填写，需要hostname
        :param route_path: API调用访问url
        :return: 添加路由需要的配置信息
        """
        pattern_path = os.path.join(self.midgard_pattern_root, pattern_file)
        route_pattern = json.loads(open(pattern_path, encoding='utf-8').read())
        target_route = _combine_dic_data({"apiId": api_id, "name": route_name, "host": dynamic_host,
                                          "path": route_path}, route_pattern)
        return json.dumps(target_route)

    def replace_online_version_message(self, pattern_file):
        """
        API管理中，上线API时配置的上线模式
        :return:
        """
        pattern_path = os.path.join(self.midgard_pattern_root, pattern_file)
        return open(pattern_path, encoding='utf-8').read()
