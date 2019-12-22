import pandas as pd
import numpy as np
from entity.constants import *
from .order import Order
import gateway.binance_api.enums as binance_enums


def alpaca_to_goquant(symbol, in_data):
    cur_df = in_data[symbol].rename(
        {'open': DATA_OPEN, 'high': DATA_HIGH, 'low': DATA_LOW,
         'close': DATA_CLOSE, 'volume': DATA_VOLUME},
        axis=1)
    cur_df[DATA_ADJCLOSE] = cur_df[DATA_CLOSE]
    cur_df[DATA_SYMBOL] = symbol
    cur_df.index.names = [DATA_DATETIME]
    cur_df.dropna(inplace=True)
    return cur_df[DATA_HISTORICAL_COLS]


def binance_to_goquant(symbol, in_data):
    in_data[DATA_DATETIME] = pd.to_datetime(in_data[DATA_DATETIME], unit='ms')
    df_binance = in_data.set_index(DATA_DATETIME)
    df_binance[DATA_SYMBOL] = symbol
    df_binance[DATA_ADJCLOSE] = df_binance[DATA_CLOSE]
    return df_binance[DATA_HISTORICAL_COLS]


def order_goquant_to_binance(order: Order):
    side_map = {
        ORDER_BUY: binance_enums.SIDE_BUY,
        ORDER_SELL: binance_enums.SIDE_SELL
    }
    type_map = {
        ORDER_TYPE_MARKET: binance_enums.ORDER_TYPE_MARKET
    }
    ret = {
        "symbol": order.symbol,
        "side": side_map[order.side],
        "type": type_map[order.type],
        "quantity": order.qty
    }
    return ret
