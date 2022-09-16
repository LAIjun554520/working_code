# import json
#
# from library.sqlbook_request import Sqlbook_Test
#
# with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/library/uuid.txt", 'r', encoding='UTF-8') as f1:
#     lines = f1.readlines()
#     for i in lines:
#         # print(i.rstrip(),end = "")
#         ss = Sqlbook_Test.sql_value('172.26.5.39:28110','bearer 38785e2d-577c-4811-8df1-267708d1286a', i.rstrip())
#         print(ss)
#         s1 = json.loads(ss)
#         s2 = s1['content']
#         print(s2)
