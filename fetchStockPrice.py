import datetime, os

import pandas as pd
from pandas import ExcelWriter
import openpyxl
from yahoo_historical import Fetcher

def getHistory(stockCode):
        stockCode = str(stockCode).zfill(4)
        os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', exist_ok=True)
        dst = f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}\\historical price {stockCode}.xlsx' #result destination
        
        now = datetime.datetime.now()
        year= int(now.year)
        month = int(now.month)
        date = int(now.day)
        stockData = Fetcher(stockCode+'.hk', [1990,4,1], [year,month,date])

        df = stockData.getHistorical()
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d') #change date column from string to date
        df.Date=df.Date.dt.strftime('%Y') #change date format to Year for pivot table
        pt= pd.pivot_table(df, values='Close', index=['Date'],    #Get Max and low stock price group by each year
                        aggfunc={'Close':[min, max]})
        sortedPT = pt.sort_values('Date',axis=0,ascending=False)
        writer = ExcelWriter(dst)
        sortedPT.T.to_excel(writer,'Sheet1')
        writer.save()

        #reformat result to desire format
        wb = openpyxl.load_workbook(dst)
        ws = wb.active
        lastCol = ws.max_column
        for i in range(lastCol,2,-1):      
                ws.insert_cols(i,2)
        wb.save(dst)
        os.startfile(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}') #open report folder
if __name__ == "__main__":
    getHistory(87)
