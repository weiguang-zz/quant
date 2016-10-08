#coding=utf8
'''
提供从quandl同步数据的工具
目前仅仅同步wiki database

'''
import sys
from datetime import datetime,timedelta

import pandas as pd
import quandl

import os
import time
import requests
import zipfile
import re
import glob
from requests.exceptions import RequestException
import utils
import logging

ppath = utils.get_absolute_path('datas')#存储数据的父目录
PICKLE_FILE_PATH_PREFIX = 'whole_data.pickle'

def sync_whole(force=False):
    '''

    :param force: 是否需要重新下载,否则的话,会继续上一次的下载
    :return:
    '''
    try:
        link = "https://www.quandl.com/api/v3/databases/WIKI/data?api_key=ZB_kT6_ftbkEqJMLnXeH"
        download_path = os.path.join(ppath,'wholedata.zip')
        if os.path.exists(download_path) and force:
            os.remove(download_path)
            resume_download(link,filename=download_path)
        else:
            resume_download(link,filename=download_path)

        logging.info('rebuild the pickle datas')
        z = zipfile.ZipFile(download_path, 'r')
        f = z.namelist()[0]
        names = ['code', 'date', 'open', 'high', 'low', 'close', 'volumn'
            , 'dividends', 'split_ratio', 'adj.open', 'adj.high', 'adj.low'
            , 'adj.close', 'adj.volumn']
        df = pd.read_csv(z.open(f), header=None,names=names)

        datestr = re.search('\d+',f).group()# 获取全量数据持续到哪一天
        pickle_path = os.path.join(ppath,'%s_%s' % (PICKLE_FILE_PATH_PREFIX, datestr))

        for whole_file in glob.glob0(ppath,PICKLE_FILE_PATH_PREFIX+'*'):
            os.remove(whole_file)
        df.to_pickle(pickle_path)
        os.remove(download_path)
        logging.info('sync whole done')
    except RequestException :
        logging.info('resume download')
        sync_whole()



def get_current_utctime_str(pat='%Y-%m-%d'):
    utctime = time.gmtime()
    return time.strftime(pat,utctime)


def sync_last_day(force=False):
    try:
        link = "https://www.quandl.com/api/v3/databases/WIKI/data?api_key=ZB_kT6_ftbkEqJMLnXeH&download_type=partial"
        download_path = os.path.join(ppath,"dailydata.zip")
        if os.path.exists(download_path) and force:
            os.remove(download_path)
            resume_download(link,download_path)
        else:
            resume_download(link,download_path)

        z = zipfile.ZipFile(download_path, 'r')
        f = z.namelist()[0]
        #校验全量数据中是否含有当前的daily数据
        wf = glob.glob1(ppath,PICKLE_FILE_PATH_PREFIX+'*')[0]
        wholedate = re.search('\d+',wf).group()#全量数据的时间
        wd = time.strptime(wholedate,'%Y%m%d')
        ddstr = re.search('\d+',f).group()#增量数据的时间
        dd = time.strptime(ddstr, '%Y%m%d')
        if wd >= dd:
            logging.info('the whole data already has the daily data on date:%s' % wholedate)
            os.remove(download_path)
            return
        else:
            names = ['code', 'date', 'open', 'high', 'low', 'close', 'volumn'
                , 'dividends', 'split_ratio', 'adj.open', 'adj.high', 'adj.low'
                , 'adj.close', 'adj.volumn']
            dailydf = pd.read_csv(z.open(f), header=None, names=names)
            alldf = pd.read_pickle(wf)
            merged = pd.concat((alldf,dailydf))
            the_new_pickle_path = os.path.join(ppath,'%s_%s' % (PICKLE_FILE_PATH_PREFIX, ddstr))

            os.remove(os.path.join(ppath,wf))#删除原有的全量pickle文件
            os.remove(download_path)
            merged.to_pickle(the_new_pickle_path)
            logging.info('done')
    except RequestException:
        logging.info('resume download')
        sync_last_day()


def resume_download(url,filename,chunk_size=4096):

    with open(filename, "ab") as f:
        logging.info("Downloading %s" % filename)
        downloaded_bytes = f.tell()
        resume_header = {'Range': 'bytes=%d-' % downloaded_bytes}
        response = requests.get(url, stream=True, headers=resume_header,verify=False,timeout=(3,5))

        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = downloaded_bytes
            total_length = int(total_length) + dl
            for data in response.iter_content(chunk_size=chunk_size):
                dl += len(data)
                f.write(data)
                pct = float(dl) / total_length * 100
                # done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%%]" % pct)
                sys.stdout.flush()
if __name__ == '__main__':
    utils.set_logconf()
    sync_last_day()


