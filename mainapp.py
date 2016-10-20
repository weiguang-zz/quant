#coding=utf8
from flask import Flask,render_template,request,url_for,request
from flask_sqlalchemy import SQLAlchemy
import quandl
from flask_restful import Resource,Api
from screen.base import KDJScreen,MACDScreen
import pandas as pd
import utils
import glob
import os
import logging
from sync import sync_whole,sync_last_day
import threading
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

_datas = None
def _get_datas():
    global _datas
    if _datas is not None:
        return _datas
    filename = glob.glob1(utils.get_absolute_path("datas"),'whole_data.pickle*')[0]
    _datas = pd.read_pickle(os.path.join(utils.get_absolute_path("datas"),filename))
    return _datas
# quandl.ApiConfig.api_key='ZB_kT6_ftbkEqJMLnXeH'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/quant'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)
# api = Api(app)
#
# #the route
# api.add_resource(Index,'/index','/')#使用flask-restful会在返回template的时候出现问题

class Config(object):
    JOBS = [
        {
            'id': 'test_job',
            'func': 'sync:job1',
            'args': (1, 2),
            'trigger': 'cron',
            'minute': 10
        },
        {
            'id': 'sync_last_day_data',
            'func': 'sync:sync_last_day',
            'args': (),
            'trigger': 'cron',
            'hour': 12
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///'+utils.get_absolute_path("datas/jobstore.db"))
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }


    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'



app = Flask(__name__)
app.config.from_object(Config())

api = Api(app) #集成restful

scheduler = APScheduler()
scheduler.init_app(app)#集成apscheduler
scheduler.delete_all_jobs()
scheduler.start()


@app.after_request
def add_header(response):
    response.headers['Content-Type']='application/json'
    return response

class KDJ(Resource):
    def get(self):
        ks = KDJScreen(_get_datas())
        return ks.screen(),200


class MACD(Resource):
    def get(self):
        ms = MACDScreen(_get_datas())
        return ms.screen(),200
#同步服务的endpoint
class Sync(Resource):
    def __init__(self):
        self.is_whole_running = False
        self.is_daily_running = False
    def get(self,sync_type):
        global _datas
        if sync_type=='whole' and not self.is_whole_running:
            self.is_whole_running = True
            logging.info("sync whole start")
            sync_whole()
            _datas = None#刷新价格数据
            self.is_whole_running = False
            return 'success'
        elif sync_type=='daily' and not self.is_daily_running:
            self.is_daily_running = True
            sync_last_day()
            _datas = None
            self.is_daily_running = False
            return 'success'
        else:
            return 'not support sync_type:%s or the sync is running' % sync_type

api.add_resource(KDJ,'/kdj')
api.add_resource(MACD,'/macd')
api.add_resource(Sync,'/sync/<string:sync_type>')

if __name__ == '__main__':
    utils.set_logconf()
    app.run()
