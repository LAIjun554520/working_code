# import jaydebeapi
#
# url = 'jdbc:dm://172.26.0.14:5236'
# user = 'SYSDBA'
# password = 'SYSDBA'
# dirver = 'dm.jdbc.driver.DmDriver'
# jarFile = '/Users/simons/PycharmProjects/TEST/studio_performance_test/library/Dm7JdbcDriver17.jar'
# sqlStr = 'select count(*) from SYSDBA.torc_data_qw0'
# conn = jaydebeapi.connect(dirver, url, [user, password], jarFile)
# curs=conn.cursor()
# curs.execute(sqlStr)
# result=curs.fetchall()
# print(result)
# curs.close()
# conn.close()


# for i in range(5):
#     sqlStr = 'select count(*) from SYSDBA.mysql_ince_dm' + str(i)
#     print(sqlStr)
#     with open('./dm_result_qw.txt', 'a') as file:
#         file.write(result)
#         file.write('\n')
#         file.close()

import datetime
import json

from library.sqlbook_request import Sqlbook_Test

if __name__ == '__main__':
    result = Sqlbook_Test.get_session('172.26.2.14:28110', 'bearer a735e9c0-bdf4-4408-81dc-abba5f19fe36')
    new_session = json.loads(result)
    # print(new_session)
    sessions_list = []
    for i in new_session:
        sessions_statue = i['sessions']
        print(sessions_statue)
        if sessions_statue :
            sessions_list.append(sessions_statue)
    print(sessions_list)
    uuid = sessions_list[0][0]['uuid']
    print(uuid)
    # list_temp = []
    # if list_temp:
    #      print(1)
    # else:
    #     print(2)



    # result1 = Sqlbook_Test.close_instance('172.26.2.14:28110', 'instance-34211684-7d32-4207-8a05-a223131230e3"', 'bearer a735e9c0-bdf4-4408-81dc-abba5f19fe36')
    # print(result1)

    # new_source = Sqlbook_Test.retry_datasource('172.26.2.14:28110', 'bearer a735e9c0-bdf4-4408-81dc-abba5f19fe36', 'session-1bd2f6f6-119d-4230-b5b1-ebcc1f7c86a9', 'fc95239245754faeb3525bfcd377713a', 'instance-75079f13-ae32-41bc-9afa-0a1fd0e9d8de')
    # print(new_source)



# now_time = datetime.datetime.now ()
# print(now_time)
#
#
# list = []
# list.append('s')
# print(list)
# list.append('a')
# print(list)