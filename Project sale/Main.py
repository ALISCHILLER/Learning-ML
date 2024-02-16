import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("Project sale/data.csv")

print(data.info())

# مشاهده آمار و توصیف داده‌ها
print(data.describe())




# توزیع متغیر NETWR_B با نمودار histogram
sns.histplot(data['NETWR_B'], kde=True)
plt.xlabel('NETWR_B')
plt.ylabel('Frequency')
plt.title('Distribution of NETWR_B')
plt.show()

# توزیع متغیر دیگر با استفاده از نمودار boxplot
sns.boxplot(x='Your_Column', data=data)
plt.xlabel('Your_Column')
plt.ylabel('Value')
plt.title('Boxplot of Your_Column')
plt.show()