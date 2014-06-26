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
import time
import csv
import sys
from jsm.util import html_parser, debuglog
from jsm.pricebase import PriceData

class HistoricalPricesParser(object):
    """過去の株価情報ページパーサ"""
    SITE_URL = "http://info.finance.yahoo.co.jp/history/?code=%(ccode)s.T&sy=%(syear)s&sm=%(smon)s&sd=%(sday)s&ey=%(eyear)s&em=%(emon)s&ed=%(eday)s&tm=%(range_type)s&p=%(page)s"
    DATA_FIELD_NUM = 7 # データの要素数
    COLUMN_NUM = 50 # 1ページ辺り最大行数

    def __init__(self):
        self._elms = []
    
    def fetch(self, start_date, end_date, ccode, range_type, page=0):
        """対象日時のYahooページを開く
        start_date: 開始日時(datetime)
        end_date: 終了日時(datetime)
        ccode: 証券コード
        range_type: 取得タイプ（デイリー, 週間, 月間）
        page: ページ(1ページ50件に調整)
        """
        siteurl = self.SITE_URL % {'syear': start_date.year, 'smon': start_date.month, 'sday': start_date.day,
                                   'eyear': end_date.year, 'emon': end_date.month, 'eday': end_date.day,
                                   'page': page*self.COLUMN_NUM, 'range_type':range_type, 'ccode':ccode}
        fp = urlopen(siteurl)
        html = fp.read()
        fp.close()
        soup = html_parser(html)
        self._elms = soup.findAll("table", attrs={"class": "boardFin yjSt marB6"})[0].findAll("tr")[1:]
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
                    #data = [self._text(td) for td in tds]
                    data = [td.string.encode("utf-8") for td in tds]
                    data = PriceData(data[0], data[1], data[2],data[3], data[4], data[5], data[6])
                    return data
        else:
            return None
    
    def get_all(self):
        return [self.get(i) for i in range(len(self._elms))]
        
    def _text(self, soup):
        small = soup.find("small")
        if small:
            b = small.find("b")
            if sys.version_info.major < 3:
                if b:
                    return b.text.encode("utf-8")
                else:
                    return small.text.encode("utf-8")
            else:
                if b:
                    return b.text
                else:
                    return small.text
        else:
            return ""

class HistoricalPrices(object):
    """Yahooファイナンスから株価データを取得する
    """
    INTERVAL = 0.5 # 株価取得インターバル（秒）
    DAILY = "d" # デイリー
    WEEKLY = "w" # 週間
    MONTHLY = "m" # 月間
    
    def __init__(self):
        self._range_type = self.DAILY # 取得タイプ

    def get(self, ccode, page=0):
        """指定ページから一覧を取得"""
        p = HistoricalPricesParser()
        today = datetime.date.today()
        old = datetime.date(2000, 1, 1)
        p.fetch(old, today, ccode, self._range_type, page)
        return p.get_all()
    
    def get_latest_one(self, ccode):
        """最新の1件を取得"""
        p = HistoricalPricesParser()
        today = datetime.date.today()
        p.fetch(today, today, ccode, self._range_type, 0)
        return p.get()
    
    def get_one(self, ccode, date):
        """指定日時の中から1件を取得"""
        p = HistoricalPricesParser()
        p.fetch(date, date, ccode, self._range_type, 0)
        return p.get()
    
    def get_range(self, ccode, start_date, end_date):
        """指定日時間から取得"""
        p = HistoricalPricesParser()
        res = []
        for page in range(500):
            p = HistoricalPricesParser()
            p.fetch(start_date, end_date, ccode, self._range_type, page)
            data = p.get_all()
            if not data:
                break
            res.extend(data)
            time.sleep(self.INTERVAL)
        return res
        
    def get_all(self, ccode):
        """全部取得"""
        start_date = datetime.date(2000, 1, 1)
        end_date = datetime.date.today()
        res = []
        for page in range(500):
            p = HistoricalPricesParser()
            p.fetch(start_date, end_date, ccode, self._range_type, page)
            data = p.get_all()
            if not data:
                break
            res.extend(data)
            time.sleep(self.INTERVAL)
        return res

class HistoricalDailyPrices(HistoricalPrices):
    """デイリーの株価データを取得
    """
    def __init__(self):
        super(HistoricalDailyPrices, self).__init__()
        self._range_type = self.DAILY

class HistoricalWeeklyPrices(HistoricalPrices):
    """週間の株価データを取得
    """
    def __init__(self):
        super(HistoricalWeeklyPrices, self).__init__()
        self._range_type = self.WEEKLY

class HistoricalMonthlyPrices(HistoricalPrices):
    """月間の株価データを取得
    """
    def __init__(self):
        super(HistoricalMonthlyPrices, self).__init__()
        self._range_type = self.MONTHLY

class HistoricalPricesToCsv(object):
    """株データをCSVファイルに
    """
    def __init__(self, path, klass):
        self._path = path
        self._klass = klass
    
    def save(self, ccode, page=0):
        """指定ページから一覧をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        for one in self._klass.get(ccode, page):
            c.writerow(self._csv(one))
    
    def save_latest_one(self, ccode):
        """最新の1件をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        one = self._klass.get_latest_one(ccode)
        if one:
            c.writerow(self._csv(one))
    
    def save_one(self, date, ccode):
        """指定日時の中から1件をCSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        one = self._klass.get_one(ccode, date)
        if one:
            c.writerow(self._csv(one))
    
    def save_all(self, ccode):
        """全部CSV形式で保存"""
        c = csv.writer(open(self._path, 'w'))
        for one in self._klass.get_all(ccode):
            c.writerow(self._csv(one))
    
    def _csv(self, one):
        """株データをCSV形式に変換"""
        return [one.date.strftime('%Y-%m-%d'),
                one.open, one.high, one.low, 
                one.close, one.volume]
