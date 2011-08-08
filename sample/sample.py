# coding=utf-8
from jsm.quote import QuoteDaily, QuoteWeekly, QuoteMonthly, QuoteCsv
from jsm.quotetoday import QuoteToday
from jsm.finance import Finance

if __name__ == "__main__":
    import tempfile
    for q in (QuoteDaily(), QuoteWeekly(), QuoteMonthly()):
        print q.get_latest_one(9984)
        print q.get(9984, 2)
        c = QuoteCsv(tempfile.mktemp(dir='/tmp/'), q)
        c.save(9984, 2)
    
    q = QuoteToday()
    print q.get(9984)
    
    f = Finance()
    print f.get(9984)