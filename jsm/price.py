# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
try:
    # For Python3
    from urllib.request import urlopen
except ImportError:
    # For Python2
    from urllib2 import urlopen
import datetime
from jsm.util import html_parser, debuglog
from jsm.pricebase import PriceData


class PriceParser(object):
    """今日の値動きデータの情報を解析
    """
    SITE_URL = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=%(code)s"

    def __init__(self):
        self._elm = None

    def fetch(self, code):
        """株価データを取得
        code: 証券コード
        """
        siteurl = self.SITE_URL % {'code': code}
        fp = urlopen(siteurl)
        html = fp.read()
        fp.close()
        soup = html_parser(html)
        self._elm = soup.findAll("dd", attrs={"class": "ymuiEditLink mar0"})
        debuglog(siteurl)

    def get(self):
        if self._elm:
            data = [self._text(tr) for tr in self._elm]
            return PriceData(
                date=datetime.datetime.today(), close=data[0], open=data[1],
                high=data[2], low=data[3], volume=data[4], adj_close=data[0])
        else:
            return None

    def _text(self, elm):
        """strong及びfontタグを取り除く
        """
        text = elm.find('strong')
        if not text:
            font = elm.find('font')
        if not text:
            return elm.text
        return text.text.replace(',', '')


class Price(object):
    """今日の値動きデータを取得
    """
    def get(self, code):
        """指定の証券コードから取得"""
        p = PriceParser()
        p.fetch(code)
        return p.get()

if __name__ == "__main__":
    p = Price()
    print(p.get(4689))
