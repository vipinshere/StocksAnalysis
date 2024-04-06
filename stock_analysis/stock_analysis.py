from datetime import date
from utilities.utilities import *
from constants.constants import CLOSING_PRICE, RELATIVE_STRENGTH_INDEX


def calculate_simple_moving_average(price_list):
    # calculate SMA
    simple_moving_average = round(calculate_average(price_list), 2)
    return simple_moving_average


def calculate_exponential_moving_average(simple_moving_average, price_list):
    # calculate multiplier
    multiplier = 2 / (SIMPLE_MOVING_AVERAGE_TIME_PERIOD - 1)
    last_closing_price = get_last_closing_price(price_list)
    exponential_moving_average = (last_closing_price * multiplier) + (simple_moving_average * (1 - multiplier))
    exponential_moving_average = round(exponential_moving_average, 2)
    return exponential_moving_average


def calculate_macd(price_list):
    twelve_day_price_list = price_list[-12:]
    twenty_six_day_price_list = price_list[-26:]
    twelve_day_sma = calculate_simple_moving_average(twelve_day_price_list)
    twelve_day_ema = calculate_exponential_moving_average(twelve_day_sma, twelve_day_price_list)
    twenty_six_day_sma = calculate_simple_moving_average(twenty_six_day_price_list)
    twenty_six_day_ema = calculate_exponential_moving_average(twenty_six_day_sma, twenty_six_day_price_list)
    macd = twenty_six_day_ema - twelve_day_ema
    return macd


def calculate_percentage_return(history):
    first_date_closing_price = history['CH_CLOSING_PRICE'].iloc[0]
    last_date_closing_price = history['CH_CLOSING_PRICE'].iloc[-1]
    percentage_return = ((last_date_closing_price - first_date_closing_price)/first_date_closing_price) * 100
    return round(percentage_return, 2)


def calculate_bollinger_bands(price_list):
    standard_deviation = calculate_sd(price_list)
    simple_moving_average = calculate_simple_moving_average(price_list)
    upper_band = simple_moving_average + (standard_deviation * 2)
    lower_band = simple_moving_average - (standard_deviation * 2)
    return {'upper': round(upper_band, 2), 'lower': round(lower_band, 2)}


def calculate_rsi(history):
    rsi_historical_data = get_data_from_history(history, CLOSING_PRICE, RELATIVE_STRENGTH_INDEX)
    up_closing_prices_list = []
    down_closing_prices_list = []
    for index, data in enumerate(rsi_historical_data):
        if index == 0:
            continue
        else:
            close_price = data
            previous_close_price = rsi_historical_data[index - 1]
            if close_price > previous_close_price:
                up_closing_prices_list.append(round(close_price - previous_close_price, 2))
                down_closing_prices_list.append(0)
            else:
                down_closing_prices_list.append(round(previous_close_price - close_price, 2))
                up_closing_prices_list.append(0)
    sma_up = statistics.mean(up_closing_prices_list)
    sma_down = statistics.mean(down_closing_prices_list)
    smoothened_up_closing_prices_list = []
    smoothened_down_closing_prices_list = []
    for up in up_closing_prices_list:
        smoothened_up_closing_prices_list.append(((1 / RELATIVE_STRENGTH_INDEX_TIME_PERIOD) * up) +
                                                 ((13 / 14) * sma_up))
    for down in down_closing_prices_list:
        smoothened_down_closing_prices_list.append(((1 / RELATIVE_STRENGTH_INDEX_TIME_PERIOD) * down) +
                                                   ((13 / 14) * sma_down))
    average_up_price_change = statistics.mean(smoothened_up_closing_prices_list)
    average_down_price_change = statistics.mean(smoothened_down_closing_prices_list)
    relative_strength = average_up_price_change / average_down_price_change
    relative_strength_index = round(100 - (100 / (1 + relative_strength)), 2)
    return relative_strength_index


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
    price_list = closing_price_list_from_history(history)
    last_closing_price = get_last_closing_price(price_list)

    # calculate simple_moving_average
    simple_moving_average = calculate_simple_moving_average(price_list)
    # calculate simple_moving_average
    exponential_moving_average = calculate_exponential_moving_average(simple_moving_average, price_list)
    if exponential_moving_average < last_closing_price:
        print("EMA {} is lower than LCP {} - Good".format(exponential_moving_average, last_closing_price))
    else:
        print("EMA {} is higher than LCP {} - Not good".format(exponential_moving_average, last_closing_price))
    # Calculate Moving Average Convergence & Divergence
    macd = calculate_macd(price_list)
    if macd > 0:
        print("MACD is positive. Good")
    else:
        print("MACD is negative. Not good")

    # calculate bollinger bands
    bollinger_bands = calculate_bollinger_bands(price_list)
    if bollinger_bands['upper'] - last_closing_price > last_closing_price - bollinger_bands['upper']:
        print("short {} because last closing price is closer to upper bollinger band".format(stock))
    else:
        print("buy {} because last closing price is closer to lower bollinger band".format(stock))

    # calculate percentage change between last closing price and closing price from the first date in history
    percentage_return = calculate_percentage_return(history)
    print(percentage_return)

    # calculate Relative Strength Index (RSI)
    rsi = calculate_rsi(history)


stock_analysis()
