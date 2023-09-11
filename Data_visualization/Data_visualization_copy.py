import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font",family='YouYuan')

# 从CSV文件加载数据
data = pd.read_csv('data.csv')

data['销售日期'] = data['销售日期'].astype(str).str[:2]

# 按单品名称分组并计算总销量
total_sales = data.groupby(['单品名称', '销售日期'])['销量(千克)'].sum().reset_index()

# 添加名为“总销量”的列，表示每个单品名称的总销量
total_sales['总销量'] = total_sales.groupby('单品名称')['销量(千克)'].transform('sum')

# 按总销量降序排序
total_sales = total_sales.sort_values(by='总销量', ascending=False)
# print(total_sales)
# 按总销量降序排列
# total_sales = total_sales.sort_values(by='销量(千克)', ascending=False)
# total_sales.to_csv('total_sales.csv', index=False, encoding='utf-8-sig')
# 选择销量排名前30的数据
# data = sorted_df.head(1000)
total_sales = total_sales.head(100)
# data['销量(千克)'] = data['销量(千克)'].head(30)

# 创建数据透视表
pivot_table = total_sales.pivot_table(index='单品名称', columns='销售日期', values='销量(千克)', fill_value=0)

print(pivot_table)
# 创建热力图
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".2f", linewidths=.5)

plt.title("251类单品销量热力图(部分)")
plt.xlabel("销售年份")
plt.ylabel("单品名称")
plt.show()
