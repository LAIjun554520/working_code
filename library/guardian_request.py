# -*- coding: utf-8 -*-
from time import sleep

import paramiko
import re
import requests
import json

from .utils import default_headers


def _get_federation_server(manager_ip, cluster_root_pass):
    """
    获取federation server的所有节点
    :param manager_ip: manager地址
    :param cluster_root_pass: 集群root密码
    :return: federation server所有节点
    """
    myclient = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    myclient.set_missing_host_key_policy(key)

    # 获取federation server所在的所有节点
    myclient.connect(manager_ip, 22, "root", cluster_root_pass)
    print(manager_ip)
    stdin, stdout, stderr = myclient.exec_command("kubectl -s https://127.0.0.1:6443 "
                                                  "--certificate-authority=/srv/kubernetes/ca.pem "
                                                  "--client-certificate=/srv/kubernetes/admin.pem  "
                                                  "--client-key=/srv/kubernetes/admin-key.pem get po -owide | grep "
                                                  "guardian-federation")
    federation_message = stdout.read().decode('utf-8')
    message_list = federation_message.strip("\n").split("\n")
    federation_list = []
    for item in message_list:
        message = re.sub(" +", " ", item)
        federation_ip = message.split(" ")[5]
        federation_list.append(federation_ip)
    myclient.close()
    return federation_list


def _get_guardian_server(manager_ip, cluster_root_pass):
    """
    获取guardian server的一个节点
    :param manager_ip: manager地址
    :param cluster_root_pass: 集群root密码
    :return: guardian server的一个节点
    """
    myclient = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    myclient.set_missing_host_key_policy(key)

    # 获取federation server所在的所有节点
    myclient.connect(manager_ip, 22, "root", cluster_root_pass)
    print(manager_ip)
    stdin, stdout, stderr = myclient.exec_command("kubectl -s https://127.0.0.1:6443 "
                                                  "--certificate-authority=/srv/kubernetes/ca.pem "
                                                  "--client-certificate=/srv/kubernetes/admin.pem  "
                                                  "--client-key=/srv/kubernetes/admin-key.pem get po -owide | grep "
                                                  "guardian-server")
    guardian_message = stdout.read().decode('utf-8')
    message_list = guardian_message.strip("\n").split("\n")
    guardian_server_ip = re.sub(" +", " ", message_list[0]).split(" ")[5]
    myclient.close()
    return guardian_server_ip


def _check_catpcha(federation_list, cluster_root_pass):
    myclient = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    myclient.set_missing_host_key_policy(key)
    for item in federation_list:
        myclient.connect(item, 22, "root", cluster_root_pass)
        stdin, stdout, stderr = myclient.exec_command("grep guardian.federation.service.captcha.enabled=false "
                                                      "/etc/federation/conf/application.properties")
        return_message = stdout.read().decode('utf-8').strip(" ").strip("\n")
        if return_message == "guardian.federation.service.captcha.enabled=false":
            print("federation 登录验证码已关闭")
            return False
        else:
            print("federation 登录验证码未关闭，需要关闭验证码")
            return True


def _close_federation_captcha(manager_ip, cluster_root_pass, federation_list, manager_username, manager_password):
    # 修改federation所有节点服务的配置，关闭captcha验证
    myclient = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    myclient.set_missing_host_key_policy(key)
    for item in federation_list:
        myclient.connect(item, 22, "root", cluster_root_pass)
        federation_stdin, federation_stdout, federation_stderr = myclient.exec_command(
            "N=`grep -n guardian.federation.service.captcha.enabled /etc/federation/conf/application.properties | awk "
            "-F "
            ": '{print $1}'`;sed -i \"${N}c guardian.federation.service.captcha.enabled=false\" "
            "/etc/federation/conf/application.properties;N1=`grep -n FEDERATION_SERVICE_CAPTCHA_ENABLED "
            "/etc/federation/conf/federation-env.sh |awk -F : '{print $1}'`;sed -i \"${N1}c export "
            "FEDERATION_SERVICE_CAPTCHA_ENABLED=false\" /etc/federation/conf/federation-env.sh")
        sleep(90)
        print("close federation login verify, ip ", item)
        for i in federation_stdout.readlines():
            print(i)
        sleep(2)

    # 获取guardian服务id
    manager_login_api = "http://" + manager_ip + ":8180/api/users/login"
    print(manager_login_api)
    data = {
        "userName": manager_username,
        "userPassword": manager_password
    }
    header = {
        "Content-Type": "application/json"
    }
    manager_session = requests.Session()
    login_re = manager_session.post(manager_login_api, data=json.dumps(data), headers=header, verify=False)
    if login_re.status_code == 200:
        print("login manager successful")
    else:
        print("login manager failed")
        exit()
    # get service id
    server_list_api = "http://" + manager_ip + ":8180/api/services?global=true"
    conf_re = manager_session.get(server_list_api)
    conf_dict = conf_re.json()
    guardian_id = -1
    # for op in conf_dict:
    for op in conf_dict:
        # print(op["type"])
        if "GUARDIAN" in op['type']:
            guardian_id_dic = op
            print(guardian_id_dic["id"])
            guardian_id = guardian_id_dic["id"]
            # print(type(str(guardian_id)))
    if guardian_id == -1:
        print("获取guardian服务id失败")
        exit(-1)

    # restart guardian server
    restart_guardian_api = "http://" + manager_ip + ":8180/api/services/" + str(guardian_id) + "/operations/restart"
    data_guardian = {
        "rolling": "false"
    }
    restart_guardian_re = manager_session.post(restart_guardian_api, data=json.dumps(data_guardian), headers=header,
                                               verify=False)
    restart_guardian_dict = restart_guardian_re.json()
    print(restart_guardian_dict)
    print(restart_guardian_re.status_code)
    waiting_guardian_api = "http://" + manager_ip + ":8180/api/operations/jobs/" + str(restart_guardian_dict["id"])
    if restart_guardian_re.status_code == 202:
        for server_time in range(40):
            waiting_re = manager_session.get(waiting_guardian_api)
            waiting_list = waiting_re.json()
            print(waiting_list["status"])
            if "SUCCESSFUL" == waiting_list["status"]:
                print("restart guardian successful")
                break
            else:
                print("please waiting restart")
            sleep(60)
    else:
        print("restart guardian failed,please check it")
        exit(-1)


