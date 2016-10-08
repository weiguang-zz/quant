#coding=utf8
from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
import quandl
from flask_restful import Resource,Api
from jinja2 import Environment,PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

from resources.index import Index



quandl.ApiConfig.api_key='ZB_kT6_ftbkEqJMLnXeH'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/quant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# api = Api(app)
#
# #the route
# api.add_resource(Index,'/index','/')#使用flask-restful会在返回template的时候出现问题

@app.route("/index",methods=['POST','GET'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:

        return 'haha'


@app.after_request
def add_header(response):
    # response.headers['Content-Type']='text/html'
    return response

if __name__ == '__main__':
    app.run(debug=True)
