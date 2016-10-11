#!/usr/bin/env bash
#!/usr/bin/env bash
BASEDIR=`dirname $0`
cd "$BASEDIR"
if [[ ! -d research ]];then
    mkdir research
fi
if [ `ps aux | grep jupyter | wc -l` -gt 1 ];then
    echo "the notebook is already running,stop it first"
    exit
fi
#启动notebook
nohup jupyter notebook --ip 0.0.0.0 > logs/notebook.log &