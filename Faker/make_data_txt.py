# # ⾃动化⽤faker造数据保存到txt
# from faker import Faker
# import time
# now=time.time()
# class Create_Data(object):
#     def __init__(self):
#         # 选择中⽂
#         fake = Faker("zh_CN")
#         # ⽣成数据改变循环体来控制数据量rang(?)
#         self.data_total = [
#             [x, fake.name(), fake.random_int(), fake.job(), fake.company(), fake.phone_number(), fake.company_email(), fake.address(),
#              fake.date_time(tzinfo=None)] for x in range(10000)]
#         # print(self.data_total)
#     def deal_txt(self):
#         with open("txt_file"+str(int(round(now * 1000)))+".txt", "w", errors="ignore", encoding="utf-8") as output:
#             output.write("id|name|job|company|phone_number|company_email|address|date_time\n")
#
#             for row in self.data_total:
#                 rowtxt = "{}|{}|{}|{}|{}|{}|{}|{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
#                 output.write(rowtxt)
#                 output.write("\n")
#             output.close()
#             print("Processing completed to txt")
# if __name__ == '__main__':
#     data = Create_Data()
#     data.deal_txt()


# ⾃动化⽤faker造数据保存到txt
from faker import Faker
import time
now=time.time()
# import pymysql
class Create_Data(object):
    def __init__(self):
        # 选择中⽂
        fake = Faker("zh_CN")
        # ⽣成数据改变循环体来控制数据量rang(?)
        self.data_total = [
            [x ,fake.random_int(), fake.name(), fake.am_pm(), fake.boolean(), fake.country_code(), fake.country(), fake.province(),
             fake.postcode(), fake.date_object()] for x in range(500)]
        print(self.data_total)
    def deal_txt(self):
        with open("txt_file"+str(int(round(now * 1000)))+".txt", "w", errors="ignore", encoding="utf-8") as output:
            output.write("序号, 年纪, 姓名, AM_PM, boolean, 国际代码, 国籍名称, 省份, 邮编, 日期\n")

            for row in self.data_total:
                rowtxt = "{},{},{},{},{},{},{},{},{},{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                output.write(rowtxt)
                output.write("\n")
            output.close()
            print("Processing completed to txt")
if __name__ == '__main__':
    data = Create_Data()
    data.deal_txt()

# # 中文
# # ⾃动化⽤faker造数据保存到txt
# from faker import Faker
# # import pymysql
# class Create_Data(object):
#     def __init__(self):
#         # 选择中⽂
#         fake = Faker("zh_CN")
#         # ⽣成数据改变循环体来控制数据量rang(?)
#         self.data_total = [
#             [x+1500, fake.name(), fake.job(), fake.company(), fake.city_suffix(), fake.district(), fake.street_name(),
#              fake.company_suffix()] for x in range(500)]
#         print(self.data_total)
#     def deal_txt(self):
#         with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/CN_TXT_GB18030_4.txt", "w", errors="ignore", encoding="GB18030") as output:
#             output.write("序号,名字,工作,公司,市,区,街道名,公司性质\n")
#
#             for row in self.data_total:
#                 rowtxt = "{},{},{},{},{},{},{},{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
#                 output.write(rowtxt)
#                 output.write("\n")
#             output.close()
#             print("Processing completed to txt")
# if __name__ == '__main__':
#     data = Create_Data()
#     data.deal_txt()

# # 英文
# # ⾃动化⽤faker造数据保存到txt
# from faker import Faker
# # import pymysql
# class Create_Data(object):
#     def __init__(self):
#         # 选择中⽂
#         fake = Faker("en_US")
#         # ⽣成数据改变循环体来控制数据量rang(?)
#         self.data_total = [
#             [x, fake.name(), fake.random_element(), fake.currency_code(), fake.month_name(), fake.file_path(), fake.domain_name(),
#              fake.street_address()] for x in range(500)]
#         print(self.data_total)
#     def deal_txt(self):
#         with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/txt_en_gbk.txt", "w", errors="ignore", encoding="GBK") as output:
#             output.write("id,name,random_element,currency_code,month_name,file_path,domain_name,street_address\n")
#
#             for row in self.data_total:
#                 rowtxt = "{},{},{},{},{},{},{},{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
#                 output.write(rowtxt)
#                 output.write("\n")
#             output.close()
#             print("Processing completed to txt")
# if __name__ == '__main__':
#     data = Create_Data()
#     data.deal_txt()


# # ⾃动化⽤faker造数据保存到txt
# from faker import Faker
# # import pymysql
# class Create_Data(object):
#     def __init__(self):
#         # 选择中⽂
#         fake = Faker("zh_CN")
#         # ⽣成数据改变循环体来控制数据量rang(?)
#         self.data_total = [
#             [x,
#              fake.name(),
#              fake.pyfloat(left_digits=2,right_digits=2,positive=True),
#              fake.pyfloat(left_digits=2,right_digits=3,positive=True),
#              fake.random_digit(),
#              fake.random_int(),
#              fake.pyfloat(left_digits=2, right_digits=4, positive=True),
#              fake.random_int(),
#              fake.pyfloat(left_digits=2, right_digits=4, positive=True),
#              fake.boolean(),
#              fake.district(),
#              fake.street_name(),
#              fake.company_suffix(),
#              fake.sentence(),
#              fake.past_date(),
#              fake.future_datetime(),
#              fake.time()] for x in range(500)]
#         print(self.data_total)
#     def deal_txt(self):
#         with open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/TXT_type.txt", "w", errors="ignore", encoding="UTF-8") as output:
#             output.write("id,name,ATINYINT,ASMALLINT,AINT,ABIGINT,AFLOAT,ADOUBLE,ADECIMAL,ABOOLEAN,ASTRING,ACHAR,AVARCHAR,AVARCHAR2,ADATE,ATIMESTAME,ATIME\n")
#
#             for row in self.data_total:
#                 rowtxt = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])
#                 output.write(rowtxt)
#                 output.write("\n")
#             output.close()
#             print("Processing completed to txt")
# if __name__ == '__main__':
#     data = Create_Data()
#     data.deal_txt()
