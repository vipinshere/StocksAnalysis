from datetime import timedelta
import statistics
from service.stock_apis import get_equity_history as fetch_history
from constants.constants import SIMPLE_MOVING_AVERAGE_TIME_PERIOD, RELATIVE_STRENGTH_INDEX, RELATIVE_STRENGTH_INDEX_TIME_PERIOD


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


def closing_price_list_from_history(history):
    price_list = history['CH_CLOSING_PRICE'].to_list()
    return price_list


def get_last_closing_price(price_list):
    last_closing_price = price_list[-1]
    return last_closing_price


def get_data_from_history(history, column, time_period):
    if time_period == RELATIVE_STRENGTH_INDEX:
        return history[column].to_list()[-(RELATIVE_STRENGTH_INDEX_TIME_PERIOD + 1):]
    else:
        return None

