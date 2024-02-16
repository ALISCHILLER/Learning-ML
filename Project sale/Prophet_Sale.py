import pandas as pd
from fbprophet import Prophet

# فرض کنید data_frame داده‌های شما است
data_frame = pd.read_csv("Project sale/data.csv")
# تبدیل ستون زمان به تاریخ
data_frame['Time'] = pd.to_datetime(data_frame['Time'])

# محاسبه جمع فروش برای هر ماه و شعبه
monthly_sales = data_frame.groupby(['Branch', pd.Grouper(key='Time', freq='M')])['Sales'].sum().reset_index()

# آماده‌سازی داده برای Prophet
monthly_sales.rename(columns={'Time': 'ds', 'Sales': 'y'}, inplace=True)

# ایجاد مدل Prophet
model = Prophet()

# آموزش مدل
model.fit(monthly_sales)

# پیش‌بینی فروش برای ماه‌های آینده
future = model.make_future_dataframe(periods=12, freq='M')
forecast = model.predict(future)

# چاپ نتایج پیش‌بینی
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12))
