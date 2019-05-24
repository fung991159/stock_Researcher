import webbrowser, time

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def openWebPages(stockCode):
    #open web page and navagate to the stock page according to stockCode
    stockCode = str(stockCode)
    links = [
        f'https://webb-site.com/dbpub/orgdata.asp?code={stockCode}&Submit=current', #webbsite
        f'http://www.aastocks.com/tc/', #aastock
        f'https://xueqiu.com/', #xueqiu
        'http://www3.hkexnews.hk/listedco/listconews/advancedsearch/search_active_main_c.aspx'
    ]

    opts = ChromeOptions() #make chrome stay open after test
    opts.add_experimental_option("detach", True)   
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\chromedriver.exe', chrome_options=opts)
    
    for i in range(len(links)):
        if i == 0:
            driver.get(links[i])
        elif i == 1:
            driver.get(links[i])
            driver.find_element_by_id('txtHKQuote').send_keys(stockCode)
            element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "ui-menu-item")))
            element.click() #the first item in popuplist is usually right
        elif i == len(links)-2:
            driver.get(links[i])
            driver.find_element_by_xpath('//*[@id="app"]/nav/div/div[1]/form/input').send_keys(stockCode.zfill(5))
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "nav__search__result__list__bd")))
            driver.find_element_by_class_name('nav__search__result__item').click()  
        elif i == len(links)-1:   #HKEX is always at end  
            #HKEX advance stock search
            driver.get(links[i])
            driver.find_element_by_id('ctl00_txt_stock_code').send_keys(stockCode)
            driver.find_element_by_xpath('//*[@id="aspnetForm"]/table/tbody/tr[7]/td[3]/label/a[1]').click()    
        driver.execute_script("window.open();")
        driver.switch_to.window(driver.window_handles[i+1])
    #xueqiu
    print('action completed!')
if __name__ == "__main__":
    openWebPages(5)