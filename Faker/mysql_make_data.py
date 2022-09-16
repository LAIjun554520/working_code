#!/usr/bin/python
# -*- coding: UTF-8 -*-

import mysql.connector  # 引入mysql包
from faker import Faker  # 引入faker库

faker = Faker("en_US")  # 指定faker库造什么语言的假数据，中文：zh-CN，英文：en_US

#创建连接对象，设置连接信息
#如果不设置端口（port），则会按默认的3306端口连接
try:
    conn = mysql.connector.connect(
        host="172.26.0.14",
        user="root",
        passwd="password",
        port=3306,
        database='demo',
        auth_plugin='mysql_native_password'
    )
except mysql.connector.Error as e:
    print('connect fail!{}'.format(e))

cursor = conn.cursor()  # 使用cursor()方法获取操作游标

# 创建测试表
# 若表已存在，则不创建
try:
    sql = '''
         create table if not exists ince_data(
           id bigint primary key auto_increment,
           atinyint tinyint, 
           asmallint smallint,
           aint int,
           afloat float ,
           adouble double ,
           adecimal decimal ,
           aboolean boolean,
           astring varchar(200) not null comment '姓名',
           achar char(100),
           avarcahr varchar(200) not null comment '电话号码',
           avarchar2 varchar(100),
           adate date,
           atimestamp timestamp )
        '''
    cursor.execute(sql)  # 执行sql语句
except mysql.connector.Error as e:
    print('create error!{}'.format(e))


# 定义sql插入数据语句
insertNumber = 2 #设置要插入的数据量
try:
    for i in range(insertNumber):
        atinyint = faker.pyfloat(left_digits=1, right_digits=2, positive=True)
        asmallint = faker.pyfloat(left_digits=2, right_digits=2, positive=True)
        aint = faker.random_int()
        afloat = faker.pyfloat(left_digits=1, right_digits=2, positive=True)
        adouble = faker.random_int()
        adecimal = faker.pyfloat(left_digits=2, right_digits=2, positive=True)
        aboolean = faker.boolean()
        astring = faker.name()
        achar = faker.word()
        avarcahr = faker.phone_number()
        avarchar2 = faker.url()
        adate = faker.date_object()
        atimestamp = faker.date_time()
        sql = "insert into test_data(atinyint,asmallint,aint,afloat,adouble,adecimal,aboolean,astring,achar,avarcahr,avarchar2,adate,atimestamp)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            atinyint,asmallint,aint,afloat,adouble,adecimal,aboolean,astring,achar,avarcahr,avarchar2,adate,atimestamp)
        print("插入的数据：", atinyint,asmallint,aint,afloat,adouble,adecimal,aboolean,astring,achar,avarcahr,avarchar2,adate,atimestamp)
        cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 数据表内容有更新，必须使用到该语句，否则会出现 虽然执行成功但表未新增记录的情况
    print("插入", insertNumber, "条数据成功！")
except mysql.connector.Error as e:
    print('insert error!{}'.format(e))

finally:
    cursor.close()  # 关闭指针对象
    conn.close()  # 关闭连接对象
