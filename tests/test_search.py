# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import jsm

def test_search():
    q = jsm.Quotes()
    result = q.search('グリー')
    assert result[0].ccode == '3632'
    result = q.search('3632')
    assert result[0].ccode == '3632'
    result = q.search('NTTドコモ')
    assert result[0].ccode == '9437'
    