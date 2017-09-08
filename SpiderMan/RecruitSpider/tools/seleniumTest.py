from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector

# 火狐浏览器
# browser = webdriver.Firefox('/usr/local/Cellar/geckodriver/0.18.0/bin/')
browser = webdriver.Chrome('/Users/monstar/Downloads/chromedriver')
browser.get("https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f")
elem_username = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='username']/input")
elem_password = browser.find_element_by_xpath("//form[@class='active']/div[@data-propertyname='password']/input")
elem_username.clear()
elem_password.clear()
elem_username.send_keys("13622031255")
elem_password.send_keys("WXK1991327")
elem_password.send_keys(Keys.ENTER)
# browser.close()