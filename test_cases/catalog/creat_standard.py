import json
import random
import string
import requests
requests.packages.urllib3.disable_warnings()


standard_endpoint = 'https://172.22.6.79:28381'        # catalog standard url
navigator_endpoint = 'https://172.22.6.61:28183'       # foundation navigator url
federation_token = 'VtB47TGiBQ5dmc8Q3mJP-TDH'              # Guardian Federation Server的自定义token

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

class StandardApi():
    def __init__(self, navigator_endpoint, standard_endpoint):
        """
        类初始化
        :param url: 测试环境地址，http://172.22.6.28:18141
        """
        self.standard_endpoint = standard_endpoint
        self.navigator_endpoint = navigator_endpoint

    def creat_standard(self, payload):
        """
        创建标准各资源类型
        :param payload: 字典类型,{
            "category": "STANDARD_BASIC",
            "name": "test1",
            "parentUUID": "66ac4dba50374b969da90a864c58fa58",
            "type": "STANDARD_BASIC",
            "nodeType": "FILE"
             }
        :return:
        """
        navigitorApi = NavigatorApi(self.navigator_endpoint)
        response = navigitorApi.creat_file(payload=payload)
        status_code = response.status_code
        if status_code == 200:
            body_dict = json.loads(response.text)
            uuid = body_dict["uuid"]
            name = body_dict["name"]
            return(response,status_code, uuid, name)
        else:
            return (response, None, None, None)

    def get_standard(self, resource_id):

        api = '/studio/api/standard/v1/info/{id}'.format(id=resource_id)
        url = '{endpoint}{api}'.format(endpoint=self.endpoint, api=api)
        # payload = {"page":1,"size":10,"name":"年龄","type":"Rule","status":""}
        response = requests.request("GET", url, headers=headers, verify=False)
        print(response.text)
        print(response.status_code)
        return response


class StandardTestCase():
    def __init__(self,navigator_endpoint, standard_endpoint):
        self.standardApi = StandardApi(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    def creat_base_standard(self,parent_uuid) -> dict:
        # 创建基础标准
        payload = {
            "category": "STANDARD_BASIC",
            "name": "test2",
            "parentUUID": parent_uuid,
            "type": "STANDARD_BASIC",
            "nodeType": "FILE"
        }
        payload["name"] = "base_standard_" + get_random_by_length(10)
        response = self.standardApi.creat_standard(payload=payload)
        return response

    def creat_index_standard(self,parent_uuid) -> dict:
        # 创建指标标准
        payload = {
            "category": "STANDARD_INDEX",
            "name": "test2",
            "parentUUID": parent_uuid,
            "type": "STANDARD_INDEX",
            "nodeType": "FILE"
        }
        payload["name"] = "index_standard_" + get_random_by_length(10)
        response = self.standardApi.creat_standard(payload=payload)
        return response

    def creat_dimension_standard(self,parent_uuid) -> dict:
        # 创建维度标准
        payload = {
            "category": "STANDARD_DIMENSION",
            "name": "test2",
            "parentUUID": parent_uuid,
            "type": "STANDARD_DIMENSION",
            "nodeType": "FILE"
        }
        payload["name"] = "dimension_standard_" + get_random_by_length(10)
        response = self.standardApi.creat_standard(payload=payload)
        return response

    def creat_common_code(self,parent_uuid) -> dict:
        # 创建公共代码
        payload = {
            "category": "STANDARD_COMMON",
            "name": "test2",
            "parentUUID": parent_uuid,
            "type": "STANDARD_COMMON",
            "nodeType": "FILE"
        }
        payload["name"] = "common_code_" + get_random_by_length(10)
        response = self.standardApi.creat_standard(payload=payload)
        return response

    def creat_standard_dictionary(self,parent_uuid) -> dict:
        # 创建命名字典
        payload = {
            "category": "STANDARD_DICTIONARY",
            "name": "test2",
            "parentUUID": parent_uuid,
            "type": "STANDARD_DICTIONARY",
            "nodeType": "FILE"
        }
        payload["name"] = "dictionary_" + get_random_by_length(10)
        response = self.standardApi.creat_standard(payload=payload)
        return response

def creat_base_standard_by_number(parent_uuid, number=1):
    '''
    批量创建基础标准
    :param parent_uuid:
    :param number:
    :return:
    '''
    standardTestCase = StandardTestCase(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    for i in range(number):
        response = standardTestCase.creat_base_standard(parent_uuid=parent_uuid)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response[0].status_code))

def creat_index_standard_by_number(parent_uuid, number=1):
    '''
    批量创建指标标准
    :param parent_uuid:
    :param number:
    :return:
    '''
    standardTestCase = StandardTestCase(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    for i in range(number):
        response = standardTestCase.creat_index_standard(parent_uuid=parent_uuid)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response[0].status_code))

def creat_dimension_standard_by_number(parent_uuid, number=1):
    '''
    批量创建维度标准
    :param parent_uuid:
    :param number:
    :return:
    '''
    standardTestCase = StandardTestCase(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    for i in range(number):
        response = standardTestCase.creat_dimension_standard(parent_uuid=parent_uuid)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response[0].status_code))

def creat_common_code_by_number(parent_uuid, number=1):
    '''
    批量创建公共代码
    :param parent_uuid:
    :param number:
    :return:
    '''
    standardTestCase = StandardTestCase(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    for i in range(number):
        response = standardTestCase.creat_common_code(parent_uuid=parent_uuid)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response[0].status_code))

def creat_dictionary_standard_by_number(parent_uuid, number=1):
    '''
    批量创建命名字典
    :param parent_uuid:
    :param number:
    :return:
    '''
    standardTestCase = StandardTestCase(navigator_endpoint=navigator_endpoint, standard_endpoint=standard_endpoint)

    for i in range(number):
        response = standardTestCase.creat_standard_dictionary(parent_uuid=parent_uuid)
        print("创建第{index}个,status_code: {status_code}".format(index=i,status_code=response[0].status_code))

if __name__ == '__main__':
    number = 1  # 预期创建标准数量
    base_parent_uuid = 'b4816e2ac230425a889d9bbbe01c180b' # 基础标准目标目录uuid
    index_parent_uuid = '35bc3ab73fce44399030bf545df05355' # 指标标准目标目录uuid
    dimension_parent_uuid = '7807c276eb934be2ba65bc8e4d2dd265' # 维度标准目标目录uuid
    common_code_parent_uuid = '8dee2b5dc9ce472f9f5829941a7d6580' # 公共代码目标目录uuid
    dictionary_parent_uuid = '4ee064bfe5684b06adaf120167121bdc' # 命名字典目标目录uuid
    # creat_base_standard_by_number(parent_uuid=base_parent_uuid, number=number)     # 批量创建基础标准
    # creat_index_standard_by_number(parent_uuid=index_parent_uuid, number=number)   # 批量创建指标标准
    # creat_dimension_standard_by_number(parent_uuid=dimension_parent_uuid, number=number)    # 批量创建维度标准
    # creat_common_code_by_number(parent_uuid=common_code_parent_uuid, number=number)    # 批量公共代码标准
    creat_dictionary_standard_by_number(parent_uuid=dictionary_parent_uuid, number=number)    # 批量创建命名字典




