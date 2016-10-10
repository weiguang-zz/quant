BASEDIR=`dirname $0`
cd $BASEDIR
#创建log目录
if [[ ! -d logs ]];then
    mkdir logs
fi
