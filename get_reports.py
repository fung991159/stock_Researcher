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
    #grab input stockCode and use browser to search stock information on different sites
    stockCode = str(stockCode).zfill(4)
    os.makedirs(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}', exist_ok=True)
    link = 'http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx'
    opts = ChromeOptions() #make chrome stay open after test
    opts.add_experimental_option("detach", True) #browser stay open
    
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\stock_Researcher\related files\chromedriver.exe', chrome_options=opts)
    driver.get(link)
    driver.find_element_by_id('ctl00_txt_stock_code').send_keys(stockCode)
    select = Select(driver.find_element_by_id('ctl00_sel_tier_1'))
    select.select_by_value('4') 
    select2 = Select(driver.find_element_by_id('ctl00_sel_tier_2'))
    select2.select_by_value('159')  #annual reports
    driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr[7]/td[3]/label/a[1]').click() 
    elems = driver.find_elements_by_tag_name('a')
    AR_regex = re.compile (r'http://www3.hkexnews.hk/listedco/listconews/SEHK/(20\d\d).*\.pdf', re.IGNORECASE)
    count = 0
    for elem in elems:
        if count <= numOfyear-1:
            pdfUrl = elem.get_attribute("href")
            if AR_regex.search(pdfUrl) is not None:
                # pdfList.append(pdfUrl)
                filename = AR_regex.search(pdfUrl).group(1)
                res = requests.get(pdfUrl)
                print(f'downloading {stockCode} annual report for year {filename}')
                with open(os.path.join(f'C:\\Users\\Fung\\Downloads\\Financial Reports {stockCode}',filename+'.pdf'),'wb') as pdf:
                    pdf.write(res.content)
                count+=1
        else:
            break

if __name__ == "__main__":
    get_Reports(939)
    # print('All reports downloaded!')