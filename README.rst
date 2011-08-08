Overview
========

日本の株式市場の株価・財務データを取得するツールです。

各種データは、 `Yahoo!ファイナンス <http://finance.yahoo.co.jp/>`_ からスクレイピングしています。

動作は、Python2.6 - 2.7 で確認しています。

Installation
============

以下のように、pypiからのインストールをおすすめします。::

  easy_install jsm

Usage
=====

note: 株価データを取得した際の戻り値は、QuoteDataクラスのインスタンス。

当日株価の取得::

  from jsm.quotetoday import QuoteToday
  q = QuoteToday()
  q.get(9984) # 証券コードを指定して取得。この例ではソフトバンクの株価を取得

デイリー株価の取得::

  from jsm.quote import QuoteDaily
  q = QuoteDaily()
  q.get_latest_one(9984) # 最新のデイリー株価を取得
  q.get(9984, 2) # 指定ページの株価一覧を取得
  q.get_all(9984) # 全データを取得。重いうえに負荷をかけるので注意してください。

ウィークリー株価の取得::

  from jsm.quote import QuoteWeekly
  q = QuoteWeekly()
  # デイリー株価の取得APIと同じ

マンスリー株価の取得::

  from jsm.quote import QuoteMonthly
  q = QuoteMonthly()
  # デイリー株価の取得APIと同じ

株価データをCSVファイルに保存::

  from jsm.quote import QuoteCsv, QuoteToday
  import tempfile
  q = QuoteCsv(tempfile.mktemp(dir='/tmp/'), QuoteToday()) # 第1引数に保存する場所, 第2引数に取得する株価のクラス
  q.save(9984, 2) # CSV形式で保存

note: 財務データを取得した際の戻り値は、FinanceDataクラスのインスタンス。

財務データの取得::

  from jsm.finance import Finance
  f = Finance()
  f.get(9984)

note: 銘柄データを取得した際の戻り値は、BrandDataクラスのインスタンス。

銘柄データの取得::

  from jsm.brand import Brand
  b = Brand()
  b.get_0050() # 農林・水産業
  b.get_1050() # 鉱業
  b.get_2050() # 建設業
  b.get_3050() # 食料品
  b.get_3100() # 繊維製品
  b.get_3150() # パルプ・紙
  b.get_3200() # 化学
  b.get_3250() # 医薬品
  b.get_3300() # 石油・石炭製品
  b.get_3350() # ゴム製品
  b.get_3400() # ガラス・土石製品
  b.get_3450() # 鉄鋼
  b.get_3500() # 非鉄金属
  b.get_3550() # 金属製品
  b.get_3600() # 機械
  b.get_3650() # 電気機器
  b.get_3700() # 輸送機器
  b.get_3750() # 精密機器
  b.get_3800() # その他製品
  b.get_4050() # 電気・ガス業
  b.get_5050() # 陸運業
  b.get_5100() # 海運業
  b.get_5150() # 空運業
  b.get_5200() # 倉庫・運輸関連業
  b.get_5250() # 情報・通信
  b.get_6050() # 卸売業
  b.get_6100() # 小売業
  b.get_7050() # 銀行業
  b.get_7100() # 証券業
  b.get_7150() # 保険業
  b.get_7200() # その他金融業
  b.get_8050() # 不動産業
  b.get_9050() # サービス業
  b.get_all() # 全業種

Data
====

QuoteData::

  date      # 日時
  open      # 初値
  high      # 高値
  low       # 安値
  close     # 終値
  volume    # 出来高
  adj_close # 調整後終値（株式分割後など）

FinanceData::

  market_cap        # 時価総額
  shares_issued     # 発行済株式数
  dividend_yield    # 配当利回り
  dividend_one      # 1株配当
  per               # 株価収益率
  pbr               # 純資産倍率
  eps               # 1株利益
  bps               # 1株純資産
  price_min         # 最低購入代金
  round_lot         # 単元株数
  years_high        # 年初来高値
  years_low         # 年初来安値

BrandData::

  ccode     # 証券コード
  market    # 市場
  name      # 銘柄名
  info      # 銘柄情報

