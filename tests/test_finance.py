# coding=utf-8
from jsm.finance import Finance
from tests import SCODE

def test_get():
    f = Finance()
    d = f.get(SCODE)
    if not d:
        raise Exception('is None')
    