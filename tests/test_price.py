# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import jsm
from tests import CCODE

def test_get():
    q = jsm.Quotes()
    d = q.get_price(CCODE)
    if not d:
        raise Exception('is None')
    