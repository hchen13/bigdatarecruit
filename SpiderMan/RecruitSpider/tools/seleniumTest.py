from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time
import sys
import os


def lagouLogin(type = 'str'):

    driver_path = platformJudge()

    # 谷歌浏览器
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_sttings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs)
    chrome_opt.add_argument("--no-sandbox")
    chrome_opt.add_argument("--disable-setuid-sandbox")
    browser = webdriver.Chrome(driver_path,chrome_options=chrome_opt)
    # browser.set_page_load_timeout(20)
    # browser.set_script_timeout(20)
    login_url = "https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f"
    browser.get(login_url)
    elem_username = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='username']/input")
    elem_password = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='password']/input")
    elem_username.clear()
    elem_password.clear()
    elem_username.send_keys("13060029781")
    elem_password.send_keys("WXK13060029781")
    elem_password.send_keys(Keys.ENTER)

    time.sleep(1)
    if browser.current_url != login_url:
        cookie_str = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]

    cookies_str = ';'.join(item for item in cookie_str)

    cookie_name = [item['name'] for item in browser.get_cookies()]
    cookie_value = [item['value'] for item in browser.get_cookies()]
    cookies_dict = dict(zip(cookie_name,cookie_value))

    browser.close()
    cookies = cookies_str if type == "str" else cookies_dict
    return cookies,browser

def platformJudge():
    file_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    com_platform = sys.platform
    if 'win32' in com_platform:
        driver_name = "chromedriver.exe"
        file_path = os.path.join(file_dir_path, 'seleniumDriver', driver_name)
    elif "darwin" in com_platform:
        driver_name = "chromedriver"
        file_path = os.path.join(file_dir_path, 'seleniumDriver', driver_name)
    elif "linux" in com_platform:
        file_path = "/usr/local/bin/chromedriver"
    return file_path
