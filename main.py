import sys

from open_web_pages import open_Webpages
from get_reports_new import get_HKEX_Reports
from fetchStockPrice import getHistory

if __name__ == "__main__":
    #stockprice as 1st argument, 2nd optional argument = running just particular functions
    if len(sys.argv) == 1:
        print('missing arguments')
        input()
    elif len(sys.argv) == 2:  # if only stock price given
        stockCode = int(sys.argv[1])
        # print('opening browser to webpages')
        # open_Webpages(stockCode)
        # print("")
        print('Connecting to HKEX website to download reports')
        get_HKEX_Reports(stockCode)
        print("")
        print('Fetching historical stock price from Yahoo Financial')
        getHistory(stockCode)
        print("")
        print('All done! :)')
    else:
        stockCode = int(sys.argv[1])
        if sys.argv[2] == 'sp':
            print('ONLY fetching stock price!')
            getHistory(stockCode)
        elif sys.argv[2] == 'rp':
            print('ONLY download HKEX reports')
            get_HKEX_Reports(stockCode)