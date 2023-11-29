import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


# prepare a helper function for plotting prices to avoid code redundancy
def plot_prices(y_pred, y_test, model_name, ticker_name, title="Closing Price Predictions"):
    plt.figure(figsize=(9, 6))
    plt.title(title + f" ({model_name})" + f" ({ticker_name})")
    plt.plot(y_pred, label=model_name)
    plt.plot(y_test, label="Actual")
    plt.ylabel('Price')
    plt.xlabel('Day')
    plt.legend()
    plt.savefig('../Output/figure/' + ticker_name + '.png')
    plt.show()


def get_data(ticker, start_date, end_date):
    # 指定股票代码和时间范围

    # 使用yfinance库获取股票数据
    data = yf.download(ticker, start=start_date, end=end_date)

    # 将价格数据向上移动一个时间步长，即获取下一个价格
    data['Next Price'] = data['Close'].shift(-1)

    n_values = [1, 2, 3, 4, 5]  # 多个n值

    # 获取多个n-Price
    for n in n_values:
        data[f'Day _n-{n} Price'] = data['Close'].shift(n)

    data.to_csv('../Data/' + ticker + '_stock_data.csv')
    # print("数据", data)
    return data


def train(data, ticker):
    # get rid of rows with empty values
    data = data.dropna()
    #
    # drop unnecessary columns (only leave closing prices from the previous 5 days and those from the 'Close' column)
    # store the result in a variable called X
    X = data[["Close"] + list(filter(lambda x: "Day" in x, data.columns))]

    # print(X)

    # prepare outputs by storing values from the 'Next Price' column in a variable called y (preserve the case)
    y = data["Next Price"].to_frame()

    # split the data into a training and test sets (50% training, 50% testing)
    # remember to set shuffle to False
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.167, shuffle=False)

    # prepare a dictionary for storing test errors and predictions
    model_data = dict()
    #
    # normalise the data to speed up training (only fit on the training set!)
    X_scaler, y_scaler = StandardScaler(), StandardScaler()
    X_train = X_scaler.fit_transform(X_train)
    y_train = y_scaler.fit_transform(y_train)
    X_test = X_scaler.transform(X_test)
    y_test = y_test.values

    model = MLPRegressor(activation='relu', alpha=0.005, hidden_layer_sizes=(100,), learning_rate='invscaling',
                         max_iter=400, solver='lbfgs', batch_size=128)

    # train the Model
    model.fit(X_train, y_train.ravel())

    # get predictions
    normalised_y_pred = model.predict(X_test)

    # scale the outputs back
    y_pred = y_scaler.inverse_transform(normalised_y_pred.reshape(-1, 1))
    # calculate error
    model_name = "MLP"
    model_data[model_name] = {
        "error": mean_absolute_error(y_test, y_pred),
        "predictions": y_pred
    }
    print("Error of " + ticker + " " + model_name + " regression Model:", model_data[model_name]["error"])
    return y_pred, y_test, model_name


def add_predict(ticker, y_pred):
    ticker_data = pd.read_csv('../Data/' + ticker + '_stock_data.csv')
    # print(y_pred.shape)
    # print()
    ticker_data.loc[1258:, 'prediction_price'] = y_pred.flatten()
    ticker_data.to_csv('../Output/prediction/' + ticker + '_stock_predicted.csv')


if __name__ == '__main__':
    start_date = '2017-01-01'
    end_date = '2022-12-31'
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TCEHY', 'TSLA']
    for ticker in stocks:
        data = get_data(ticker, start_date, end_date)
        y_pred, y_test, model_name = train(data, ticker)
        # add prediction to initial data
        add_predict(ticker, y_pred)
        # plot the results
        plot_prices(y_pred, y_test, model_name, ticker)
