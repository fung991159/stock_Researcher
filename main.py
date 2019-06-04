import sys

from open_web_pages import open_Webpages
from get_reports import get_HKEX_Reports
from fetchStockPrice import getHistory

#should take stock price as first argument, defautl to run all process, second arugment to choose run which process

stockCode = 543

if __name__ == "__main__":
    print('opening browser to webpages')
    open_Webpages(stockCode)
    print('Connecting to HKEX website to download reports')
    get_HKEX_Reports(stockCode)
    print('Fetching historical stock price from Yahoo Financial')
    getHistory(stockCode)
    print('All done! :)')