import csv
from faker import Faker
import datetime
fake = Faker(['zh_CN'])
file = open("/Users/simons/PycharmProjects/TEST/studio_performance_test/Faker/test_data.csv","w", encoding="utf-8", newline="")
# 创建文件，分别是文件名、w打开方式(w代表新建，如果已存在，就删除重写)、newline(如果不加，每行数据就会多一空白行)
fwrite = csv.writer(file)
# 获取写文件的对象
fwrite.writerow(["id", "name", "phone", "Card_id", "公司", "地址", "信用卡", "职位", "email"])
# 写入标题头
for i in range(500):
    id = i
    user_name = fake.name()
    phone = fake.phone_number()
    card_id = fake.ssn()
    company = fake.company()
    addr = fake.address()
    bank_card = fake.credit_card_number()
    title = fake.job()
    email = fake.email()
    fwrite.writerow([id, user_name, phone, card_id, company, addr, bank_card, title, email])
# 写入一行一行的数据
file.close()