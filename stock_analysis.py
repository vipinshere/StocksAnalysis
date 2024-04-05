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


def calculateMACD(price_list):
    twelve_day_price_list = price_list[-12:]
    twenty_six_day_price_list = price_list[-26:]
    twelve_day_sma = calculate_simple_moving_average(twelve_day_price_list)
    twelve_day_ema = calculate_exponential_moving_average(twelve_day_sma, twelve_day_price_list)
    twenty_six_day_sma = calculate_simple_moving_average(twenty_six_day_price_list)
    twenty_six_day_ema = calculate_exponential_moving_average(twenty_six_day_sma, twenty_six_day_price_list)
    macd = twenty_six_day_ema - twelve_day_ema
    if macd > 0:
        print("MACD is positive. Good")
    else:
        print("MACD is negative. Not good")


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
    if exponential_moving_average < last_closing_price:
        print("EMA {} is lower than last closing price {} - Good".format(exponential_moving_average, last_closing_price))
    else:
        print("EMA {} is higher than last closing price {} - Not good".format(exponential_moving_average, last_closing_price))

    calculateMACD(price_list)


stock_analysis()
