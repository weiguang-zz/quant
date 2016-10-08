#coding=utf8
'''
该脚本在同步脚本执行完毕后执行,选取推荐的股票发送邮件
'''
from screen.base import KDJScreen,MACDScreen
import pandas as pd
import utils
import os
import glob
import logging

def choose():
    wf = glob.glob1(utils.get_absolute_path('datas'),'whole_data.pickle*')[0]
    wdf = pd.read_pickle(os.path.join(utils.get_absolute_path('datas'), wf))
    ms = MACDScreen(wdf)
    mscodes = ms.screen()
    ks = KDJScreen(wdf)
    kcodes = ks.screen()

    body = 'macd:%s\nkdj:%s' % (mscodes,kcodes)
    utils.send_mail(['zhengzhang23@creditease.cn'],'choose results',body=body)

    logging.info('done')


if __name__=='__main__':
    utils.set_logconf()
    choose()
