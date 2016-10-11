# coding=utf8
import sys

import pandas as pd
import talib
import logging


# pd.read_csv("WIKI-datasets-codes.csv",header=None,names=['code','company_name'],index_col=)

class PriceScreen(object):
    '''
    基于股票价格的股票删选
    '''



    def __init__(self,wholedata,prescreen=None):
        self.wholedata = wholedata#存储所有股票每天的价格数据的Dataframe
        self.prescreen = prescreen

    def screen_one(self,code,data):
        if self.prescreen:
            resu = self.prescreen.screen_one(code,data)
            if not resu:
                return False
        return self.check(code,data)

    def check(self,code):
        '''
        模版方法,由子类具体实现
        :param code:
        :return:
        '''
        raise NotImplementedError()
    def screen(self):
        valid_codes = []
        for name,group in self.wholedata.groupby('code'):
            if self.screen_one(name,group):
                valid_codes.append(name)
        return valid_codes


class MACDScreen(PriceScreen):


    def __init__(self, wholedata, prescreen=None,fastperiod=12,slowperiod=26,signalperiod=9):
        super(MACDScreen, self).__init__(wholedata, prescreen)
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def check(self,code,data):
        '''
        基于MACD指标,返回上个交易日出现金叉的股票
        :return:
        '''
        # logging.info('macd start to process  %s' % code)
        # prefixL = code[0].upper()
        # data = self.wholedata[self.wholedata.code==code].sort_values('date')

        macd, macdsignal, macdhist = talib.MACD(data['adj.close'].values,fastperiod=self.fastperiod
                                                , slowperiod=self.slowperiod, signalperiod=self.signalperiod)
        t1 = pd.DataFrame(
            {"close": data['adj.close'].values, "macd": macd, "macdsignal": macdsignal, 'macdhist': macdhist},
            index=data.date)
        # 判断最近一天是否上穿点
        if t1['macd'][-1] > 0 and t1['macdsignal'][-1] > 0 \
                and t1['macd'][-1] > t1['macdsignal'][-1] and t1['macd'][-2] < t1['macdsignal'][-2]:
            logging.info('%s statisfied macd indicator' % code)
            return True
        else:
            return False



class KDJScreen(PriceScreen):
    '''
    基于KDJ指标,选择相关的股票
    # 删选方法，K在20左右向上交叉D时，视为买进信号
    # k是rsv（未成熟随机指标值）的指数移动平均线，d是k的指数移动平均线。rsv小于50时表示收盘价
    # 更加接近于最低价，所以k在20左右向上交叉d表示此时价位较低（9日来看的话） 且具有增长的动量。
    '''
    def __init__(self, wholedata, prescreen=None,fastk_period=5, slowk_period=3, slowd_period=3):
        super(KDJScreen, self).__init__(wholedata, prescreen)
        self.fastk_period = fastk_period
        self.slowk_period = slowk_period
        self.slowd_period = slowd_period

    def check(self,code,data):

        high = data['adj.high'].values
        low = data['adj.low'].values
        close = data['adj.close'].values
        k, d = talib.STOCH(high, low, close,fastk_period=self.fastk_period,slowk_period=self.slowk_period,slowd_period=self.slowd_period)
        df = pd.DataFrame(data={'k': k, 'd': d}, index=data.date)
        df['j'] = 3 * df['k'] - 2 * df['d']
        if df['k'][-1] <= 25 and df['k'][-1] > df['d'][-1] \
                and df['k'][-2] < df['d'][-2]:
            logging.info('%s statisfied kdj indicator' % code)
            return True
        else:
            return False

if __name__=='__main__':
    import os
    os.chdir(os.path.dirname(__file__))
    wd = pd.read_pickle('../datas/whole_data.pickle_20161006')
    kdjs = KDJScreen(wd)
    re = kdjs.screen_one('A')