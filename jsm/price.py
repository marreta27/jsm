# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------
import urllib2
import datetime
from jsm.util import html_parser, debuglog
from jsm.pricebase import PriceData

class PriceParser(object):
    """今日の値動きデータの情報を解析
    """
    SITE_URL = "http://quote.yahoo.co.jp/q?s=%(code)s&d=v2&esearch=1"
    DATA_FIELD_NUM = 11 # データの要素数
    
    def __init__(self):
        self._elm = None
    
    def fetch(self, code):
        """株価データを取得
        code: 証券コード
        """
        siteurl = self.SITE_URL % {'code':code}
        fp = urllib2.urlopen(siteurl)
        html = fp.read()
        fp.close()
        html = html.decode("euc_jp", "ignore").encode("utf8") # UTF-8に変換
        soup = html_parser(html)
        self._elm = soup.find("tr", attrs={"align": "right"})
        debuglog(siteurl)
    
    def get(self):
        if self._elm:
            # 有効なデータは１つ
            tds = self._elm.findAll("td")
            if len(tds) == self.DATA_FIELD_NUM:
                tds = tds[3:10] # 不要な要素を取り除く
                data = [self._text(td) for td in tds]
                data = PriceData(datetime.datetime.today(), 
                                 data[4], data[5], data[6], data[0], data[3], data[0])
                return data
        else:
            return None
    
    def _text(self, elm):
        b = elm.find("b")
        if b:
            return b.text.encode("utf-8")
        font = elm.find('font')
        if font:
            return font.text.encode("utf-8")
        return elm.text.encode("utf-8")

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

