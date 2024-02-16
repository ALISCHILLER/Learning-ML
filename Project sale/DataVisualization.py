import pandas as pd
import matplotlib.pyplot as plt

# خواندن داده‌ها از فایل CSV
data = pd.read_csv("Project sale/data.csv")

# تبدیل ستون CreateDate به فرمت تاریخ
data['CreateDate'] = pd.to_datetime(data['CreateDate'])

# استخراج ماه از ستون تاریخ
data['Month'] = data['CreateDate'].dt.month

# گروه‌بندی بر اساس ماه و کالا و محاسبه مجموع فروش
monthly_sales = data.groupby(['Month', 'MATNR'])['NETWR_B'].sum().reset_index()

# تجسم داده‌ها
plt.figure(figsize=(10, 6))
for product in monthly_sales['MATNR'].unique():
    product_data = monthly_sales[monthly_sales['MATNR'] == product]
    plt.plot(product_data['Month'], product_data['NETWR_B'], label=f'Product {product}')

plt.xlabel('Month')
plt.ylabel('Sales')
plt.title('Monthly Sales for Each Product')
plt.legend()
plt.grid(True)
plt.show()
