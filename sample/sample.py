# coding=utf-8
from jsm.historicalprices import HistoricalDailyPrices, HistoricalWeeklyPrices, HistoricalMonthlyPrices, HistoricalPricesToCsv
from jsm.price import Price
from jsm.finance import Finance
from jsm.brand import Brand

if __name__ == "__main__":
    import tempfile
    for p in (HistoricalDailyPrices(), HistoricalWeeklyPrices(), HistoricalMonthlyPrices()):
        print(p.get_latest_one(4689))
        print(p.get(4689, 2))
        c = HistoricalPricesToCsv(tempfile.mktemp(dir='/tmp/'), p)
        c.save(4689, 2)
    
    p = Price()
    print(p.get(4689))
    
    f = Finance()
    print(f.get(4689))
    
    b = Brand()
    print(b.get_0050())
    print(b.get_all())
    