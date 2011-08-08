# coding=utf-8
from jsm.quotetoday import QuoteToday
from tests import SCODE

def test_get():
    q = QuoteToday()
    d = q.get(SCODE)
    if not d:
        raise Exception('is None')
    