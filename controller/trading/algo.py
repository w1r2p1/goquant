from datetime import datetime, timezone
import pandas as pd
from pyalgotrade import strategy

from entity.constants import *
from controller.trading.account import get_account_class
from controller.data.data import GQData
from util.logger import logger


class GQAlgo(object):
    def __init__(self, trading_platform, datasource):
        self.trading_platform = trading_platform
        self.datasource = datasource
        self.account = get_account_class(trading_platform)
        self.data = GQData()
        self.t = None  # current time in UTC

        self.backtest_strategy = None
        self.metrics = {}

        self.init()

    def init(self):
        pass

    def run(self) -> [list]:
        raise NotImplementedError

    def get_trading_platform(self):
        return self.trading_platform

    def get_time(self):
        return self.t

    def get_cash(self):
        """
        get current cash in USD
        :return:
        """
        return self.account.get_cash()

    def get_positions(self):
        """
        get current positions
        :return: dict
            symbol->position
        """
        return self.account.get_positions()

    def algo_get_data(self, symbols, interval_timedelta, freq, fill_nan_method=None, remove_nan_rows=True):
        """
        get data until now (time t, get from get_time())
        :param symbols: list
            list of symbols
        :param interval_timedelta: deltatime
            used to calculate start time
        :param freq: string
            day, minute data level
        :param fill_nan_method: string
            fill nan method, default not fill, see more parameters here:
            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html
        :param remove_nan_rows: bool
            remove nan rows after fill nan
        :return:
        """
        end_datetime = datetime.now(timezone.utc)
        if self.trading_platform == TRADING_BACKTEST:
            end_datetime = self.get_time()
            if end_datetime is None:
                raise ValueError("please run prerun() function first")
        start_datetime = end_datetime - interval_timedelta
        data = self.data.get_data(symbols=symbols,
                                  freq=freq,
                                  start_date=start_datetime,
                                  end_date=end_datetime,
                                  datasource=self.datasource,
                                  dict_output=True,
                                  fill_nan_method=fill_nan_method,
                                  remove_nan_rows=remove_nan_rows
                                  )
        return data

    def init_backtest(self, strategy: strategy.BacktestingStrategy):
        self.backtest_strategy = strategy
        self.account.set_backtest_strategy(strategy)

    def prerun(self, t, verbose=True):
        if verbose:
            msg = "=============\nAlgorithm Time: {}\nCash: {}\nPositions: {}\n".format(
                t, self.get_cash(), self.get_positions()
            )
            logger.info(msg)
        self.t = t

    def record_metric(self, key, value, figure_group=1):
        if figure_group < 0:
            raise ValueError("figure_grouup only can be positive, get figure_group {}".format(figure_group))
        cur_data_serise, _ = self.metrics.get(key, (pd.Series([], name=key), figure_group))
        cur_data_serise = cur_data_serise.append(pd.Series([value], index=[self.t], name=key))
        self.metrics[key] = (cur_data_serise, figure_group)
