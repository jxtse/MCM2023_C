import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc("font",family='YouYuan')

# 读取数据
data = pd.read_csv('data.csv')

# 数据预处理：筛选蔬菜品类，按日期和分类名称分组，计算每组销量总和
# 定义一个字典，将原始的分类名称映射到新的数字
category_mapping = {
    '花菜类': 1,
    '花叶类': 2,
    '水生根茎类': 3,
    '茄类': 4,
    '辣椒类': 5,
    '食用菌': 6
}

# 使用replace方法进行替换
data['分类名称'] = data['分类名称'].replace(category_mapping)

# 假设您的DataFrame为df，且包含“销售日期”列
# data['销售日期'] = data['销售日期'].astype(str).str[:2].astype(int)
data['销售日期'] = data['销售日期'].astype(str).str[:2] == '22'


grouped_data = data.groupby(['销售日期', '分类名称'])['销量(千克)'].sum().reset_index()

# # 创建日期和分类名称的唯一值列表
# unique_dates = grouped_data['销售日期'].unique()
# unique_categories = grouped_data['分类名称'].unique()

# # 创建一个空的三维数组，用于存储销量数据
# sales_volume = np.zeros((len(unique_dates), len(unique_categories)))

# # 填充销量数据
# for i, date in enumerate(unique_dates):
#     for j, category in enumerate(unique_categories):
#         volume = grouped_data.loc[(grouped_data['销售日期'] == date) & (grouped_data['分类名称'] == category), '销量(千克)']
#         if not volume.empty:
#             sales_volume[i, j] = volume.values[0]
            
# # df = pd.DataFrame(sales_volume)
# df = pd.DataFrame(sales_volume, columns=unique_categories)

# # 创建包含销售年份和分类名称的DataFrame
# data_df = pd.read_csv('data.csv')  # 读取包含销售年份和分类名称的数据
# data_df = data_df[['销售日期', '分类名称']]  # 选择需要的列

# # 合并数据
# merged_df = pd.concat([data_df, df], axis=1)

# print(merged_df.head(5))

# 假设销售数据存储在df中，包括'品类'、'销售年份'和'销量'列
pivot_table = data.pivot_table(index='销售日期', columns='分类名称', values='销量(千克)', aggfunc='sum')
correlation_matrix = pivot_table.corr()

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("不同蔬菜品类在不同年份销量变化的相关性热力图")
plt.xlabel("蔬菜品类")
plt.ylabel("蔬菜品类")
plt.show()
