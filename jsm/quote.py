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
import time
import csv
from jsm.util import html_parser, debuglog
from jsm.quotebase import QuoteData

class QuoteParser(object):
    """HTMLパーサー"""
    SITE_URL = "http://table.yahoo.co.jp/t?c=%(byear)s&a=%(bmon)s&b=%(bday)s&f=%(ayear)s&d=%(amon)s&e=%(aday)s&g=%(type)s&s=%(code)s&y=%(page)s&z=%(code)s.t&x=.csv"
    DATA_FIELD_NUM = 7 # データの要素数
    COLUMN_NUM = 50 # 1ページ辺り最大行数

    def __init__(self):
        self._elms = []
    
    def fetch(self, bdate, adate, code, type, page=0):
        """対象日時のYahooページを開く
        bdate: 開始日時
        ayear: 終了日時
        code: 証券コード
        type: 取得タイプ（デイリー, 週間, 月間）
        page: ページ(1ページ50件に調整)
        """
        siteurl = self.SITE_URL % {'byear': bdate.year, 'bmon': bdate.month, 'bday': bdate.day,
                                   'ayear': adate.year, 'amon': adate.month, 'aday': adate.day,
                                   'page': page*self.COLUMN_NUM, 'type':type, 'code':code}
        fp = urllib2.urlopen(siteurl)
        html = fp.read()
        fp.close()
        html = html.decode("euc_jp", "ignore").encode("utf8") # UTF-8に変換
        soup = html_parser(html)
        # <tr align=right bgcolor="#ffffff">
        self._elms = soup.findAll("tr", attrs={"align": "right", "bgcolor": "#ffffff"})
        debuglog(siteurl)
        debuglog(len(self._elms))
        
    def get(self, idx=None):
        if self._elms:
            # 有効なデータが見つかるまでループ
            if idx >= 0:
                elms = self._elms[idx:]
            else:
                elms = self._elms
            for elm in elms:
                tds = elm.findAll("td")
                if len(tds) == self.DATA_FIELD_NUM:
                    data = [self._text(td) for td in tds]
                    data = QuoteData(data[0], data[1], data[2],data[3], data[4], data[5], data[6])
                    return data
        else:
            return None
    
    def get_all(self):
        return [self.get(i) for i in xrange(len(self._elms))]
        
    def _text(self, soup):
        small = soup.find("small")
        if small:
            b = small.find("b")
            if b:
                return b.text.encode("utf-8")
            return small.text.encode("utf-8")
        else:
            return ""

class Quote(object):
    """Yahooファイナンスから株価データを取得する
    基底クラス
    """
    INTERVAL = 0.5 # 株価取得インターバル（秒）
    DAILY = "d" # デイリー
    WEEKLY = "w" # 週間
    MONTHLY = "m" # 月間
    
    def __init__(self):
        self._type = self.DAILY # 取得タイプ

    def get(self, code, page=0):
        """指定ページから一覧を取得"""
        p = QuoteParser()
        today = datetime.date.today()
        old = datetime.date(2000, 1, 1)
        p.fetch(old, today, code, self._type, page)
        return p.get_all()
    
    def get_latest_one(self, code):
        """最新の1件を取得"""
        p = QuoteParser()
        today = datetime.date.today()
        p.fetch(today, today, code, self._type, 0)
        return p.get()
    
    def get_one(self, date, code):
        """指定日時の中から1件を取得"""
        p = QuoteParser()
        p.fetch(date, date, code, self._type, 0)
        return p.get()
    
    def get_all(self, code):
        """全部取得"""
        today = datetime.date.today()
        old = datetime.date(2000, 1, 1)
        ret = []
        for page in xrange(500):
            p = QuoteParser()
            p.fetch(old, today, code, self._type, page)
            data = p.get_all()
            if not data:
                break
            ret.extend(data)
            time.sleep(self.INTERVAL)
        return ret

class QuoteDaily(Quote):
    """デイリーの株価データを取得
    """
    def __init__(self):
        super(Quote, self).__init__()
        self._type = self.DAILY

class QuoteWeekly(Quote):
    """週間の株価データを取得
    """
    def __init__(self):
        super(Quote, self).__init__()
        self._type = self.WEEKLY

class QuoteMonthly(Quote):
    """月間の株価データを取得
    """
    def __init__(self):
        super(Quote, self).__init__()
        self._type = self.MONTHLY

class QuoteCsv(object):
    """株データをCSVファイルに
    """
    def __init__(self, path, klass):
        self._path = path
        self._klass = klass
    
    def save(self, code, page=0):
        """指定ページから一覧をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        for one in self._klass.get(code, page):
            c.writerow(self._csv(one))
    
    def save_latest_one(self, code):
        """最新の1件をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        one = self._klass.get_latest_one(code)
        if one:
            c.writerow(self._csv(one))
    
    def save_one(self, date, code):
        """指定日時の中から1件をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        one = self._klass.get_one(date, code)
        if one:
            c.writerow(self._csv(one))
    
    def save_all(self, code):
        """全部CSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        for one in self._klass.get_all(code):
            c.writerow(self._csv(one))
    
    def _csv(self, one):
        """株データをCSV形式に変換"""
        return [one.date.strftime('%Y-%m-%d'),
                one.open, one.high, one.low, 
                one.close, one.volume, one.adj_close]
