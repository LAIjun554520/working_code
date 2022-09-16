import json
from library.sqlbook_request import Sqlbook_Test
import time



def sqlbook_exec(sqlbook_ip, token, file_uuid):
    # 创建执行空间
    instance_massage = Sqlbook_Test.open_instance(sqlbook_ip, token)
    print(instance_massage)
    instance_massage_json = json.loads(instance_massage)
    instanceUuid = instance_massage_json['instanceUuid']
    print(instanceUuid)
    # 获取sql内容
    sql_content = Sqlbook_Test.sql_value(sqlbook_ip, token, file_uuid)
    print(sql_content)
    content_res = json.loads(sql_content)
    sql_vlues = content_res['content']
    print("-----" + "sql_vlues" + "------")
    print(sql_vlues)
    # 获取session
    result = Sqlbook_Test.get_session(sqlbook_ip, token)
    new_session = json.loads(result)
    sessions_list = []
    for i in new_session:
        sessions_statue = i['sessions']
        print(sessions_statue)
        if sessions_statue :
            sessions_list.append(sessions_statue)
    print(sessions_list)
    dataSourceUuid = sessions_list[0][0]['uuid']
    print(dataSourceUuid)
    # 重试数据源
    new_source = Sqlbook_Test.retry_datasource(sqlbook_ip, token, dataSourceUuid, file_uuid, instanceUuid)
    print(new_source)
    # 执行sql语句
    sql_exec = Sqlbook_Test.sql_register(sqlbook_ip, token, dataSourceUuid, file_uuid, instanceUuid, sql_vlues)
    print(sql_exec)
    new_result = json.loads(sql_exec)
    registerId = new_result['registerId']
    print(registerId)
    time.sleep(5)
    # 获取执行结果统计
    result_count = Sqlbook_Test.get_result_count(sqlbook_ip, token, registerId)
    print(result_count)
    new_count = json.loads(result_count)
    successCount = new_count['successCount']
    failCount = new_count['failCount']
    print(successCount, failCount)
    # # 获取详细执行结果
    rigister_result = Sqlbook_Test.get_result(sqlbook_ip, token, registerId)
    print(rigister_result)
    new_resulta = json.loads(rigister_result)
    state_list = []
    for i in new_resulta:
        state = i['state']
        state_list.append(state)
    print(state_list)
    for i in state_list:
        if i == 'RUNNUNG' or i == 'FAILURE':
            print('sql执行有失败语句，写入文件')
            with open('./sql_execute.txt', 'a') as file:
                file.write('失败sql任务的uuid:' + str(file_uuid))
                file.write('\n')
                file.close()
                break
        else:
            print('sql执行通过')

    # 关闭执行空间
    close_ins = Sqlbook_Test.close_instance(sqlbook_ip, instanceUuid, token)
    print(close_ins)


if __name__ == '__main__':
    f1 = open("./library/uuid.txt", 'r', encoding='UTF-8')
    lines = f1.readlines()
    for uuid in lines:
        sqlbook_exec('172.26.2.14:28110', 'bearer a735e9c0-bdf4-4408-81dc-abba5f19fe36', uuid.rstrip())


