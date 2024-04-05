from datetime import date, timedelta
import statistics
from stock_apis import get_equity_history as fetch_history


SIMPLE_MOVING_AVERAGE_TIME_PERIOD = 50


def calculate_average(lst):
    return sum(lst) / len(lst)


def calculate_sd(lst):
    standard_deviation = statistics.stdev(lst)
    return standard_deviation


def get_past_date(today):
    time_delta = timedelta(days=SIMPLE_MOVING_AVERAGE_TIME_PERIOD)
    past_date = today - time_delta
    return past_date


def equity_history(stock, past_date, today):
    # get equity history of a stock for the date period. Returns data as a data frame
    history = fetch_history(stock, past_date, today)
    return history


def price_list_from_history(history):
    price_list = history['CH_CLOSING_PRICE'].to_list()
    return price_list


def get_last_closing_price(price_list):
    last_closing_price = price_list[-1]
    return last_closing_price


def calculate_simple_moving_average(price_list):
    # calculate SMA
    simple_moving_average = round(calculate_average(price_list), 2)
    return simple_moving_average


def calculate_exponential_moving_average(simple_moving_average, price_list):
    # calculate multiplier
    multiplier = 2/(SIMPLE_MOVING_AVERAGE_TIME_PERIOD - 1)
    last_closing_price = get_last_closing_price(price_list)
    exponential_moving_average = (last_closing_price * multiplier) + (simple_moving_average * (1 - multiplier))
    exponential_moving_average = round(exponential_moving_average, 2)
    return exponential_moving_average


def calculate_bollinger_bands(price_list):
    standard_deviation = calculate_sd(price_list)
    simple_moving_average = calculate_simple_moving_average(price_list)
    upper_band = simple_moving_average + (standard_deviation * 2)
    lower_band = simple_moving_average - (standard_deviation * 2)
    return {'upper': round(upper_band, 2), 'lower': round(lower_band, 2)}


def stock_analysis():
    stock = "TATAMOTORS"
    # get today's date and past date for which the simple moving average is calculated
    today = date.today()
    past_date = get_past_date(today)

    # format today and past_date as per DD-MM-YYYY
    today = today.strftime("%d-%m-%Y")
    past_date = past_date.strftime("%d-%m-%Y")

    # get history data of the stock
    history = equity_history(stock, past_date, today)
    # sort the history per the timestamp
    history = history.sort_values(by=['CH_TIMESTAMP'], ascending=True)

    # get price list from history
    price_list = price_list_from_history(history)
    last_closing_price = get_last_closing_price(price_list)

    # calculate simple_moving_average
    simple_moving_average = calculate_simple_moving_average(price_list)
    # calculate simple_moving_average
    exponential_moving_average = calculate_exponential_moving_average(simple_moving_average, price_list)

    print(simple_moving_average)
    print(exponential_moving_average)

    bollinger_bands = calculate_bollinger_bands(price_list)
    if bollinger_bands['upper'] - last_closing_price > last_closing_price - bollinger_bands['upper']:
        print("short " + stock + " because last closing price is closer to upper bollinger band")
    else:
        print("buy " + stock + " because last closing price is closer to lower bollinger band")


stock_analysis()
