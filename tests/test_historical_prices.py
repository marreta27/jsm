# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
from tests import CCODE
import jsm
import datetime
import time

def test_get():
    q = jsm.Quotes()
    for range_type in (jsm.DAILY, jsm.WEEKLY, jsm.MONTHLY):
        one = q.get_historical_prices(CCODE, range_type)
        if not one:
            raise Exception('is None')

def test_get_range():
    q = jsm.Quotes()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    for range_type in (jsm.DAILY, jsm.WEEKLY, jsm.MONTHLY):
        one = q.get_historical_prices(CCODE, range_type, start_date, end_date)
        if not one:
            raise Exception('is None')

def test_get_all():
    q = jsm.Quotes()
    for range_type in (jsm.DAILY, jsm.WEEKLY, jsm.MONTHLY):
        all = q.get_historical_prices(CCODE, range_type, all=True)
        if not all:
            raise Exception("is None")
