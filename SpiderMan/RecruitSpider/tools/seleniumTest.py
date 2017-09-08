from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import time
# 火狐浏览器
# browser = webdriver.Firefox('/usr/local/Cellar/geckodriver/0.18.0/bin/')
browser = webdriver.Chrome('/Users/monstar/Downloads/chromedriver')
login_url = "https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f"
browser.get(login_url)
elem_username = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='username']/input")
elem_password = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='password']/input")
elem_username.clear()
elem_password.clear()
elem_username.send_keys("13622031255")
elem_password.send_keys("WXK1991327")
elem_password.send_keys(Keys.ENTER)

time.sleep(1)
if browser.current_url != login_url:
    cookie = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]

cookiestr = ';'.join(item for item in cookie)
print(cookiestr)
# browser.close()