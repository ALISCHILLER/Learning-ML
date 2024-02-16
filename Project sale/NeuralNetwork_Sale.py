import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# خواندن داده‌ها از فایل CSV
data = pd.read_csv("Project sale/data.csv")

# تبدیل ستون CreateDate به فرمت تاریخ
data['CreateDate'] = pd.to_datetime(data['CreateDate'])

# استخراج ماه از ستون تاریخ
data['Month'] = data['CreateDate'].dt.month

# انتخاب ویژگی‌ها و متغیر وابسته
X = data[['Month', 'MATNR']]
y = data['NETWR_B']

# تقسیم داده‌ها به داده‌های آموزش و آزمون
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# مقیاس‌بندی ویژگی‌ها
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ساخت مدل شبکه عصبی
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)
])

# کامپایل مدل
model.compile(optimizer='adam', loss='mse')

# آموزش مدل
model.fit(X_train_scaled, y_train, epochs=50, batch_size=32, verbose=0)

# ارزیابی مدل
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
