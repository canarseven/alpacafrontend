from django.shortcuts import render
from django.http import HttpResponse, Http404

import datetime
import os
import sys

import alpaca_trade_api as tradeapi
import requests
import pandas as pd


def initialize_api():
    try:
        api = tradeapi.REST()
        return api
    except:
        print("Error in api init ...")
        print("Exciting program.")
        sys.exit()


def check_account_status(api):
    account = api.get_account()
    return account.status


def check_positions(api):
    account = api.get_account()
    positions = api.list_positions()

    current_portfolio_val = account.portfolio_value
    current_cash = account.cash

    formatted_positions = []
    for position in positions:
        formatted_position = {
            "symbol": position.symbol,
            "market_value": round(float(position.market_value), 2),
            "unrealized_plpc": round(float(position.unrealized_plpc), 2) * 100,
            "unrealized_intraday_plpc": round(float(position.unrealized_intraday_plpc), 2) * 100,
            "share_of_portfolio": round(float(position.market_value) / float(current_portfolio_val), 2) * 100
        }
        formatted_positions.append(formatted_position)
    formatted_positions = pd.DataFrame(formatted_positions)
    formatted_positions.sort_values(by="unrealized_plpc")
    positions_data = {"positions": formatted_positions,
                      "portfolio_val": round(float(current_portfolio_val), 2),
                      "cash": round(float(current_cash), 2)}
    return positions_data


# Create your views here.
def index(request):
    api = initialize_api()
    positions_data = check_positions(api)
    return render(request, "frontend/index.html", positions_data)
