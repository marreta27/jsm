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
import time
import sys

from jsm.util import html_parser, debuglog


class BrandData(object):
    """銘柄情報
    ccode: 証券コード
    market: 市場
    name: 銘柄名
    info: 銘柄情報
    """

    def __init__(self, ccode, market, name, info):
        self.ccode = ccode  # 証券コード
        self.market = market  # 市場
        self.name = name  # 銘柄名
        self.info = info  # 銘柄情報

    def __repr__(self):
        if sys.version_info.major < 3:
            return ('<ccode:%s market:%s name:%s info:%s>' % (
                self.ccode, self.market, self.name, self.info)).encode("utf-8")
        else:
            return '<ccode:%s market:%s name:%s info:%s>' % (
                self.ccode, self.market, self.name, self.info)


class BrandIndustryParser(object):
    """業種別銘柄データの情報を解析
    """
    SITE_URL = "http://stocks.finance.yahoo.co.jp/stocks/qi/?ids=%(ids)s&p=%(page)s"
    DATA_FIELD_NUM = 5  # データの要素数

    def __init__(self):
        self._elms = []

    def fetch(self, ids, page):
        """銘柄データを取得
        ids: 業種別ID
        page: ページ
        """
        siteurl = self.SITE_URL % {'ids': ids, 'page': page}
        fp = urlopen(siteurl)
        html = fp.read()
        fp.close()
        soup = html_parser(html)
        self._elms = soup.findAll("tr", attrs={"class": "yjM"})
        debuglog(siteurl)

    def get(self):
        if self._elms:
            res = []
            for elm in self._elms:
                tds = elm.findAll("td")
                if len(tds) == self.DATA_FIELD_NUM:
                    data = BrandData(self._text0(tds[0]),
                                     self._text1(tds[1]),
                                     self._text2(tds[2]),
                                     self._text3(tds[2]))
                    res.append(data)
            return res
        else:
            return None

    def _text0(self, elm):
        if elm.get('class') == ['center', 'yjM']:
            a = elm.find('a')
            if a:
                return a.text
        return ""

    def _text1(self, elm):
        if elm.get('class') == ['center', 'yjSt']:
            return elm.text
        return ""

    def _text2(self, elm):
        strong = elm.find('strong')
        if strong:
            if strong.get('class') == ['yjMt']:
                a = strong.find('a')
                if a:
                    return a.text
        return ""

    def _text3(self, elm):
        span = elm.find('span')
        if span:
            if span.get('class') == ['yjSt', 'profile']:
                return span.text
        return ""


class Brand(object):
    """銘柄データを取得
    """
    IDS = {'0050': '農林・水産業',
           '1050': '鉱業',
           '2050': '建設業',
           '3050': '食料品',
           '3100': '繊維製品',
           '3150': 'パルプ・紙',
           '3200': '化学',
           '3250': '医薬品',
           '3300': '石油・石炭製品',
           '3350': 'ゴム製品',
           '3400': 'ガラス・土石製品',
           '3450': '鉄鋼',
           '3500': '非鉄金属',
           '3550': '金属製品',
           '3600': '機械',
           '3650': '電気機器',
           '3700': '輸送機器',
           '3750': '精密機器',
           '3800': 'その他製品',
           '4050': '電気・ガス業',
           '5050': '陸運業',
           '5100': '海運業',
           '5150': '空運業',
           '5200': '倉庫・運輸関連業',
           '5250': '情報・通信',
           '6050': '卸売業',
           '6100': '小売業',
           '7050': '銀行業',
           '7100': '証券業',
           '7150': '保険業',
           '7200': 'その他金融業',
           '8050': '不動産業',
           '9050': 'サービス業',
    }

    def get_0050(self):
        """農林・水産業"""
        return self._get_industry('0050')

    def get_1050(self):
        """鉱業"""
        return self._get_industry('1050')

    def get_2050(self):
        """建設業"""
        return self._get_industry('2050')

    def get_3050(self):
        """食料品"""
        return self._get_industry('3050')

    def get_3100(self):
        """繊維製品"""
        return self._get_industry('3100')

    def get_3150(self):
        """パルプ・紙"""
        return self._get_industry('3150')

    def get_3200(self):
        """化学"""
        return self._get_industry('3200')

    def get_3250(self):
        """医薬品"""
        return self._get_industry('3250')

    def get_3300(self):
        """石油・石炭製品"""
        return self._get_industry('3300')

    def get_3350(self):
        """ゴム製品"""
        return self._get_industry('3350')

    def get_3400(self):
        """ガラス・土石製品"""
        return self._get_industry('3400')

    def get_3450(self):
        """鉄鋼"""
        return self._get_industry('3450')

    def get_3500(self):
        """非鉄金属"""
        return self._get_industry('3500')

    def get_3550(self):
        """金属製品"""
        return self._get_industry('3550')

    def get_3600(self):
        """機械"""
        return self._get_industry('3600')

    def get_3650(self):
        """電気機器"""
        return self._get_industry('3650')

    def get_3700(self):
        """輸送機器"""
        return self._get_industry('3700')

    def get_3750(self):
        """精密機器"""
        return self._get_industry('3750')

    def get_3800(self):
        """その他製品"""
        return self._get_industry('3800')

    def get_4050(self):
        """電気・ガス業"""
        return self._get_industry('4050')

    def get_5050(self):
        """陸運業"""
        return self._get_industry('5050')

    def get_5100(self):
        """海運業"""
        return self._get_industry('5100')

    def get_5150(self):
        """空運業"""
        return self._get_industry('5150')

    def get_5200(self):
        """倉庫・運輸関連業"""
        return self._get_industry('5200')

    def get_5250(self):
        """情報・通信"""
        return self._get_industry('5250')

    def get_6050(self):
        """卸売業"""
        return self._get_industry('6050')

    def get_6100(self):
        """小売業"""
        return self._get_industry('6100')

    def get_7050(self):
        """銀行業"""
        return self._get_industry('7050')

    def get_7100(self):
        """証券業"""
        return self._get_industry('7100')

    def get_7150(self):
        """保険業"""
        return self._get_industry('7150')

    def get_7200(self):
        """その他金融業"""
        return self._get_industry('7200')

    def get_8050(self):
        """不動産業"""
        return self._get_industry('8050')

    def get_9050(self):
        """サービス業"""
        return self._get_industry('9050')

    def get_all(self):
        """全業種全銘柄
        辞書型を返す
        {'0050': [aaa,bbb,ccc], '1050', [aaa, bbb, ccc]...etc}
        """
        ret = {}
        for ids in self.IDS.keys():
            method = getattr(self, "get_%s" % ids)
            if not method:
                continue
            ret[ids] = method()
            time.sleep(1)
        return ret

    def _get_industry(self, ids):
        """指定のIDから業種別銘柄リストを取得"""
        if not ids in self.IDS.keys():
            raise Exception('Invalid arg. %s not found.' % ids)
        p = BrandIndustryParser()
        ret = []
        for i in range(1, 31):  # 最大30ページと想定
            p.fetch(ids, i)
            data = p.get()
            if not data:
                break
            ret.extend(data)
            time.sleep(0.5)
        return ret


if __name__ == "__main__":
    from jsm.util import use_debug

    use_debug()
    b = Brand()
    print(b.get_0050())

    # test
#    markets = {}
#    data = b.get_all()
#    for (k, v) in data.items():
#        for d in v:
#            o = markets.get(d.market)
#            if o:
#                o.append(d)
#            else:
#                markets[d.market] = [d]
#    for (k, v) in markets.items():
#        print '-------------------------------------------------'
#        print k
#        print v
