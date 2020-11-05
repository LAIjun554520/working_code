# -*- coding: utf-8 -*-


import requests
from .utils import authorization_headers
import json


class TDTRequest(object):
    """
    tdt api
    """
    def __init__(self, federation_token, protocol, host, port):
        federation_token = federation_token
        self.tdt_url = protocol + "://" + host + ":" + port
        self.tdt_session = requests.Session()
        self.tdt_session.headers = authorization_headers(federation_token=federation_token)
        if protocol == "https":
            self.tdt_session.verify = False

    def get_table_schema(self, connection_uuid, db_structures):
        api = self.tdt_url + "/studio/api/tdt/v1/db/schemas"
        connection = {"connectionUuId": connection_uuid}
        response = self.tdt_session.post(api, params=connection, data=db_structures)
        if response.status_code == 200:
            print("已获取数据表信息")
            return json.loads(response.text)["responseObject"]
        else:
            print("获取数据表信息失败， status_code: ", response.status_code)
            print(response.text)
            return None

    def get_solution_id(self, file_uuid):
        api = self.tdt_url + "/studio/api/tdt/v1/solution/" + file_uuid
        response = self.tdt_session.get(api)
        if response.status_code == 200:
            solution_id = json.loads(response.text)["responseObject"]["id"]
            print("新建任务id：", solution_id)
            return solution_id
        else:
            print("创建数据流转任务失败：", file_uuid)
            return -1

    def update_solution(self, solution_message):
        api = self.tdt_url + "/studio/api/tdt/v1/solution"
        response = self.tdt_session.put(api, data=solution_message)
        if response.status_code == 200:
            print("成功更新任务：", json.loads(solution_message)["uniqueId"])
            return 0
        else:
            print("更新任务失败：", json.loads(solution_message)["uniqueId"])
            return -1

    def online_solution(self, solution_uuid_list):
        api = self.tdt_url + "/studio/api/tdt/v1/solution/submit"
        solution_uuids = {"uuids": solution_uuid_list}
        response = self.tdt_session.post(api, data=json.dumps(solution_uuids))
        if response.status_code == 200:
            print("任务已发布：", ",".join(solution_uuid_list))
            return 0
        else:
            print("任务发布失败：", ",".join(solution_uuid_list))
            return -1

    def offline_solution(self, solution_uuid_list):
        api = self.tdt_url + "/studio/api/tdt/v1/solution/offline"
        solution_uuids = {"uuids": solution_uuid_list}
        response = self.tdt_session.post(api, data=json.dumps(solution_uuids))
        if response.status_code == 200:
            print("任务已下线：", ",".join(solution_uuid_list))
            return 0
        else:
            print("任务下线失败：", ",".join(solution_uuid_list))
            return -1
