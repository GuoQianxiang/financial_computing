import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('../Output/moving_average/AAPL_moving_average.csv')
df = df[df['Date'].str.contains('2022')]
# 初始化变量
principal = 20_0000  # 本金
shares = 0  # 持有股票数量
profits = []  # 记录每次买卖的收益
total_profits = 0  # 总收益

# 遍历DataFrame，执行买卖操作
fig, ax = plt.subplots()  # 创建图形和轴对象

# 其他代码保持不变...

for i, row in df.iterrows():
    if row['trade'] == False and shares == 0:
        # 当trade为False且没有持有股票时，买入股票
        shares = principal / row['Close']
        principal = 0  # 本金全部用于买入股票
    elif row['trade'] == True and shares > 0:
        # 当trade为True且持有股票时，卖出股票
        profit = shares * row['Close'] - 200000
        profits.append(profit)  # 记录收益
        principal = profit + 200000  # 更新本金
        shares = 0  # 清空持股数量
        total_profits += profit  # 更新总收益

        # 在图上绘制散点
        ax.scatter(row['Date'], profit, marker='o', color='r')  # 使用红色圆圈表示收益点

# 设置x轴和y轴的标签
ax.set_xlabel('Date')
ax.set_ylabel('Profits')

# 显示图形
plt.show()

# 如果最后一天还有股票，则全部卖出
if shares > 0:
    profit = shares * df.iloc[-1]['Close'] - 20_0000
    profits.append(profit)
    total_profits += profit

# 绘制收益图
# plt.plot(df['Date'], profits, marker='o')
# plt.xlabel('Date')
# plt.ylabel('Profits')
# plt.title('Profits over Time')
# plt.show()

# 输出总收益
print("Total Profits: ${:,.2f}".format(total_profits))