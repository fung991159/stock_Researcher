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
        f'https://xueqiu.com/'
    ]

    opts = ChromeOptions() #make chrome stay open after test
    opts.add_experimental_option("detach", True)   
    opts.add_argument('disable-infobars')
    driver = webdriver.Chrome(r'C:\xampp\htdocs\Python\chromedriver.exe', chrome_options=opts)

    driver.get(links[0])
    driver.find_element_by_xpath('//*[@id="app"]/nav/div/div[1]/form/input').send_keys(stockCode.zfill(5))
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "nav__search__result__list__bd")))
    driver.find_element_by_class_name('nav__search__result__item').click()  
    driver.window_handles
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    #test
    

    #xueqiu
    print('action completed!')
if __name__ == "__main__":
    openWebPages(941)