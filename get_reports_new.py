import os, re, datetime, time, shutil

import glob, requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from compNameDict import compNameDict
def get_HKEX_Reports(stockCode, numOfyear = 5):
    #---Download latest n years of annual and interim reports from HKEX in headless mode---
    stockCode = str(stockCode).zfill(4)
    #company might not be in dictionary (IPO etc)
    try:
        os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode} {compNameDict[stockCode]}', exist_ok=True)
        target_dir = f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode} {compNameDict[stockCode]}'
    except KeyError: 
        os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', exist_ok=True)
        target_dir = f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}'
    link = 'https://www.hkexnews.hk/index_c.htm'
    opts = ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--log-level=3")  # pop up fatal error msg only
    # opts.add_experimental_option("detach", True) #browser stay open
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\stock_Researcher\related files\chromedriver.exe', options=opts)

    #getting preliminary reports
    reportType = ['中期業績', '末期業績']  #interim, annual
    for report in reportType:
        driver.get(link)
        driver.find_element_by_id('searchStockCode').send_keys(stockCode)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='autocomplete-suggestion narrow']")))
        element.click()
        driver.find_element_by_id('tier1-select').click()
        driver.find_element_by_xpath("//*[@class='droplist-item']//*[text()='標題類別']").click()
        driver.find_element_by_id('rbAfter2006').click()
        element = driver.find_element_by_xpath(f"//*[@class='droplist-item']//*[text()='{report}']")
        driver.execute_script("arguments[0].click();", element) #click on button directly, regardless of dropdown menu visibility
        driver.find_element_by_xpath("//div[@class='filter__buttonGroup']/a[@class='btn-blue filter__btn-applyFilters-js']").click()
        div = driver.find_element_by_id("titleSearchResultPanel")
        elems = div.find_elements_by_tag_name('a')
        AR_details_regex = re.compile (r'/listedco/listconews/sehk/(\d{4}/\d{4})/.*\.pdf', re.IGNORECASE)
        for elem in elems:
            pdfUrl = elem.get_attribute("href")
            if pdfUrl != None: #exclude a tag without any links
                if AR_details_regex.search(pdfUrl) is not None: #match regex
                    dateStr = AR_details_regex.search(pdfUrl).group(1)
                    date = datetime.datetime.strptime(dateStr, '%Y/%m%d')
                    now = datetime.datetime.now()
                    if now-datetime.timedelta(days=45) <= date <= now:  #download prelimnary report only if it is published less than 45 days (ie. full report not available yet)
                        res = requests.get(pdfUrl)
                        if report == '中期業績': #Interim
                            localFileName = f'{stockCode} Prelimanary Interim Report {dateStr[:4]}.pdf'
                        else:
                            localFileName = f'{stockCode} Prelimanary Annual Report {dateStr[:4]}.pdf'
                        destPath = os.path.join(target_dir, localFileName)
                        if os.path.exists(destPath): #if pdf were downloaded b4, skip download
                            print(f'{localFileName} already exist!')
                            pass   
                        else:
                            print(f'downloading {localFileName}')     
                            with open(destPath,'wb') as pdf: #download PDF files
                                pdf.write(res.content)
                        break #getting first report is enough for prelimnary

    # #Getting annual reports and interim reports
    reportList = ['年報', '中期/半年度報告']
    for report in reportList:
        driver.get(link)
        driver.find_element_by_id('searchStockCode').send_keys(stockCode)
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='autocomplete-suggestion narrow']")))
        element.click()
        driver.find_element_by_id('tier1-select').click()
        driver.find_element_by_xpath("//*[@class='droplist-item']//*[text()='標題類別']").click()
        driver.find_element_by_id('rbAfter2006').click()
        element = driver.find_element_by_xpath(f"//*[@class='droplist-item']//*[text()='{report}']")
        driver.execute_script("arguments[0].click();", element) #click on button directly, regardless of dropdown menu visibility
        driver.find_element_by_xpath("//div[@class='filter__buttonGroup']/a[@class='btn-blue filter__btn-applyFilters-js']").click()
        div = driver.find_element_by_id("titleSearchResultPanel")
        elems = div.find_elements_by_tag_name('a')
        AR_details_regex = re.compile (r'/listedco/listconews/sehk/(\d{4})/\d{4}/.*\.pdf', re.IGNORECASE)
        count = 0
        for elem in elems:
            if count <= numOfyear-1: #default getting 5 year/period report
                pdfUrl = elem.get_attribute("href")
                if pdfUrl != None:
                    if AR_details_regex.search(pdfUrl) is not None:
                            pdfYear = AR_details_regex.search(pdfUrl).group(1) #current doc year as shown in pdfUrl
                            res = requests.get(pdfUrl)
                            if report == '年報':
                                localFileName = f'{stockCode} Annual Report {pdfYear}.pdf'
                            else:
                                localFileName = f'{stockCode} Interim Report {pdfYear}.pdf'

                            destPath = os.path.join(target_dir, localFileName)
                            if os.path.exists(destPath): #if pdf were downloaded b4, skip download
                                print(f'{localFileName} already exist!')
                                pass  
                            else:
                                print(f'downloading {localFileName}')     
                                with open(destPath,'wb') as pdf: #download PDF files
                                    pdf.write(res.content)

                            count+=1
                    else:
                        break #don't continue with other links
    os.startfile(target_dir) #open report folder when done

def delete_old_folder():
    #delete folder older than 2 weeks
    folderList = glob.glob(r'C:\Users\Fung\Downloads\Financial Reports*')
    now = datetime.datetime.now()
    for folder in folderList:
        last_access_time = os.path.getctime(folder)
        last_access_time = datetime.datetime.fromtimestamp(last_access_time) #somehow getctime return float, change it into datetime format
        if last_access_time <= now - datetime.timedelta(days=14): #if last modified time is more than 2 weeks
            shutil.rmtree(folder)

if __name__ == "__main__":
    get_HKEX_Reports(2002) #1st arg=stockCode, 2nd opt arg=num of yr report to get
    print('All reports downloaded!')
    delete_old_folder()
    print('Previous reports older than 2 weeks were removed!')