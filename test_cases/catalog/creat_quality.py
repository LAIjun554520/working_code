import json
import random
import string
import requests
requests.packages.urllib3.disable_warnings()


quality_endpoint = 'https://172.22.6.79:28100'        # catalog standard url
navigator_endpoint = 'https://172.22.6.61:28183'       # foundation navigator url
federation_token = 'VtB47TGiBQ5dmc8Q3mJP-TDH'          # Guardian Federation Server的自定义token

headers = {
    'authorization': 'bearer ' + federation_token,
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*'
}

def get_random_by_length(length: int = 10) -> str:
    """
    随机生成指定位数的字符串
    :param length: 长度
    :return: 生成的随机字符串
    """
    # 0123456789 + abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    base_char_str = string.digits + string.ascii_letters
    random_str = ''.join(random.choices(population=base_char_str, k=length))
    return random_str

class NavigatorApi():
    def __init__(self, navigator_endpoint):
        self.navigator_endpoint = navigator_endpoint

    def creat_file(self, payload):
        '''
        navigator 创建文件接口
        :param payload: {
	                        "category": "STANDARD_BASIC",
	                        "name": "test1",
                            "parentUUID": "66ac4dba50374b969da90a864c58fa58",
                            "type": "STANDARD_BASIC",
                            "nodeType": "FILE"
                        }
        :return: response
        '''
        api = '/studio/api/navigator/v1/common/newFile'
        url = '{endpoint}{api}'.format(endpoint=self.navigator_endpoint, api=api)
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        # print(response.text)
        # print(response.status_code)
        return response

    def paste_file(self, payload):
        '''
        navigator 粘贴任意类型文件接口，如：标准、质量、调度、集成文件......
        :param payload: {
                            "uuidList":["1c7c53cbe38a4481aa699dbffd4d3ed1"],
                            "parentUUID":"4ee064bfe5684b06adaf120167121bdc"
                        }
        :return: response
        '''
        api = '/studio/api/navigator/v1/common/paste'
        url = '{endpoint}{api}'.format(endpoint=self.navigator_endpoint, api=api)
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        # print(response.text)
        # print(response.status_code)
        return response


class QualityApi():
    def __init__(self, navigator_endpoint, quality_endpoint):
        """
        类初始化
        :param url: 测试环境地址，http://172.22.6.28:18141
        """
        self.quality_endpoint = quality_endpoint
        self.navigator_endpoint = navigator_endpoint

    def paste_quality(self, payload):
        """
        粘贴质量规则、质量模板、质量任务文件
        :param payload: 字典类型,{
                                    "uuidList":["1c7c53cbe38a4481aa699dbffd4d3ed1"],
                                    "parentUUID":"4ee064bfe5684b06adaf120167121bdc"
                                  }
        :return:
        """
        navigitorApi = NavigatorApi(self.navigator_endpoint)
        response = navigitorApi.paste_file(payload=payload)
        # status_code = response.status_code
        return response

    def creat_quality_rule(self, payload):
        """
        粘贴质量规则、质量模板、质量任务文件
        :param payload: 字典类型,{
                                    "ruleGroups": [
                                        {
                                            "id": 1,
                                            "name": "te"
                                        }
                                    ],
                                    "parameters": [
                                        {
                                            "name": "table_a",
                                            "type": "TABLE",
                                            "description": "test",
                                            "value": "zyl.table1"
                                        }
                                    ],
                                    "ruleGroupIds": [
                                        1
                                    ],
                                    "ruleName": "tt",
                                    "description": "tsdfats",
                                    "templateUuid": "40a3235314d3449490bb0fccadb5139e",
                                    "templateName": "非空检查",
                                    "templateDesc": "testssss",
                                    "templateContent": "SELECT COUNT(1) FROM ${table_a}",
                                    "datasourceUuid": "69e352a132984aa38e9e48eaa317f8e9",
                                    "datasourceName": "inceptor660"
                                 }
        :return:
        """
        api = '/studio/api/quality/v1/rule/save'
        url = '{endpoint}{api}'.format(endpoint=self.quality_endpoint, api=api)
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload), verify=False)
        # print(response.text)
        # print(response.status_code)
        return response
