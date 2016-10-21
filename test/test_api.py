from unittest import TestCase
from flask import Flask
from flask_apscheduler import APScheduler
import pandas as pd
from mainapp import app

class TestApi(TestCase):
    def setUp(self):
        self.app = app
        # self.app.config['SCHEDULER_VIEWS_ENABLED'] = True
        # self.scheduler = APScheduler(app=self.app)
        # self.scheduler.start()
        self.client = self.app.test_client()

    def test_kdj(self):
        response = self.client.get('/kdj')
        self.assertEqual(response.status_code,200)

    def test_macd(self):
        response = self.client.get('/macd')
        self.assertEqual(response.status_code,200)

    def test_sync_last_day(self):
        response = self.client.get('/sync/daily')
        self.assertEqual(response.status_code,200)

    def test_price_data(self):
        response = self.client.get('/price_data/BIDU')
        self.assertEqual(response.status_code,200)