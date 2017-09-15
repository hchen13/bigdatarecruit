from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time

def lagouLogin(type = 'str'):
    # 火狐浏览器
    # browser = webdriver.Firefox('/usr/local/Cellar/geckodriver/0.18.0/bin/')

    # 谷歌浏览器
    chrome_opt = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_sttings.images":2}
    chrome_opt.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome('/Users/monstar/Downloads/chromedriver',chrome_options=chrome_opt)
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
