from openpyxl import workbook
from faker import Faker
import time
now=time.time()

wb = workbook.Workbook()
faker = Faker("zh-CN")
ws = wb.active
ws.append(['序号', '姓名', '工作', '公司', '市', '区', '街道名', '公司性质', '词语'])
for i in range(500):#注意：1.每次执行后都会覆盖之前的数据
    ws.append([i+1500, faker.name(),faker.job(), faker.company(), faker.city_suffix(), faker.district(), faker.street_name(), faker.company_suffix(), faker.word()])
#wb.save('c:/Users/Desktop/data.xlsx')#自定义文件存放位置，若无会则自动创建
wb.save("execl_file"+str(int(round(now * 1000)))+".xlsx") # 默认存放在当前project下，若无会自动创建
