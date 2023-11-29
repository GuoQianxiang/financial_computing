import pandas as pd
from Strategy.bolling_macd import plot_MA


def calculate_profits(df, principal, ticker):
    df = df[df['Date'].str.contains('2022')].copy()
    # 初始化变量
    initial_principal = principal
    shares = 0  # 持有股票数量
    profits = []  # 记录每次买卖的收益
    total_profits = 0  # 总收益

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

        else:
            profits.append(principal)

    # 如果最后一天还有股票，则全部卖出
    if shares > 0:
        profit = shares * df.iloc[-1]['Close'] - initial_principal
        profits[-1] = shares * df.iloc[-1]['Close']
        print(ticker + " Total Profits: ${:,.2f}".format(profit))
    # 如果最后已经清仓，则收益等于总金池减去本金
    else:
        print(ticker + " Total Profits: ${:,.2f}".format(principal - initial_principal))
    df.loc[:, 'balance'] = profits
    return df


if __name__ == '__main__':
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TCEHY', 'TSLA']
    for ticker in stocks:
        data = pd.read_csv('../Output/moving_average/' + ticker + '_moving_average.csv')
        data = calculate_profits(data, 20_0000, ticker)

        plot_MA(data, ticker, 20_0000)

