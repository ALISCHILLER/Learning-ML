import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

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

# تعیین مقادیر پارامترهای Grid Search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# ساخت یک مدل Random Forest Regression
rf = RandomForestRegressor()

# اعمال Grid Search برای یافتن بهترین پارامترها
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='neg_mean_squared_error', verbose=2)
grid_search.fit(X_train, y_train)

# یافتن بهترین مدل با پارامترهای بهینه
best_rf = grid_search.best_estimator_

# پیش‌بینی فروش برای داده‌های آزمون
y_pred = best_rf.predict(X_test)

# ارزیابی مدل
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)
print('Best Parameters:', grid_search.best_params_)
