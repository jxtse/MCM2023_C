import pandas as pd
import numpy as np  
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

df1 = pd.read_csv('附件1.csv')
df2 = pd.read_csv('附件2.csv', dtype={'销售日期': str, '扫码销售时间':str})
df3 = pd.read_csv('附件3.csv', dtype={'日期': str})
df4 = pd.read_csv('附件4.csv')

# # 简化数据
# 将'销售日期'和'扫码销售时间'数据进行简化


def process_text(text, indices):
    selected_chars = ''.join(text[i] for i in indices if 0 <= i < len(text))
    return selected_chars

sales_date = [3, 5, 6, 8, 9]
df2['销售日期'] = df2['销售日期'].apply(lambda x: process_text(x, sales_date))
# df2['扫码销售时间'] = df2['扫码销售时间'].str[:2]

# # 统一附件三格式

def process_text(text, indices):
    selected_chars = ''.join(text[i] for i in indices if 0 <= i < len(text))
    return selected_chars

sales_date = [3, 5, 6, 8, 9]
df3['日期'] = df3['日期'].apply(lambda x: process_text(x, sales_date))
new_column_name = '销售日期'
df3.columns.values[0] = new_column_name

# # 将附件一、附件三、附件四的信息加入附件二

df1_key = df1['单品编码'].tolist()
df1_value1 = df1['分类名称'].tolist()
df1_value2 = df1['单品名称'].tolist()
df4_key = df4['单品编码'].tolist()
df4_value = df4['损耗率(%)'].tolist()
csv_dict1_1 = dict(zip(df1_key, df1_value1))
csv_dict1_2 = dict(zip(df1_key, df1_value2))
csv_dict4 = dict(zip(df4_key, df4_value))

def get_value(key, csv_dict):
    return csv_dict.get(key, None)
df2['单品名称'] = df2['单品编码'].apply(get_value, args=(csv_dict1_2,))
df2['分类名称'] = df2['单品编码'].apply(get_value, args=(csv_dict1_1,))
df2['损耗率(%)'] = df2['单品编码'].apply(get_value, args=(csv_dict4,))
merged_df = df2.merge(df3[['销售日期', '单品编码', '批发价格(元/千克)']], on=['销售日期', '单品编码'], how='left')

# # 将数据改为适当的数据类型，并将'扫码销售时间'改为'存放时常(小时)'

# columns_to_convert = {'扫码销售时间': int, '损耗率(%)': float}
# df2 = df2.astype(columns_to_convert)
# df2['扫码销售时间'] = df2['扫码销售时间'] - 4
# new_column_name = '存放时常(小时)'
# df2.rename(columns={'扫码销售时间': new_column_name}, inplace=True)
df2.columns = df2.columns.tolist()
new_columns = df2.columns.tolist()
df = pd.DataFrame(df2.values, columns=new_columns)
columns_to_convert = {'单品编码': int, '销量(千克)': float,
                      '销售单价(元/千克)': float, '损耗率(%)': float
                     }
# df['存放时常(小时)'] = df['存放时常(小时)'].astype('int64')
df['单品编码'] = df['单品编码'].astype('int64')

# 定义一个函数来处理每一行的'扫码销售时间'
def process_time(row):
    time_str = row['扫码销售时间']
    time_int = int(time_str.replace(':', '').replace('.', ''))
    return time_int

# 使用apply()方法将处理函数应用到'扫码销售时间'列的每一行
df['扫码销售时间'] = df.apply(process_time, axis=1)

df['销售日期'] = df['销售日期'].astype(int)

# 将'销售日期'和'扫码销售时间'列合并成一个新列'销售时间'
df['销售时间'] = df['销售日期'] + df['扫码销售时间']

# df.to_csv('data.csv', index=False, encoding='utf-8-sig')
# print(df.info())
# print(df.head())

# 使用groupby和agg将相同销售时间的单品放入一个集合中
result_df = df.groupby('销售时间')['单品名称'].agg(lambda x: set(x) if len(x) > 1 else x).reset_index()
result_df = result_df[result_df['单品名称'].apply(lambda x: isinstance(x, set))]
# print(result_df)

# 将包含集合的行合并到一个列表中
basket = result_df['单品名称'].tolist()

# 将数据转换为适合Apriori的格式
te = TransactionEncoder()
te_ary = te.fit(basket).transform(basket)

# 使用pandas创建一个DataFrame
df = pd.DataFrame(te_ary, columns=te.columns_)

# 使用Apriori找出所有的频繁项集
frequent_itemsets = apriori(df, min_support=0.0001, use_colnames=True)

# 使用频繁项集生成规则
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

# 筛选单品类与单品类之间的关联规则
rules = rules[rules['antecedents'].apply(lambda x: len(x) == 1) &
                                               rules['consequents'].apply(lambda x: len(x) == 1)]



# print(basket)

# 打印关联规则
print(rules)

rules.to_csv('rules_single.csv', index=False, encoding='utf-8-sig')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
matplotlib.rc("font",family='YouYuan')

# 读取关联规则数据
rules = pd.read_csv('rules_single.csv')

# 提取antecedents和consequents列中的标签
rules['antecedents'] = rules['antecedents'].apply(lambda x: x.strip("frozenset()").replace("'", ""))
rules['consequents'] = rules['consequents'].apply(lambda x: x.strip("frozenset()").replace("'", ""))

# 绘制支持度和置信度的散点图
# plt.figure(figsize=(8, 6))
# sns.scatterplot(x='support', y='confidence', data=rules)
# plt.title('Support vs Confidence')
# plt.xlabel('Support')
# plt.ylabel('Confidence')
# plt.show()

# 绘制规则的热力图
pivot_table = rules.pivot_table(index='antecedents', columns='consequents', values='lift')
plt.figure(figsize=(12, 10))
sns.heatmap(pivot_table, annot=False, cmap='coolwarm')
plt.xticks(rotation=45)
plt.xticks(fontsize=8)
plt.title('单品关联性强度热力图')
plt.show()




