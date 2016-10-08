#coding=utf8
import pandas as pd
from zipline.api import (
    history,
    set_slippage,
    slippage,
    set_commission,
    commission,
    order_target_percent,
    sid,
    schedule_function,
    date_rules, time_rules,symbol,
    record)
import logging
from zipline import TradingAlgorithm
import numpy as np
import cvxopt as opt
from cvxopt import blas,solvers
import matplotlib.pyplot as plt
from datetime import datetime


def initialize(context):
    '''
    Called once at the very beginning of a backtest (and live trading).
    Use this method to set up any bookkeeping variables.

    The context object is passed to all the other methods in your algorithm.

    Parameters

    context: An initialized and empty Python dictionary that has been
             augmented so that properties can be accessed using dot
             notation as well as the traditional bracket notation.

    Returns None
    '''
    # # Register history container to keep a window of the last 100 prices.
    # add_history(100, '1d', 'price')
    # Turn off the slippage model
    set_slippage(slippage.FixedSlippage(spread=0.0))
    # Set the commission model (Interactive Brokers Commission)
    set_commission(commission.PerShare(cost=0.005, min_trade_cost=1.5))

    context.isfirst = True



def handle_data(context, data):
    #每个工作日进行调仓,
    pass
