# coding=utf-8
from tests import SCODE, DATE
from jsm.quote import QuoteCsv, QuoteDaily, QuoteWeekly, QuoteMonthly
import tempfile

def test_save_latest_one():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        q = QuoteCsv(tempfile.mktemp(dir='/tmp/'), q)
        q.save_latest_one(SCODE)

def test_save_one():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        q = QuoteCsv(tempfile.mktemp(dir='/tmp/'), q)
        q.save_one(DATE, SCODE)

def test_save_all():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        q = QuoteCsv(tempfile.mktemp(dir='/tmp/'), q)
        q.save_all(SCODE)
    