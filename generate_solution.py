# -*- coding: utf-8 -*-

import yaml
import json

from library.tdt_request import TDTRequest
from library.connector_request import ConnectorRequest
from library.navigator_request import NavigatorRequest
from pattern.file_pattern.resolve import FileResolve
from pattern.connection_pattern.resolve import ConnectionResolve
from pattern.solution_pattern.resolve import SolutionResolve


class GenerateSolution(object):
    """
    创建数据加载任务
    """
    def __init__(self, case_path, federation_token, access_token, navigator_protocol, navigator_host, navigator_port,
                 connector_protocol,
                 connector_host, connector_port, tdt_protocol, tdt_host, tdt_port):
        self.tdt = TDTRequest(federation_token, tdt_protocol, tdt_host, tdt_port)
        self.access_token = access_token
        self.navigator = NavigatorRequest(federation_token, navigator_protocol, navigator_host, navigator_port)
        self.connector = ConnectorRequest(federation_token, connector_protocol, connector_host, connector_port)
        self.case_content = yaml.load(open(case_path, 'r', encoding='utf-8').read(), Loader=yaml.FullLoader)

        self.file_resolve = FileResolve()
        self.connector_resolve = ConnectionResolve()
        self.solution_resolve = SolutionResolve()

    def _resolve_case(self):
        """
        解析用例文件定义的内容
        :return: 解析获取的用例配置信息
        """
        dir_name = self.case_content.get("dir_name")  # 任务所在文件夹的名称
        solution_num = self.case_content.get("solution_num")  # 任务数量
        solution_name = self.case_content.get("solution_name")  # 数据加载任务名称
        solution_cron = self.case_content.get("solution_cron")

        source_connection_conf = self.case_content.get("connection").get("source_db")  # 源端jdbc连接信息
        target_connection_conf = self.case_content.get("connection").get("target_db")  # 目标库连接信息
        hdfs_connection_conf = self.case_content.get("connection").get("target_hdfs")  # 目标库对应hdfs连接信息

        target_database = self.case_content.get("target_database")

        table_message = self.case_content.get("data")  # 使用的数据表信息
        table_list = []
        table_name_list = table_message.get("table_name")
        for item in table_name_list:
            table = {"catalogName": table_message.get("catalog_name"), "schemaName": table_message.get("schema_name"),
                     "tableName": item}
            table_list.append(table)
        return dir_name, solution_num, solution_name, solution_cron, source_connection_conf, table_list, target_connection_conf, hdfs_connection_conf, target_database

    def generate(self):
        """
        利用解析获取的用例配置信息，创建/获取需要的连接id，创建数据加载任务
        :return:
        """
        (dir_name, solution_num, solution_name, solution_cron, source_connection_conf, table_list, target_connection_conf, hdfs_connection_conf, target_database) = self._resolve_case()
        dir_uuid = self.generate_dir(dir_name)
        source_connection_uuid = self.generate_source_db_connection(source_connection_conf)
        target_connection_uuid = self.generate_target_db_connection(target_connection_conf)
        hdfs_connection_uuid = self.generate_hdfs_connection(hdfs_connection_conf)
        table_num = len(table_list)
        table_num_in_one_solution = table_num // solution_num

        solution_uuid_list = []
        for i in range(solution_num):
            new_solution_name = solution_name + str(i)
            table_list_size = table_num_in_one_solution
            if i == solution_num - 1:
                new_table_list = table_list[i*table_list_size:]
            else:
                new_table_list = table_list[i * table_list_size:(i + 1) * table_list_size]
            solution_uuid = self.generate_solution(dir_uuid, new_solution_name, solution_cron, source_connection_uuid,
                                                   target_connection_uuid, hdfs_connection_uuid, new_table_list,
                                                   target_database)
            solution_uuid_list.append(solution_uuid)
        with open("solution_uuid", 'w') as uw:
            uw.write(",".join(solution_uuid_list))
        return solution_uuid_list

    def generate_solution(self, dir_uuid, solution_name, solution_cron, source_connection_uuid, target_connection_uuid,
                          hdfs_connection_uuid, task_list, target_database):
        file_pattern = self.file_resolve.get_pattern(solution_name, dir_uuid, "file", "DATALOAD")
        print(file_pattern)
        file_uuid = self.navigator.create_file(file_pattern)
        solution_id = self.tdt.get_solution_id(file_uuid)
        table_details = self.tdt.get_table_schema(source_connection_uuid, json.dumps(task_list))
        source_catalogName = task_list[0].get("catalogName")
        source_schemaName = task_list[0].get("schemaName")
        new_solution_pattern = self.solution_resolve.get_jdbc_import_pattern(solution_id, file_uuid, solution_cron,
                                                                             source_connection_uuid,
                                                                             target_connection_uuid,
                                                                             hdfs_connection_uuid, table_details,
                                                                             target_database, source_catalogName,
                                                                             source_schemaName)
        add_result = self.tdt.update_solution(new_solution_pattern)
        if add_result == 0:
            return file_uuid
        else:
            exit(-1)

    def generate_source_db_connection(self, connection_conf):
        """
        利用名称获取jdbc连接的uuid，若不存在则创建
        :param connection_conf: jdbc连接配置信息
        :return: 连接uuid
        """
        connection_type = [connection_conf.get("type")]
        connection_name = connection_conf.get("name")
        driver_version = connection_conf.get("driver_version")
        connection_uuid = self.connector.get_datasource_message(connection_type, connection_name)
        if connection_uuid is None:
            connection_driver_uuid = self.connector.get_driver_message(connection_type, driver_version)
            if connection_driver_uuid is None:
                exit(-1)
            connection_conf["driver_uuid"] = connection_driver_uuid
            connection_pattern = self.connector_resolve.resolve_case_source_connection(connection_conf)
            valid_result = self.connector.valid_datasource(connection_pattern)
            if valid_result != 0:
                exit(-1)
            new_connection_uuid = self.connector.add_datasource(connection_pattern)
            if new_connection_uuid is None:
                exit(-1)
            return new_connection_uuid
        else:
            return connection_uuid

    def generate_target_db_connection(self, connection_conf):
        """
        利用名称获取inceptor、argodb连接的uuid，若不存在则创建
        :param connection_conf: inceptor、argodb连接配置信息
        :return: 连接uuid
        """
        connection_type = [connection_conf.get("type")]
        connection_name = connection_conf.get("name")
        driver_version = connection_conf.get("driver_version")
        connection_conf["access_token"] = self.access_token
        connection_uuid = self.connector.get_datasource_message(connection_type, connection_name)
        if connection_uuid is None:
            connection_driver_uuid = self.connector.get_driver_message(connection_type, driver_version)
            if connection_driver_uuid is None:
                exit(-1)
            connection_conf["driver_uuid"] = connection_driver_uuid
            connection_pattern = self.connector_resolve.resolve_case_target_connection(connection_conf)
            valid_result = self.connector.valid_datasource(connection_pattern)
            if valid_result != 0:
                exit(-1)
            new_connection_uuid = self.connector.add_datasource(connection_pattern)
            if new_connection_uuid is None:
                exit(-1)
            return new_connection_uuid
        else:
            return connection_uuid

    def generate_hdfs_connection(self, connection_conf):
        connection_type = [connection_conf.get("type")]
        connection_name = connection_conf.get("name")
        connection_uuid = self.connector.get_datasource_message(connection_type, connection_name)
        if connection_uuid is None:
            connection_pattern = self.connector_resolve.resolve_case_hdfs_connection(connection_conf)
            valid_result = self.connector.valid_datasource(connection_pattern)
            if valid_result != 0:
                exit(-1)
            new_connection_uuid = self.connector.add_datasource(connection_pattern)
            if new_connection_uuid is None:
                exit(-1)
            return new_connection_uuid
        else:
            return connection_uuid

    def generate_dir(self, dir_name):
        new_dir = dir_name
        dir_pattern = self.file_resolve.get_pattern(new_dir, "-", "dir", "DATALOAD")
        dir_uuid = self.navigator.create_dir(dir_pattern)
        return dir_uuid
