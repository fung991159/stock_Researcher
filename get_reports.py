import os, re, requests, datetime, time

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_HKEX_Reports(stockCode, numOfyear = 5):
    #---Download latest n years of annual and interim reports from HKEX in headless mode---
    stockCode = str(stockCode).zfill(4)
    os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', exist_ok=True)
    link = 'http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx'
    opts = ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--log-level=3")  # pop up fatal error msg only
    # opts.add_experimental_option("detach", True) #browser stay open
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\stock_Researcher\related files\chromedriver.exe', options=opts)

    #getting preliminary reports
    reportType = ['27', '29']  #interim, annual
    for report in reportType:
        driver.get(link)
        driver.find_element_by_id('ctl00_txt_stock_code').send_keys(stockCode)
        select = Select(driver.find_element_by_id('ctl00_sel_tier_1'))
        select.select_by_value('1') #public announcments
        select = Select(driver.find_element_by_id('ctl00_sel_tier_2_group'))
        select.select_by_value('3') #Financial reports
        select = Select(driver.find_element_by_id('ctl00_sel_tier_2'))
        select.select_by_value(report)
        driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr[7]/td[3]/label/a[1]').click() 
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "ctl00_ResultPage")))
        elems = driver.find_elements_by_tag_name('a')
        AR_details_regex = re.compile (r'http://www3.hkexnews.hk/listedco/listconews/SEHK/(20\d{2}/\d{4}).*\.pdf', re.IGNORECASE)
        for elem in elems:
            pdfUrl = elem.get_attribute("href")
            if AR_details_regex.search(pdfUrl) is not None:
                dateStr = AR_details_regex.search(pdfUrl).group(1)
                date = datetime.datetime.strptime(dateStr, '%Y/%m%d')
                now = datetime.datetime.now()
                if now-datetime.timedelta(days=45) <= date <= now:  #download prelimnary report only if it is published less than 45 days (ie. full report not available yet)
                    res = requests.get(pdfUrl)
                    if report == '29': #Interim
                        localFileName = f'Prelimanary Interim Report {dateStr[:4]}.pdf'
                    else:
                        localFileName = f'Prelimanary Annual Report {dateStr[:4]}.pdf'
                    print(f'downloading {stockCode} {localFileName}')     
                    with open(os.path.join(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', localFileName),'wb') as pdf: #download PDF files
                        pdf.write(res.content)
                    break #getting first report is enough for prelimnary

    #Getting annual reports and interim reports
    reportList = ['159', '160']
    for report in reportList:
        driver.get(link)
        driver.find_element_by_id('ctl00_txt_stock_code').send_keys(stockCode)
        select = Select(driver.find_element_by_id('ctl00_sel_tier_1'))
        select.select_by_value('4') 
        select2 = Select(driver.find_element_by_id('ctl00_sel_tier_2'))
        select2.select_by_value(report)  #reports type selection
        driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr[7]/td[3]/label/a[1]').click() 
        elems = driver.find_elements_by_tag_name('a') #search for all pdf links in page
        AR_regex = re.compile (r'http://www3.hkexnews.hk/listedco/listconews/SEHK/(20\d\d).*\.pdf', re.IGNORECASE) 
        count = 0
        for elem in elems:
            if count <= numOfyear-1: #default getting 5 year/period report
                pdfUrl = elem.get_attribute("href")
                if AR_regex.search(pdfUrl) is not None:
                    pdfYear = AR_regex.search(pdfUrl).group(1) #current doc year as shown in pdfUrl
                    res = requests.get(pdfUrl)
                    if report == '159':
                        localFileName = f'Annual Report {pdfYear}.pdf'
                    else:
                        localFileName = f'Interim Report {pdfYear}.pdf'
                    print(f'downloading {stockCode} {localFileName}')     
                    with open(os.path.join(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', localFileName),'wb') as pdf: #download PDF files
                        pdf.write(res.content)
                    count+=1
            else:
                break #don't continue with other links
   
if __name__ == "__main__":
    get_HKEX_Reports(113) #1st arg=stockCode, 2nd opt arg=num of yr report to get
    print('All reports downloaded!')