#
# import csv
# from faker import Faker
# import datetime
# fake = Faker(['zh_CN'])
# file = open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/csv_zl4.csv","w", encoding="utf-8", newline="")
# # 创建文件，分别是文件名、w打开方式(w代表新建，如果已存在，就删除重写)、newline(如果不加，每行数据就会多一空白行)
# fwrite = csv.writer(file)
# # 获取写文件的对象
# fwrite.writerow(["id", "name", "phone", "Card_id", "公司", "地址", "信用卡", "职位", "email"])
# # 写入标题头
# for i in range(500):
#     id = i + 2000
#     user_name = fake.name()
#     phone = fake.phone_number()
#     card_id = fake.ssn()
#     company = fake.company()
#     addr = fake.address()
#     bank_card = fake.credit_card_number()
#     title = fake.job()
#     email = fake.email()
#     fwrite.writerow([id, user_name, phone, card_id, company, addr, bank_card, title, email])
# # 写入一行一行的数据
# file.close()



import csv
from faker import Faker
import time
fake = Faker(['zh_CN'])
now=time.time()
file = open("csv_file"+str(int(round(now * 1000)))+".csv" ,"w", encoding="utf-8", newline="")
# 创建文件，分别是文件名、w打开方式(w代表新建，如果已存在，就删除重写)、newline(如果不加，每行数据就会多一空白行)
fwrite = csv.writer(file)
# 获取写文件的对象
fwrite.writerow(['序号','年纪', '姓名', 'am_pm', 'boolean', '国际代码', '国籍名称', '省份', '邮编', '时间'])
# 写入标题头
for i in range(500):
    id = i+500
    age = fake.random_int()
    user_name = fake.name()
    am_pm = fake.am_pm()
    boolean = fake.boolean()
    code = fake.country_code()
    country = fake.country()
    province = fake.province()
    postcode = fake.postcode()
    date = fake.date_object()
    fwrite.writerow([id, age, user_name, am_pm, boolean, code, country, province, postcode, date])
# 写入一行一行的数据
file.close()


# import csv
# from faker import Faker
# import datetime
# fake = Faker(['zh_CN'])
# file = open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/US_CSV_GBK4.csv","w", encoding="GBK", newline="")
# # 创建文件，分别是文件名、w打开方式(w代表新建，如果已存在，就删除重写)、newline(如果不加，每行数据就会多一空白行)
# fwrite = csv.writer(file)
# # 获取写文件的对象
# fwrite.writerow(['序号', '姓名', '工作', '公司', '市', '区', '街道名', '公司性质', '词语'])
# # 写入标题头
# for i in range(500):
#     id = i+1500
#     user_name = fake.name()
#     phone = fake.job()
#     card_id = fake.company()
#     code = fake.city_suffix()
#     country = fake.district()
#     province = fake.street_name()
#     postcode = fake.company_suffix()
#     address = fake.word()
#     fwrite.writerow([id, user_name, phone, card_id, code, country, province, postcode, address])
# # 写入一行一行的数据
# file.close()
#


# import csv
# from faker import Faker
# import datetime
# fake = Faker(['en_US'])
# file = open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/en_us_csv_gbk.csv","w", encoding="GBK", newline="")
# # 创建文件，分别是文件名、w打开方式(w代表新建，如果已存在，就删除重写)、newline(如果不加，每行数据就会多一空白行)
# fwrite = csv.writer(file)
# # 获取写文件的对象
# fwrite.writerow(['ID', 'NAME', 'JOB', 'CONPANY', 'city_suffix', 'random_element', 'province', 'postcode', 'address'])
# # 写入标题头
# for i in range(500):
#     id = i
#     user_name = fake.name()
#     phone = fake.job()
#     card_id = fake.company()
#     code = fake.city_suffix()
#     random_element = fake.random_element()
#     province = fake.street_name()
#     postcode = fake.company_suffix()
#     address = fake.word()
#     fwrite.writerow([id, user_name, phone, card_id, code, random_element, province, postcode, address])
# # 写入一行一行的数据
# file.close()