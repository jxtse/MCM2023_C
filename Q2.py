import pandas as pd

# 读取数据
data = pd.read_csv("问题二1数据.csv")

# data_filtered = data[data['类别'].astype(str).str[5:7] == '辣椒']
# data['类别'] = data_filtered['类别']

# 检查缺失值
missing_values = data.isnull().sum()

# 处理缺失值（如果有）
data = data.dropna()

# 数据摘要统计信息
summary_stats = data.describe()

correlation = data['profit_margin'].corr(data['total_quantity'])

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.rc("font",family='YouYuan')

# 绘制散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x='total_quantity', y='profit_margin', data=data, hue='类别')
plt.title('不同类别中profit_margin和total_quantity的相关关系')
plt.xlabel('total_quantity')
plt.ylabel('profit_margin')
plt.legend(title='类别')

# 获取当前轴上的图例
handles, labels = plt.gca().get_legend_handles_labels()

# 仅保留前8个图例项
new_handles = handles[:20]
new_labels = labels[:20]

# 创建一个自定义图例
custom_legend = plt.legend(new_handles, new_labels, loc='upper right')

# 添加自定义图例到当前图表
plt.gca().add_artist(custom_legend)
plt.show()
