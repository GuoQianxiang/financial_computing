import numpy as np
import pandas as pd
from Strategy.bolling_macd import plot_MA
import matplotlib.pyplot as plt


def calculate_profits(df, principal, ticker):
    df = df[df['Date'].str.contains('2022')].copy()
    # 初始化变量
    initial_principal = principal
    shares = 0  # 持有股票数量
    profits = []  # 记录每次买卖的收益
    highest_profits = 0

    for i, row in df.iterrows():
        if row['trade'] == False and shares == 0:
            # 当trade为False且没有持有股票时，买入股票
            shares = principal / row['Close']
            principal = 0  # 本金全部用于买入股票
            profits.append(principal)
        elif row['trade'] == True and shares > 0:
            # 当trade为True且持有股票时，卖出股票
            profit = shares * row['Close'] - initial_principal

            principal = profit + initial_principal  # 更新本金
            shares = 0  # 清空持股数量
            profits.append(principal)
            if profit > highest_profits: highest_profits = profit

        else:
            profits.append(principal)

    # 如果最后一天还有股票，则全部卖出
    if shares > 0:
        profit = shares * df.iloc[-1]['Close'] - initial_principal
        profits[-1] = shares * df.iloc[-1]['Close']
        print(ticker + " Total Profits: ${:,.2f}".format(profit) + ', highest profits:${:,.2f}'.format(highest_profits))
    # 如果最后已经清仓，则收益等于总金池减去本金
    else:
        print(ticker + " Total Profits: ${:,.2f}".format(
            principal - initial_principal) + ', highest profits:${:,.2f}'.format(highest_profits))
    df.loc[:, 'balance'] = profits
    return df, profits


if __name__ == '__main__':
    # stock list
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'BYDDF', 'TCEHY']
    # sum all five stocks's balance
    sum_balance = pd.DataFrame(columns=['balance'], data=np.zeros(251).tolist())
    # set a subplot
    fig, ax = plt.subplots(figsize=(9, 6))
    for ticker in stocks:
        data = pd.read_csv('../Output/moving_average/' + ticker + '_moving_average.csv')
        data, profits = calculate_profits(data, 20_0000, ticker)
        # plot_MA(data, ticker, 20_0000)
        if ticker == 'TCEHY':
            ax.plot([x/20_0000 for x in profits], label='benchmark', color='blue')
        else:
            sum_balance['balance'] = sum_balance['balance'] + profits
    print('Total profits:${:,.2f}'.format(sum_balance['balance'][250] - 100_0000))
    plt.plot(sum_balance['balance']/100_0000, label='five stocks', color='orange')
    plt.title('Balance of Sum five stocks and benchmark')
    plt.legend(loc='upper right')
    plt.savefig('../Output/balance/sum_benchmark.png', dpi=300)
    plt.show()

    # 使用 'w' 模式打开文件，如果文件不存在，将会新建一个文件
    with open("profits_result.txt", "w") as file:
        # 写入一些内容
        file.write("AAPL Total Profits: $11,793.80, highest profits:$41,297.91\n")
        file.write("GOOG Total Profits: $13,929.00, highest profits:$56,380.63\n")
        file.write("MSFT Total Profits: $7,254.79, highest profits:$7,254.79\n")
        file.write("AMZN Total Profits: $-31,642.96, highest profits:$30,045.72\n")
        file.write("BYDDF Total Profits: $17,849.26, highest profits:$71,268.31\n")
        file.write("Total profits:$19,183.89\n")
        file.write("Benchmark(TCEHY) Total Profits: $−438,360.75, highest profits:$0.00")
