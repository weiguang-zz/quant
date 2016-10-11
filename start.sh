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
#启动应用,每天定时同步数据
count=`ps aux | grep main.py | wc -l`
echo $count
if [ "$count" -gt 1 ];then
    echo 'the main is already running,stop it first'
    exit
fi

nohup python main.py > logs/main.log 2>&1 &