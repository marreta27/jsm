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
import re
from jsm.util import html_parser, debuglog

class FinanceData(object):
    def __init__(self, market_cap, shares_issued, dividend_yield, dividend_one, 
                         per, pbr, eps, bps, price_min, round_lot, years_high, years_low):
        self.market_cap = self._int(market_cap) # 時価総額
        self.shares_issued = self._int(shares_issued) # 発行済株式数
        self.dividend_yield = self._float(dividend_yield) # 配当利回り
        self.dividend_one = self._float(dividend_one) # 1株配当
        self.per = self._float(per) # 株価収益率
        self.pbr = self._float(pbr) # 純資産倍率
        self.eps = self._float(eps) # 1株利益
        self.bps = self._float(bps) # 1株純資産
        self.price_min = self._int(price_min) # 最低購入代金
        self.round_lot = self._int(round_lot, 1) # 単元株数
        self.years_high = self._int(years_high) # 年初来高値
        self.years_low = self._int(years_low) # 年初来安値
    
    def _parse(self, val, default=0):
        m = re.search('(-|)[0-9,\.]+', val)
        if m:
            return m.group(0).replace(',', '')
        return default
    
    def _int(self, val, default=0):
        return int(self._parse(val, default))
    
    def _float(self, val, default=0.0):
        return float(self._parse(val, default))
        
    def __repr__(self):
        return '<market_cap:%s shares_issued:%s dividend_yield:%.2f dividend_one:%.2f '\
                'per:%.2f pbr:%.2f eps:%.2f bps:%.2f ' \
                'price_min:%s round_lot:%s years_high:%s years_low:%s>' % (
                self.market_cap, self.shares_issued, self.dividend_yield, self.dividend_one,
                self.per, self.pbr, self.eps, self.bps,
                self.price_min, self.round_lot, self.years_high, self.years_low
                )

class FinanceParser(object):
    """財務データの情報を解析
    """
    SITE_URL = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=%(code)s"
    DATA_FIELD_NUM = 12 # データの要素数
    
    def __init__(self):
        self._elm = None
    
    def fetch(self, code):
        """財務データを取得
        code: 証券コード
        """
        siteurl = self.SITE_URL % {'code':code}
        fp = urllib2.urlopen(siteurl)
        html = fp.read()
        fp.close()
        html = html.decode("euc_jp", "ignore").encode("utf8") # UTF-8に変換
        soup = html_parser(html)
        self._elm = soup.find("div", attrs={"class": "chartFinance"})
        debuglog(siteurl)

    def get(self):
        if self._elm:
            # 有効なデータは１つ
            elms = self._elm.findAll("div")
            if len(elms) == self.DATA_FIELD_NUM:
                data = [self._text(elm) for elm in elms]
                data = FinanceData(data[0], data[1], data[2], data[3],
                                    data[4], data[5], data[6], data[7],
                                    data[8], data[9], data[10], data[11])
                return data
        else:
            return None
    
    def _text(self, elm):
        dd = elm.find("dd", attrs={"class": "ymuiEditLink mar0"})
        if dd:
            strong = dd.find("strong")
            if strong:
                return strong.text.encode("utf-8")
        return ""

class Finance(object):
    """財務データを取得
    """
    def get(self, code):
        """指定の証券コードから取得"""
        p = FinanceParser()
        p.fetch(code)
        return p.get()

if __name__ == "__main__":
    f = Finance()
    print f.get(9984)
    print f.get(2121)
