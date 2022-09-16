import json
import sys

from library.qt_wf_request import WF_Test
import os

#
def qt_wf(ip,dir_name,workspace_uuid,file_name,wf_server_ip):
    token = WF_Test.get_token(ip)
    print(token)
    dir_uuid = WF_Test.create_dir(ip,token,dir_name,workspace_uuid)
    print(dir_uuid)
    file_uuid = WF_Test.create_file(ip,token,file_name,dir_uuid)
    print(file_uuid)
    with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/pattern/qt_pattern/flow.json",'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
    load_dict['flow']['id'] = file_uuid
    load_dict['flow']['name'] = file_name
    print(type(file_uuid))
    load_dict['tasks'][0]['parentFlowId'] = file_uuid
    print(load_dict)
    new_load_scheme = json.dumps(load_dict)
    flow_scheme = WF_Test.flow_schemes(wf_server_ip,token,new_load_scheme)
    print(flow_scheme)

    for i in range(2):
        # 获取文件列表，拿到最后一个文件的uuid
        get_flows_mass = WF_Test.get_flows(ip, token, dir_uuid)
        print(get_flows_mass)
        flows_mass = json.loads(get_flows_mass.text)
        last_file_uuid = flows_mass['data'][-1]['uuid']
        # 更新嵌套任务流
        newfile_name = str(file_name) + str(i)
        qt_file_uuid = WF_Test.create_file(ip,token,newfile_name,dir_uuid)
        print(qt_file_uuid)
        with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/pattern/qt_pattern/qt_flow.json",'r') as new_load_f:
            new_load_dict = json.load(new_load_f)
            print(new_load_dict)
        new_load_dict['flow']['id'] = qt_file_uuid
        new_load_dict['flow']['name'] = newfile_name
        new_load_dict['tasks'][0]['name'] = 'qt_flowa' + str(i)
        new_load_dict['tasks'][0]['execSpec']['refNestFlowId'] = last_file_uuid
        new_load_dict['tasks'][0]['parentFlowId'] = qt_file_uuid
        print(new_load_dict)
        new_file_scheme = json.dumps(new_load_dict)
        qt_flow_scheme = WF_Test.flow_schemes(wf_server_ip,token,new_file_scheme)
        print(qt_flow_scheme)



if __name__ == '__main__':
    qt_wf('172.26.0.88','flow1','52CBA24E794EEC7C1E96241C2BE41593','test_wf','172.26.0.88')
    # qt_wf('172.26.0.88')