import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# خواندن داده‌ها از فایل CSV
data = pd.read_csv('Project sale/data.csv')

# تبدیل ستون CreateDate به فرمت تاریخ
data['CreateDate'] = pd.to_datetime(data['CreateDate'])

# استخراج ماه از ستون تاریخ
data['Month'] = data['CreateDate'].dt.month

# انتخاب ویژگی‌ها و متغیر وابسته
X = data[['Month', 'MATNR']]
y = data['NETWR_B']

# تقسیم داده‌ها به داده‌های آموزش و آزمون
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ایجاد مدل Linear Regression
model = LinearRegression()

# آموزش مدل
model.fit(X_train, y_train)

# پیش‌بینی فروش برای داده‌های آزمون
y_pred = model.predict(X_test)

# ارزیابی مدل
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
