import pandas as pd
import matplotlib.pyplot as plt


def calculate_MA(df, ticker, factor):
    # 计算Close的14天移动平均线
    df['MA14'] = df['Close'].rolling(window=14).mean()

    # 创建一个新的列来保存计算结果
    df['trade'] = None

    # 遍历每一行，比较预测值与移动平均线的差异
    for index, row in df.iterrows():
        # true represents selling signal
        if row['prediction_price'] > row['MA14'] + factor * row['MA14']:
            df.at[index, 'trade'] = True
        # false represents buying signal
        elif row['prediction_price'] < row['MA14'] - factor * row['MA14']:
            df.at[index, 'trade'] = False

    # print(df)
    df.to_csv('../Output/moving_average/' + ticker + '_moving_average.csv')
    return df


def plot_MA(df, ticker):
    # 筛选2022年的数据
    df = df[df['Date'].str.contains('2022')]
    # 绘制折线图
    fig, ax = plt.subplots(figsize=(9, 6))

    # 设置Close、prediction_price、MA14的颜色
    colors = ['blue', 'orange', 'red']

    # 绘制Close、prediction_price、MA14的折线图
    for i, column in enumerate(['Close', 'prediction_price', 'MA14']):
        ax.plot(df['Date'], df[column], linestyle='-', color=colors[i], label=column)

    # 将trade列为True的点在Close线上标记为下三角形，trade列为False的点在Close线上标记为倒三角形
    trade_true_close = df[df['trade'] == True]['Close']
    trade_false_close = df[df['trade'] == False]['Close']
    trade_true_dates = df[df['trade'] == True]['Date']
    trade_false_dates = df[df['trade'] == False]['Date']

    ax.scatter(trade_true_dates, trade_true_close, marker='v', color='black', label='sell', s=100)
    ax.scatter(trade_false_dates, trade_false_close, marker='^', color='black', label='buy', s=100)

    # 设置图表标题和轴标签
    ax.set_title('Close, Prediction Price, and MA14 Line Chart for '+ticker)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.set_xticks(range(0, 251, 50))
    ax.set_xticklabels([str(int(tick)) for tick in ax.get_xticks()])  # 将刻度值转换为整数并标在刻度上

    plt.savefig('../Output/signals/' + ticker + '.png', dpi=300)
    # 显示图表
    plt.show()


if __name__ == '__main__':
    # 假设你的DataFrame名为df，且含有'Close'和'prediction'两列
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TCEHY', 'TSLA']
    for ticker in stocks:
        data = pd.read_csv('../Output/prediction/' + ticker + '_stock_predicted.csv')
        data = calculate_MA(data, ticker, 0.05)
        plot_MA(data, ticker)
