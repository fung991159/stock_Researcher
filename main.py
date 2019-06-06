import sys

from open_web_pages import open_Webpages
from get_reports import get_HKEX_Reports
from fetchStockPrice import getHistory

if __name__ == "__main__":
    #should take stock price as first argument, default to run all process, second arugment to choose run which process
    if len(sys.argv) > 1:
        stockCode = int(sys.argv[1])
        print('opening browser to webpages')
        open_Webpages(stockCode)
        print('Connecting to HKEX website to download reports')
        get_HKEX_Reports(stockCode)
        print('Fetching historical stock price from Yahoo Financial')
        getHistory(stockCode)
        print('All done! :)')
    else:
        print('missing arguments')
        input()