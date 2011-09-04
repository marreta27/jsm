# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import jsm

def test_parser():
    q = jsm.Quotes()
    result = q.search('NTT')
    assert result[0].ccode == '9437'
    