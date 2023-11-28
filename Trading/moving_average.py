import pandas as pd
import matplotlib.pyplot as plt

# 假设你的DataFrame名为df，且含有'Close'和'prediction'两列
df = pd.read_csv('../Output/prediction/AAPL_stock_predicted.csv')


# 计算Close的14天移动平均线
df['MA14'] = df['Close'].rolling(window=14).mean()

# 创建一个新的列来保存计算结果
df['trade'] = None

# 遍历每一行，比较预测值与移动平均线的差异
for index, row in df.iterrows():
    # true represents selling signal
    if row['prediction_price'] > row['MA14'] + 0.05 * row['MA14']:
        df.at[index, 'trade'] = True
    # false represents buying signal
    elif row['prediction_price'] < row['MA14'] - 0.05 * row['MA14']:
        df.at[index, 'trade'] = False

print(df)
df.to_csv('moving_average.csv')