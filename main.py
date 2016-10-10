#coding=utf8

'''
1 启动同步数据的定时任务
2 启动智能选股的定时任务
'''

import schedule
import time
import logging
import utils
import sync
from jobs import daily_choose



if __name__=='__main__':
    utils.set_logconf()
    logging.info("app started")
    schedule.every().day.at('09:00').do(sync.sync_last_day)#每天上午9点同步数据
    schedule.every().day.at('10:00').do(daily_choose)
    while True:
        schedule.run_pending()
        time.sleep(1)
