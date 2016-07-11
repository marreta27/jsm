# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
from tests import CCODE
import jsm
import tempfile
import datetime
import time

def test_save():
    c = jsm.QuotesCsv()
    c.save_price(tempfile.mktemp(dir='/tmp/'), CCODE)

def test_save_ja_path():
    c = jsm.QuotesCsv()
    path = tempfile.mktemp(dir='/tmp/')
    path += '日本語'
    c.save_price(path, CCODE)

def test_save_range():
    c = jsm.QuotesCsv()
    start_date = datetime.date.fromtimestamp(time.time() - 604800) # 1週間前
    end_date = datetime.date.today()
    for range_type in (jsm.DAILY, jsm.WEEKLY, jsm.MONTHLY):
        c.save_historical_prices(tempfile.mktemp(dir='/tmp/'), CCODE, range_type, start_date, end_date)
