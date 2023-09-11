import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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
data_filtered = data[data['销售日期'].astype(str).str[:2] == '22']
data['销售日期'] = data_filtered['销售日期'].astype(str).str[2:4]


grouped_data = data.groupby(['销售日期', '分类名称'])['销量(千克)'].sum().reset_index()

# 创建日期和分类名称的唯一值列表
unique_dates = grouped_data['销售日期'].unique()
unique_categories = grouped_data['分类名称'].unique()

# 创建一个空的三维数组，用于存储销量数据
sales_volume = np.zeros((len(unique_dates), len(unique_categories)))

# 填充销量数据
for i, date in enumerate(unique_dates):
    for j, category in enumerate(unique_categories):
        volume = grouped_data.loc[(grouped_data['销售日期'] == date) & (grouped_data['分类名称'] == category), '销量(千克)']
        if not volume.empty:
            sales_volume[i, j] = volume.values[0]

# 绘制三维热力图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y = np.meshgrid(np.arange(len(unique_categories)), np.arange(len(unique_dates)))
z = sales_volume

ax.plot_surface(x, y, z, cmap='viridis')

# 设置坐标轴标签
ax.set_xticks(np.arange(len(unique_categories)))
ax.set_xticklabels(unique_categories, ha='right')
step = 2
ax.set_yticks(np.arange(len(unique_dates))[::step])
ax.set_yticklabels(unique_dates[::step])

ax.set_xlabel('分类名称')
ax.set_ylabel('销售月份')
ax.set_zlabel('销量(千克)')

plt.show()