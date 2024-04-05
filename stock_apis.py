from nsepython import *


def get_equity_history(stock, past_date, today):
    history = equity_history(stock, "EQ", past_date, today)
    return history
