from flask_restful import Resource,reqparse
from flask import render_template

post_parser = reqparse.RequestParser()
post_parser.add_argument('kdj',dest='kdj')
post_parser.add_argument('macd',dest='macd')

class Index(Resource):

    def get(self):
        return render_template('index.html')

    def post(self):
        args=post_parser.parse_args()
        return 'hello, index'
