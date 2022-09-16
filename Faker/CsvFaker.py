
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

#
# # ⾃动化⽤faker造数据保存到txt
# from faker import Faker
# import time
# now=time.time()
# # import pymysql
# class Create_Data(object):
#     def __init__(self):
#         # 选择中⽂
#         fake = Faker("zh_CN")
#         # ⽣成数据改变循环体来控制数据量rang(?)
#         self.data_total = [
#             [x ,fake.random_int(), fake.name(), fake.am_pm(), fake.boolean(), fake.country_code(), fake.country(), fake.province(),
#              fake.postcode(), fake.date_object()] for x in range(500)]
#         print(self.data_total)
#     def deal_txt(self):
#         with open("txt_file"+str(int(round(now * 1000)))+".txt", "w", errors="ignore", encoding="utf-8") as output:
#             output.write("序号, 年纪, 姓名, AM_PM, boolean, 国际代码, 国籍名称, 省份, 邮编, 日期\n")
#
#             for row in self.data_total:
#                 rowtxt = "{},{},{},{},{},{},{},{},{},{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
#                 output.write(rowtxt)
#                 output.write("\n")
#             output.close()
#             print("Processing completed to txt")
# if __name__ == '__main__':
#     data = Create_Data()
#     data.deal_txt()
