# https://blog.csdn.net/xinyuzxx/article/details/81703625?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-10.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromMachineLearnPai2%7Edefault-10.control
# pip install cx_Oracle
import random
import string

import cx_Oracle as ora  # 导入模块

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

print(__file__)
with open(file='procedure.sql', mode='r', encoding='utf-8') as f:
    procedure_sql = f.read()
conn = ora.connect('qatest','QAtest12','172.26.0.102:1521/helowin')

cursor = conn.cursor()  # cursor方法相当于设置一个游标，由于对Oracle不是很熟悉，反正就是没有这一步是不可以进行后续操作的
for i in range(1):
    # print('TEST.procedure{suffix}'.format(suffix=get_random_by_length()))
    sql = procedure_sql.replace('TEST.procedure', 'TEST.procedure_{suffix}'.format(suffix=get_random_by_length()))
    # print(sql)
    cursor.execute(sql)  # execute方法用来执行sql语句
    print('第 {index} 存储过程创建完成！'.format(index=i))

conn.commit()
cursor.close()
conn.close()





def test_oracle():
    conn = ora.connect('qatest', 'QAtest12', '172.26.0.102:1521/helowin')
    cursor = conn.cursor()  # cursor方法相当于设置一个游标，由于对Oracle不是很熟悉，反正就是没有这一步是不可以进行后续操作的
    sql = "select * from  TEST.ORA_1000_COLUMNS"  # 自定义sql语句
    cursor.execute(sql)  # execUte方法用来执行sql语句
    conn.commit()

    data = cursor.fetchone()  # fetchone方法执行结果的第一条数据，返回成一个元组
    data_all = cursor.fetchall()  # fetchall方法获取sql语句执行结果的所有数据，返回一个列表，每条数据作为一个元组
    print(data)
    print(type(data))
    print(data_all)

    index = cursor.description
    print(index)
