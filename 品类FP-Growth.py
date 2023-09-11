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


# 定义一个函数来处理日期字符串
def simplify_date(date_str):
    # 将日期字符串分割为年、月、日部分
    parts = date_str.split('-')
    year = parts[0][-2:]  # 获取年份的后两位
    month = parts[1]  # 月份部分保持不变
    day = parts[2]  # 日份部分保持不变
    # 组合年、月、日部分并返回
    simplified_date = year + month + day
    return simplified_date

# 在DataFrame中应用处理函数
df2['销售日期'] = df2['销售日期'].apply(simplify_date)

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

df.to_csv('data.csv', index=False, encoding='utf-8-sig')
# print(df.info())
# print(df.head())

# 使用groupby和agg将相同销售时间的单品放入一个集合中
result_df = df.groupby('销售时间')['分类名称'].agg(lambda x: set(x) if len(x) > 1 else x).reset_index()
result_df = result_df[result_df['分类名称'].apply(lambda x: isinstance(x, set))]
# print(result_df)

import pyfpgrowth

# 假设您的数据已经存储在一个名为data的列表中，其中每个元素是一个集合，如：[{花叶类, 水生根茎类}, {食用菌, 花菜类}, ...]
transactions = [list(item) for item in result_df['分类名称']]

# 设置支持度阈值，例如0.02，表示项集在所有交易中至少出现2%的次数
support_threshold = 0.002 * len(transactions)

# 使用find_frequent_patterns找到频繁项集
patterns = pyfpgrowth.find_frequent_patterns(transactions, support_threshold)

# 设置置信度阈值，例如0.5，表示规则成立的置信度至少为50%
confidence_threshold = 0.2

# 使用generate_association_rules找到关联规则
rules = pyfpgrowth.generate_association_rules(patterns, confidence_threshold)

# 打印关联规则
print(rules)

# rules.to_csv('rules.csv', index=False, encoding='utf-8-sig')





