# -*- coding: utf-8 -*-

import requests
import json
from .utils import authorization_headers


class ConnectorRequest(object):
    """
    连接管理相关api
    """
    def __init__(self, federation_token, protocol, host, port):
        self.connector_session = requests.Session()
        self.connector_session.headers = authorization_headers(service_token=federation_token)
        self.connector_url = protocol + "://" + host + ":" + str(port)
        if protocol == 'https':
            self.connector_session.verify = False

    def get_driver_message(self, connection_type, connection_version):
        api = self.connector_url + "/studio/api/connector/v1/driver"
        print("请求地址：", api)
        connection_message = {"connectionType": connection_type}
        response = self.connector_session.get(api, params=connection_message)
        if response.status_code == 200:
            driver_list = json.loads(response.text)
            for item in driver_list:
                if item['connectionVersion'] == connection_version:
                    print("db driver uuid: ", item['uuid'])
                    return item['uuid']
            print(connection_type, "没有所需要的版本驱动，请先上传驱动")
            return None
        else:
            print("获取驱动信息失败，", response.text)
            return None

    def get_datasource_message(self, connection_types, connection_name):
        api = self.connector_url + "/studio/api/connector/v1/query/datasource"
        print("请求地址：", api)
        datasource_info = {"connectionTypes": connection_types}
        response = self.connector_session.post(api, data=json.dumps(datasource_info))
        if response.status_code == 200:
            datasource_list = json.loads(response.text)['data']
            for item in datasource_list:
                if item['name'] == connection_name:
                    print("selected datasource ", connection_name, "'s uuid is ", item['uuid'])
                    return item['uuid']
            print("连接", connection_name, "不存在，创建数据源")
            return None
        else:
            print("获取数据源信息失败，", response.text)
            return None

    def valid_datasource(self, datasource_message):
        api = self.connector_url + "/studio/api/connector/v1/query/datasource/valid"
        print("请求地址：", api)
        response = self.connector_session.post(api, data=datasource_message)
        if response.status_code == 200:
            print("数据源正常可用")
            return 0
        else:
            print("数据源信息异常")
            print(datasource_message)
            print(response.text)
            return -1

    def add_datasource(self, datasource_message):
        api = self.connector_url + "/studio/api/connector/v1/mgmt"
        print("请求地址：", api)
        response = self.connector_session.post(api, data=datasource_message)
        if response.status_code == 200:
            print("新增数据源成功")
            return json.loads(response.text)["uuid"]
        else:
            error_message = json.loads(response.text)
            if error_message["name"] == "exception.RESOURCE_ALREADY_EXISTS":
                return error_message["resource"]
            else:
                print("新增或获取相同连接数据源失败")
                print(json.dumps(error_message))
                return None
