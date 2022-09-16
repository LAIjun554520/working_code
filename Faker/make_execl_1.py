# ⾃动化⽤faker造数据保存到excel
import pandas as pd
from faker import Faker
import pymysql
class Create_Data(object):
    def __init__(self):
        # 选择中⽂
        fake = Faker("zh_CN")
        # ⽣成数据改变循环体来控制数据量rang(?)
        self.data_total = [
            [x,fake.name(), fake.job(), fake.company(), fake.phone_number(), fake.company_email(), fake.address(),fake.date_time(tzinfo=None)] for x in range(
2000000)]
        print(self.data_total)
    # 写⼊excel
    def deal_excel(self):
        df = pd.DataFrame(self.data_total,
                          columns=["id","name", "job", "company", "phone_number", "company_email", "address", "date_time"])
        # 保存到本地excel
        df.to_excel("2bw_data_total.xlsx", index=False)
        print("Processing completed to excel")
if __name__ == '__main__':
    data = Create_Data()
    data.deal_excel()
