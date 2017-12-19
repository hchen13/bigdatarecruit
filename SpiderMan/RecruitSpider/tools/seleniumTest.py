from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import  WebDriverWait
# from scrapy.selector import Selector
import time
import codecs
import sys
import os
import json


def lagouLogin(type = 'str', *args):
    # 读取登录状态
    # login_status = os.path.exists('login.cookie')
    login_status = 0
    if login_status:
        with codecs.open('login.cookie','r') as f:
            cookies = json.load(f)
    else:
        # driver_path = platformJudge()

        # 谷歌浏览器
        # chrome_opt = Options()
        # prefs = {"profile.managed_default_content_sttings.images":2}
        # chrome_opt.add_experimental_option("prefs",prefs)
        # chrome_opt.add_argument("--no-sandbox")
        # chrome_opt.add_argument("--disable-setuid-sandbox")
        # browser = webdriver.Chrome(driver_path,chrome_options=chrome_opt)
        browser = args[0]
        # 页面加载超时时间
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

        # 找到元素就停止加载，否则刷新
        try:
            WebDriverWait(driver=browser, timeout=5).until(lambda x:x.find_element_by_id('lg_header'))
        except Exception as e:
            browser.refresh()

        if browser.current_url != login_url:
            cookie_str = [item["name"] + "=" + item["value"] for item in browser.get_cookies()]

        # cookie存入文件
        cookies_str = ';'.join(item for item in cookie_str)

        cookie_name = [item['name'] for item in browser.get_cookies()]
        cookie_value = [item['value'] for item in browser.get_cookies()]
        cookies_dict = dict(zip(cookie_name,cookie_value))

        # browser.close()
        cookies = cookies_str if type == "str" else cookies_dict
        with codecs.open("login.cookie",'w',encoding='utf-8') as f:
            if type == "str":
                f.write(cookies)
            else:
                f.write(json.dumps(cookies))

    return cookies

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
