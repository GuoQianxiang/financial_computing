import pandas as pd
from bolling_macd import plot_MA
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'BYDDF', 'TCEHY']
    sum_balance = pd.DataFrame(columns=['balance'], data=np.zeros(251).tolist())
    fig, ax = plt.subplots(figsize=(9, 6))
    for ticker in stocks:
        data = pd.read_csv('../Output/dynamic_program/output_' + ticker + '.csv')
        profits = data['balance']
        # plot_MA(data, ticker, 20_0000)
        if ticker == 'TCEHY':
            ax.plot([x / 20_0000 for x in profits], label='benchmark', color='blue')
        else:
            sum_balance['balance'] = sum_balance['balance'] + profits
    print('Total profits:${:,.2f}'.format(sum_balance['balance'][250] - 100_0000))
    plt.plot(sum_balance['balance'] / 100_0000, label='five stocks', color='orange')
    plt.title('Balance of Sum five stocks and benchmark')
    plt.legend(loc='upper right')
    plt.savefig('../Output/dynamic_program/sum_benchmark.png', dpi=300)
    plt.show()