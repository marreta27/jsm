# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
import datetime
import time
import csv
from jsm.price import Price
from jsm.historicalprices import HistoricalPrices, HistoricalDailyPrices,\
    HistoricalWeeklyPrices, HistoricalMonthlyPrices
from jsm.finance import Finance
from jsm.brand import Brand
from jsm.search import Search
from jsm.util import to_utf8, to_unicode

VERSION = '0.6'

# RangeType
DAILY = 0
WEEKLY = 1
MONTHLY = 2

class Quotes(object):
    """株式情報取得"""
    
    def get_price(self, ccode):
        """現在の株価を取得
        ccode: 証券コード
        """
        ccode = to_utf8(ccode)
        p = Price()
        return p.get(ccode)
    
    def get_historical_prices(self, ccode, range_type=DAILY, start_date=None, end_date=None, all=False):
        """過去の株価情報を取得
        ccode: 証券コード
        range_type: 取得タイプ(RANGE_DAILY, RANGE_WEEKLY, RANGE_MONTHLY)
        start_date: 取得開始日時(default: end_dateから1ヶ月前)
        end_date: 取得終了日時(default: 今日)
        all: Trueなら全データ取得
        """
        ccode = to_utf8(ccode)
        if range_type == DAILY:
            p = HistoricalDailyPrices()
        elif range_type == WEEKLY:
            p = HistoricalWeeklyPrices()
        elif range_type == MONTHLY:
            p = HistoricalMonthlyPrices()
        else:
            raise Exception('Illegal range type: %s' % range_type)
        
        if all:
            return p.get_all(ccode)
        
        if not end_date:
            end_date = datetime.date.today()
        if not start_date:
            start_date = datetime.date.fromtimestamp(time.mktime(end_date.timetuple()) - 2592000)
        return p.get_range(ccode, start_date, end_date)
    
    def get_finance(self, ccode):
        """財務データを取得
        """
        ccode = to_utf8(ccode)
        f = Finance()
        return f.get(ccode)
        
    def get_brand(self, brand_id=None):
        """業種別銘柄リストを取得
        brand_id: 業種種類
                '0050': 農林・水産業
                '1050': 鉱業
                '2050': 建設業
                '3050': 食料品
                '3100': 繊維製品
                '3150': パルプ・紙
                '3200': 化学
                '3250': 医薬品
                '3300': 石油・石炭製品
                '3350': ゴム製品
                '3400': ガラス・土石製品
                '3450': 鉄鋼
                '3500': 非鉄金属
                '3550': 金属製品
                '3600': 機械
                '3650': 電気機器
                '3700': 輸送機器
                '3750': 精密機器
                '3800': その他製品
                '4050': 電気・ガス業
                '5050': 陸運業
                '5100': 海運業
                '5150': 空運業
                '5200': 倉庫・運輸関連業
                '5250': 情報・通信
                '6050': 卸売業
                '6100': 小売業
                '7050': 銀行業
                '7100': 証券業
                '7150': 保険業
                '7200': その他金融業
                '8050': 不動産業
                '9050': サービス業
                None: 全業種
        """
        brand_id = to_utf8(brand_id)
        b = Brand()
        if not brand_id:
            return b.get_all()
        return getattr(b, 'get_%s' % brand_id)()
    
    def search(self, terms):
        """銘柄検索"""
        terms = to_utf8(terms)
        s = Search()
        return s.get(terms)
        
class QuotesCsv(object):
    """株式情報取得してCSVに保存"""
    
    def save_price(self, path, ccode):
        path = to_unicode(path)
        q = Quotes()
        price = q.get_price(ccode)
        c = csv.writer(open(path, 'w'))
        c.writerow(self._price_to_csvl(price))
    
    def save_historical_prices(self, path, ccode, range_type=DAILY, start_date=None, end_date=None, all=False):
        """過去の株価情報をCSVファイルに保存
        ccode: 証券コード
        range_type: 取得タイプ(RANGE_DAILY, RANGE_WEEKLY, RANGE_MONTHLY)
        start_date: 取得開始日時(default: end_dateから1ヶ月前)
        end_date: 取得終了日時(default: 今日)
        all: Trueなら全データ取得
        """
        path = to_unicode(path)
        q = Quotes()
        prices = q.get_historical_prices(ccode, range_type, start_date, end_date, all)
        c = csv.writer(open(path, 'w'))
        for price in prices:
            c.writerow(self._price_to_csvl(price))
    
    def _price_to_csvl(self, price):
        """株データをCSV形式に変換"""
        return [price.date.strftime('%Y-%m-%d'),
                price.open, price.high, price.low, 
                price.close, price.volume]