class GuardianRequest(object):
    """
    federation 操作，创建、获取federation token
    """

    def __init__(self, manager_ip, cluster_root_pass, manager_username, manager_password, username,
                 password, tenant):
        federation_list = _get_federation_server(manager_ip, cluster_root_pass)
        guardian_server = _get_guardian_server(manager_ip, cluster_root_pass)
        captcha_status = _check_catpcha(federation_list, cluster_root_pass)
        if captcha_status:
            _close_federation_captcha(manager_ip, cluster_root_pass, federation_list,
                                      manager_username, manager_password)
        self.federation_url = "https://" + federation_list[0] + ":8383/federation-server"
        self.guardian_url = "https://" + guardian_server + ":8380"
        self.guardian_session = requests.Session()
        self.guardian_session.headers = default_headers()
        self.guardian_session.verify = False
        self.federation_session = requests.Session()
        self.federation_session.headers = default_headers()
        self.federation_session.verify = False
        self.tenant = tenant
        self.username = username
        self.password = password

    def _login(self):
        login_message = {"tenant": self.tenant, "username": self.username, "password": self.password}
        login_api = self.federation_url + "/api/v1/login"
        response = self.federation_session.post(login_api, data=json.dumps(login_message))
        if response.status_code != 200:
            print("login fail, ", response.text)
            exit(-1)
        response = self.guardian_session.post(login_api, data=json.dumps(login_message))
        if response.status_code != 200:
            print("login fail, ", response.text)
            exit(-1)

    def get_access_token(self):
        self._login()
        get_access_token_api = self.guardian_url + "/api/v1/accessToken"
        create_access_token_api = self.guardian_url + "/api/v1/accessToken"
        params = {"owner": self.username}
        response = self.guardian_session.get(get_access_token_api, params=params)
        if response.status_code == 200:
            access_token_list = json.loads(response.text)
            for item in access_token_list:
                name = item["name"]
                if name == 'studio_performance':
                    return item
            new_token_message = {"name": "studio_performance", "expiredTime": "0001-01-01T00:00:00"}
            new_token_response = self.guardian_session.post(create_access_token_api, data=json.dumps(new_token_message))
            if new_token_response.status_code == 200:
                new_access_token = json.loads(new_token_response.text)["content"]
                print("成功创建access token studio_performance: ", new_access_token)
                return new_access_token
            else:
                print("创建access token失败，",new_token_response.text)
                return None

    def get_federation_token(self):
        self._login()
        get_federation_token_api = self.federation_url + "/api/v1/tokens"
        create_federation_token_api = self.federation_url + "/api/v1/tokens"
        refresh_token_api = self.federation_url + "/api/v1/token-refresh-tasks"
        params = {"sorting": "true", "pageSize": 10, "pageNumber": 1, "withTokenRefreshTask": "true",
                  "tokenSource": "USER", "searchValue": "studio-performance"}
        response = self.federation_session.get(get_federation_token_api, params=params)
        if response.status_code != 200:
            print("获取federation token失败: ", response.text)
            return None
        federation_token_message = json.loads(response.text)
        search_token_num = federation_token_message["itemCount"]
        if search_token_num == 0:
            print("创建federation token")
            new_token_message = {"name": "studio-performance", "validitySeconds": 43200,
                                 "refreshToken": {"validitySeconds": "null"}}
            new_token_response = self.federation_session.post(create_federation_token_api,
                                                              data=json.dumps(new_token_message))
            if new_token_response.status_code == 200:
                new_federation_message = json.loads(new_token_response.text)
                new_federation_token = new_federation_message["value"]
                print("成功创建federation token studio-performance: ", new_federation_token)
                refresh_token = new_federation_message["refreshToken"]["value"]
                refresh_message = {"status": "SCHEDULED", "refreshTokenValue": refresh_token,
                                   "executionInterval": 21600}
                refresh_response = self.federation_session.post(refresh_token_api, data=json.dumps(refresh_message))
                if refresh_response.status_code == 200:
                    print("成功开启自动刷新")
                    return new_federation_token
                else:
                    print("开启自动刷新失败，", refresh_response.text)
                    return None
            else:
                print("创建federation token失败，", new_token_response.text)
                return None
        else:
            target_token_refresh_status = federation_token_message["body"][0]["task"]["status"]
            exists_federation_token = federation_token_message["body"][0]["value"]
            exists_refresh_token = federation_token_message["body"][0]["refreshToken"]["value"]
            if target_token_refresh_status == "SCHEDULED":
                print("federation token studio-performance 已存在：", exists_federation_token)
                return exists_federation_token
            else:
                exists_refresh_message = {"status": "SCHEDULED", "refreshTokenValue": exists_refresh_token,
                                          "executionInterval": 21600}
                exists_refresh_response = self.federation_session.post(refresh_token_api,
                                                                       data=json.dumps(exists_refresh_message))
                if exists_refresh_response.status_code == 200:
                    print("成功开启自动刷新")
                    return exists_federation_token
                else:
                    print("开启自动刷新失败，", exists_refresh_response.text)
                    return None
