# coding=utf-8
import jsm

if __name__ == "__main__":
    import tempfile
    q = jsm.Quotes()
    c = jsm.QuotesCsv()
    for range in (jsm.DAILY, jsm.WEEKLY, jsm.MONTHLY):
        print(q.get_historical_prices(4689, range))
        c.save_historical_prices(tempfile.mktemp(dir='/tmp/'), 4689, range)
    
    print(q.get_price(4689))
    print(q.get_finance(4689))
    print(q.get_brand('0050'))
    