# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import jsm

def test_get_brand():
    q = jsm.Quotes()
    d = q.get_brand('0050')
    if not d:
        raise Exception('is None')
