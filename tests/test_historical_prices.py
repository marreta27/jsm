# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
from tests import CCODE, INDEX_CODE
import jsm
import datetime
import time
from jsm.exceptions import CCODENotFoundException

def test_ccode_exception():
    q = jsm.Quotes()
    try:
        q.get_historical_prices('0000', jsm.DAILY)
    except CCODENotFoundException:
        return
    raise Exception('exception is not thrown')

def test_get_daily():
    q = jsm.Quotes()
    one = q.get_historical_prices(CCODE, jsm.DAILY)
    if not one:
        raise Exception('is None')

def test_get_weekly():
    q = jsm.Quotes()
    one = q.get_historical_prices(CCODE, jsm.WEEKLY)
    if not one:
        raise Exception('is None')

def test_get_monthly():
    q = jsm.Quotes()
    one = q.get_historical_prices(CCODE, jsm.MONTHLY)
    if not one:
        raise Exception('is None')

def test_get_range_daily():
    q = jsm.Quotes()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    one = q.get_historical_prices(CCODE, jsm.DAILY, start_date, end_date)
    if not one:
        raise Exception('is None')

def test_get_range_weekly():
    q = jsm.Quotes()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    one = q.get_historical_prices(CCODE, jsm.WEEKLY, start_date, end_date)
    if not one:
        raise Exception('is None')

def test_get_range_monthly():
    q = jsm.Quotes()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    one = q.get_historical_prices(CCODE, jsm.MONTHLY, start_date, end_date)
    if not one:
        raise Exception('is None')

def test_get_stock_split_date():
    q = jsm.Quotes()
    e = datetime.datetime(2014,6,27)
    s = datetime.datetime(2014,6,23)
    one = q.get_historical_prices(6858, jsm.DAILY, s, e)
    if len(one) != 5:
        raise Exception('invalid length')

def test_get_latest_one():
    class FixedHolidayDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2014, 7, 5)
    bak = datetime.date
    datetime.date = FixedHolidayDate # mock

    h = jsm.HistoricalDailyPrices()
    try:
        one = h.get_latest_one(CCODE)
    except:
        raise
    finally:
        datetime.date = bak
    if not one:
        raise Exception('is None')

def test_get_index_range_daily():
    q = jsm.Quotes()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    one = q.get_historical_prices(INDEX_CODE, jsm.DAILY, start_date, end_date)
    if not one:
        raise Exception('is None')
