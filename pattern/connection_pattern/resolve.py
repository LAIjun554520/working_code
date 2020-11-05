# -*- coding: utf-8 -*-


import json
import base64


class ConnectionResolve(object):
    """
    解析创建连接的模板
    """
    def __init__(self):
        pass

    def resolve_case_source_connection(self, connection_message):
        """
        将用例中定义的源端jdbc连接信息整理成创建连接所需要的格式
        :param connection_message: 从用例文件中解析获取的源端jdbc连接配置信息
        :return: 整理后可用于创建连接的信息
        """
        connection_new = {"connectionType": connection_message["type"], "name": connection_message["name"],
                              "driverUuid": connection_message["driver_uuid"], "connection": connection_message["connection"]}
        connection_auth_infos = {"USERNAME": connection_message["username"], "PASSWORD": connection_message["password"]}
        connection_new["authInfos"] = connection_auth_infos
        connection_new["connectionArgs"] = {}
        connection_new["authType"] = "PASSWORD"
        return json.dumps(connection_new)

    def resolve_case_target_connection(self, connection_message):
        """
        将用例中定义的目标库连接信息整理成创建连接所需要的格式
        :param connection_message: 从用例文件中解析获取的目标库连接配置信息
        :return: 整理后看可以用于创建连接的信息
        """
        connection_new = {"connectionType": connection_message["type"], "name": connection_message["name"],
                              "driverUuid": connection_message["driver_uuid"], "connection": connection_message["connection"]}
        connection_auth_infos = {"ACCESS_TOKEN": connection_message["access_token"]}
        connection_new['authInfos'] = connection_auth_infos
        connection_new["connectionArgs"] = {}
        connection_new["authType"] = "ACCESS_TOKEN"
        return json.dumps(connection_new)

    def resolve_case_hdfs_connection(self, connection_message):
        """
        将用例中定义的hdfs连接信息整理成创建连接所需要的格式
        :param connection_message: 从用例文件中解析获取的hdfs连接配置信息
        :return: 整理后可以用于创建连接的信息
        """
        connection_new = {"connectionType": connection_message["type"], "name": connection_message["name"],
                          "connection": connection_message["connection"], "driverUuid": ""}
        keytab_path = connection_message["user_keytab"]
        keytab_content = str(base64.b64encode(open(keytab_path, 'rb').read())).strip("b").strip("'")
        print(keytab_content)
        connection_auth_infos = {"PRINCIPAL": connection_message["user_principal"],
                                 "KEYTAB": keytab_content}
        connection_new["authInfos"] = connection_auth_infos
        hdfs_site_path = connection_message["hdfs_site"]
        core_site_path = connection_message["core_site"]
        hdfs_site_content = open(hdfs_site_path, 'r').read().strip().replace('\n', '')
        core_site_content = open(core_site_path, 'r').read().strip().replace('\n', '')
        connection_args = {"HDFS_SITE": hdfs_site_content, "CORE_SITE": core_site_content}
        connection_new["connectionArgs"] = connection_args
        connection_new["schema"] = ["/"]
        connection_new["authType"] = "KERBEROS"
        return json.dumps(connection_new)
