import os, re, requests

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_Reports(stockCode, numOfyear = 5):
    #Download latest n years of annual and interim reports from HKEX in headless mode
    stockCode = str(stockCode).zfill(4)
    os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', exist_ok=True)
    link = 'http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx'
    opts = ChromeOptions() #make chrome stay open after test
    opts.add_argument("--headless")
    # opts.add_experimental_option("detach", True) #browser stay open
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\stock_Researcher\related files\chromedriver.exe', chrome_options=opts)
    reportList = ['159', '160'] #annual reports and interim reports
    for report in reportList:
        driver.get(link)
        driver.find_element_by_id('ctl00_txt_stock_code').send_keys(stockCode)
        select = Select(driver.find_element_by_id('ctl00_sel_tier_1'))
        select.select_by_value('4') 
        select2 = Select(driver.find_element_by_id('ctl00_sel_tier_2'))
        select2.select_by_value(report)  #annual reports
        driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr[7]/td[3]/label/a[1]').click() 
        elems = driver.find_elements_by_tag_name('a') #search for all pdf links in page
        AR_regex = re.compile (r'http://www3.hkexnews.hk/listedco/listconews/SEHK/(20\d\d).*\.pdf', re.IGNORECASE) 
        count = 0
        for elem in elems:
            if count <= numOfyear-1:
                pdfUrl = elem.get_attribute("href")
                if AR_regex.search(pdfUrl) is not None:
                    pdfYear = AR_regex.search(pdfUrl).group(1)
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
                break
    
if __name__ == "__main__":
    get_Reports(87)
    print('All reports downloaded!')