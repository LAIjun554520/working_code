# #!/usr/bin/python
# # -*- coding: UTF-8 -*-
#
# import mysql.connector  # 引入mysql包
# from faker import Faker  # 引入faker库
#
# faker = Faker("zh_CN")  # 指定faker库造什么语言的假数据，中文：zh-CN，英文：en_US
#
# #创建连接对象，设置连接信息
# #如果不设置端口（port），则会按默认的3306端口连接
# try:
#     conn = mysql.connector.connect(
#         host="172.26.2.15",
#         user="vt_app",
#         passwd="transwarp",
#         port=15307,
#         database='bc_test',
#         auth_plugin='mysql_native_password'
#     )
# except mysql.connector.Error as e:
#     print('connect fail!{}'.format(e))
#
# cursor = conn.cursor()  # 使用cursor()方法获取操作游标
#
# # 创建测试表
# # 若表已存在，则不创建
# try:
#     sql = '''
#          create table if not exists `中文测试表`(
#            编号 bigint NOT NULL primary key AUTO_INCREMENT,
#            姓名 varchar(20) not null comment '姓名',
#            省份 varchar(20) not null comment '省份',
#            年龄 varchar(3) not null comment '年龄',
#            地址 varchar(64) not null comment '地址',
#            词语 varchar(64) not null comment '词语',
#            生成时间 timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6) comment '创建时间')
#         '''
#     cursor.execute(sql)  # 执行sql语句
# except mysql.connector.Error as e:
#     print('create error!{}'.format(e))
#
#
# # 定义sql插入数据语句
# insertNumber = 100 #设置要插入的数据量
# try:
#     for i in range(insertNumber):
#         myName = faker.name()
#         province = faker.province()
#         myAge = faker.random_int(1, 99)
#         myAddress = faker.address()
#         word = faker.word()
#         sql = "insert into `中文测试表`(姓名,省份,年龄,地址,词语)values('%s','%s','%s','%s','%s')" % (
#             myName, province, myAge, myAddress,word)
#         print("插入的数据：", myName, province, myAge, myAddress,word)
#         cursor.execute(sql)  # 执行sql语句
#     conn.commit()  # 数据表内容有更新，必须使用到该语句，否则会出现 虽然执行成功但表未新增记录的情况
#     print("插入", insertNumber, "条数据成功！")
# except mysql.connector.Error as e:
#     print('insert error!{}'.format(e))
#
# finally:
#     cursor.close()  # 关闭指针对象
#     conn.close()  # 关闭连接对象



#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector  # 引入mysql包
from faker import Faker  # 引入faker库

faker = Faker("en_US")  # 指定faker库造什么语言的假数据，中文：zh-CN，英文：en_US

#创建连接对象，设置连接信息
#如果不设置端口（port），则会按默认的3306端口连接
try:
    conn = mysql.connector.connect(
        host="172.26.2.15",
        user="vt_app",
        passwd="transwarp",
        port=15307,
        database='bc_test',
        auth_plugin='mysql_native_password'
    )
except mysql.connector.Error as e:
    print('connect fail!{}'.format(e))

cursor = conn.cursor()  # 使用cursor()方法获取操作游标

# 创建测试表
# 若表已存在，则不创建
try:
    sql = '''
         create table if not exists English_Table(
           id bigint NOT NULL primary key AUTO_INCREMENT,
           name varchar(200) not null comment '姓名',
           city varchar(200) not null comment '省份',
           age varchar(3) not null comment '年龄',
           address varchar(200) not null comment '地址',
           word varchar(64) not null comment '词语',
           create_time timestamp(6) NULL DEFAULT CURRENT_TIMESTAMP(6) comment '创建时间')
        '''
    cursor.execute(sql)  # 执行sql语句
except mysql.connector.Error as e:
    print('create error!{}'.format(e))


# 定义sql插入数据语句
insertNumber = 100 #设置要插入的数据量
try:
    for i in range(insertNumber):
        myName = faker.name()
        country = faker.country()
        myAge = faker.random_int(1, 99)
        myAddress = faker.address()
        word = faker.word()
        sql = "insert into English_Table (name,city,age,address,word)values('%s','%s','%s','%s','%s')" % (
            myName, country, myAge, myAddress,word)
        print("插入的数据：", myName, country, myAge, myAddress,word)
        cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 数据表内容有更新，必须使用到该语句，否则会出现 虽然执行成功但表未新增记录的情况
    print("插入", insertNumber, "条数据成功！")
except mysql.connector.Error as e:
    print('insert error!{}'.format(e))

finally:
    cursor.close()  # 关闭指针对象
    conn.close()  # 关闭连接对象