class QualityTestCase():
    def __init__(self,navigator_endpoint, quality_endpoint):
        self.qualityApi = QualityApi(navigator_endpoint=navigator_endpoint, quality_endpoint=quality_endpoint)

    def paste_quality_file(self,parent_uuid, file_uuid) -> dict:
        # 粘贴质量文件，可以是质量模板、质量任务
        payload = {"uuidList":[file_uuid],
                   "parentUUID":parent_uuid
                   }

        response = self.qualityApi.paste_quality(payload=payload)
        return response

    def creat_quality_rule(self,payload) -> dict:
        # 粘贴质量文件，可以是质量模板、质量规则、质量任务
        response = self.qualityApi.creat_quality_rule(payload=payload)
        return response



qualityTestCase = QualityTestCase(navigator_endpoint=navigator_endpoint, quality_endpoint=quality_endpoint)

def paste_quality_file_by_number(parent_uuid, file_uuid, number=1):
    '''
    批量复制质量文件，可以是质量模板、质量规则、质量任务
    :param parent_uuid:
    :param number:
    :return:
    '''

    for i in range(number):
        response = qualityTestCase.paste_quality_file(parent_uuid=parent_uuid, file_uuid=file_uuid)
        #print(response.text)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response.status_code))


def paste_quality_file_by_number(parent_uuid, file_uuid, number=1):
    '''
    批量复制质量文件，可以是质量模板、质量规则、质量任务
    :param parent_uuid:
    :param number:
    :return:
    '''

    for i in range(number):
        response = qualityTestCase.paste_quality_file(parent_uuid=parent_uuid, file_uuid=file_uuid)
        #print(response.text)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response.status_code))
def creat_quality_rule_by_number(payload, number=1):
    '''
    批量复制质量文件，可以是质量模板、质量规则、质量任务
    :param parent_uuid:
    :param number:
    :return:
    '''

    for i in range(number):
        payload['ruleName'] = "quality_rule_" + get_random_by_length(10)
        response = qualityTestCase.creat_quality_rule(payload=payload)
        print(response.text)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response.status_code))


if __name__ == '__main__':
    number = 3  # 预期创建标准数量

    #批量复制质量模板
    quality_template_parent_uuid = '8125e83729044632a0665206a4cab3a7' # 质量模板目标目录uuid
    quality_template_file_uuid = '40a3235314d3449490bb0fccadb5139e' # 复制的质量模板文件uuid
    #paste_quality_file_by_number(parent_uuid=quality_template_parent_uuid, file_uuid=quality_template_file_uuid, number=number)    # 批量复制治好了模板

    # 批量创建质量规则
    # 质量规则没法复制，只能通过创建方式，此处需手动创建一个质量规则，然后将请求参数赋值给payload
    payload = {"ruleGroups": [{"id": 1, "name": "te"}],
               "parameters": [{"name": "table_a", "type": "TABLE", "description": "test", "value": "zyl.table1"}],
               "ruleGroupIds": [1], "ruleName": "tt", "description": "tsdfats",
               "templateUuid": "40a3235314d3449490bb0fccadb5139e", "templateName": "非空检查", "templateDesc": "testssss",
               "templateContent": "SELECT COUNT(1) FROM ${table_a}", "datasourceUuid": "69e352a132984aa38e9e48eaa317f8e9",
               "datasourceName": "inceptor660"}
    creat_quality_rule_by_number(payload=payload, number=number)    # 批量创建命名字典

    # 批量复制质量任务
    quality_task_parent_uuid = '32c23f3d3e2443af800738d51372cc67' # 质量任务目标目录uuid
    quality_task_file_uuid = 'b0942d50977a4d83a688134e3ce1aa9c' # 复制的质量任务文件uuid
    #paste_quality_file_by_number(parent_uuid=quality_task_parent_uuid, file_uuid=quality_task_file_uuid, number=number)    # 批量复制质量任务


