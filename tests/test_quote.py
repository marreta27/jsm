from tests import SCODE, DATE
from jsm.quote import QuoteDaily, QuoteWeekly, QuoteMonthly

def test_get_latest_one():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        q.get_latest_one(SCODE)

def test_get_one():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        one = q.get_one(DATE, SCODE)
        if not one:
            raise Exception('is None')

def test_get_all():
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        all = q.get_all(SCODE)
        if not all:
            raise Exception("is None")
