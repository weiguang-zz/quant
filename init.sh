#!/usr/bin/env bash
BASEDIR=`dirname $0`
cd $BASEDIR
#创建log目录
if [[ ! -d logs ]];then
    mkdir logs
fi
if [[ ! -d datas ]];then
    mkdir datas
fi
if [[ ! -d research ]];then
    mkdir research
fi
#启动应用,每天定时同步数据
nohup python main.py > logs/main.log &
#启动notebook
nohup jupyter notebook --ip 0.0.0.0 > logs/notebook.log &