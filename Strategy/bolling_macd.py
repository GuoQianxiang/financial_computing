import pandas as pd
import matplotlib.pyplot as plt


def plot_MA(df, ticker):
    # 绘制折线图
    fig, ax = plt.subplots(figsize=(9, 6))

    plt.plot(df['Date'], df['Close'], label='Close', color='blue')

    # 将trade列为True的点在Close线上标记为下三角形，trade列为False的点在Close线上标记为倒三角形
    trade_true_close = df[df['trade'] == True]['Close']
    trade_false_close = df[df['trade'] == False]['Close']
    trade_true_dates = df[df['trade'] == True]['Date']
    trade_false_dates = df[df['trade'] == False]['Date']

    ax.scatter(trade_true_dates, trade_true_close, marker='v', color='black', label='sell', s=100)
    ax.scatter(trade_false_dates, trade_false_close, marker='^', color='black', label='buy', s=100)

    # 创建一个与第一个坐标轴共享x轴，但有不同y轴的第二个坐标轴
    ax2 = ax.twinx()
    # 在第二个坐标轴上画图
    ax2.plot(df['Date'], df['balance']/10_0000, label='balance', color='orange')
    ax2.set_ylabel('balance', color='orange')  # 设置y2的标签颜色
    ax2.tick_params('y', colors='orange')  # 设置y轴的颜色
    ax2.legend()
    # 设置图表标题和轴标签
    ax.set_ylabel('Close price', color='blue')  # 设置y2的标签颜色
    ax.tick_params('y', colors='blue')  # 设置y轴的颜色
    ax.set_title('Close Line Chart for '+ticker)
    ax.set_xlabel('Date')
    # 创建一个图例
    ax.legend()
    ax.set_xticks(range(0, 251, 50))
    ax.set_xticklabels([str(int(tick)) for tick in ax.get_xticks()])  # 将刻度值转换为整数并标在刻度上

    # plt.savefig('../Output/signals/' + ticker + '.png', dpi=300)
    # 显示图表
    plt.show()


if __name__ == '__main__':
    data = pd.read_csv('AAPL_trade_macd_5_15.csv')
    plot_MA(data, 'apple')