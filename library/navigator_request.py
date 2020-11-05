# -*- coding: utf-8 -*-

import requests
import json
from .utils import authorization_headers


class NavigatorRequest(object):
    """
    目录树api操作，包括创建文件夹、创建文件
    """
    def __init__(self, federation_token, protocol, host, port):
        self.navigator_session = requests.Session()
        self.navigator_session.headers = authorization_headers(federation_token=federation_token)
        self.navigator_url = protocol + "://" + host + ":" + str(port)
        if protocol == 'https':
            self.navigator_session.verify = False

    def create_dir(self, dir_message):
        api = self.navigator_url + "/studio/api/navigator/v1/common/newDir"
        response = self.navigator_session.post(api, data=dir_message)
        if response.status_code == 200:
            new_dir_message = json.loads(response.text)
            new_dir_uuid = new_dir_message['uuid']
            print("成功创建文件夹，文件夹uuid: ", new_dir_uuid)
            return new_dir_uuid
        else:
            print("创建文件夹失败， 报错信息： ", response.text)
            return None

    def create_file(self, file_message):
        api = self.navigator_url + "/studio/api/navigator/v1/common/newFile"
        response = self.navigator_session.post(api, data=file_message)
        if response.status_code == 200:
            new_dir_message = json.loads(response.text)
            new_dir_uuid = new_dir_message['uuid']
            print("成功创建文件，文件uuid: ", new_dir_uuid)
            return new_dir_uuid
        else:
            print("创建文件失败， 报错信息： ", response.text)
            return None
