## SpiderMan
SpiderMan是招聘大数据的爬虫部分。抓取拉勾网，51job，智联招聘的每天最新的职位信息

[TOC]

### 项目结构
-------------------------------------------------
>* DBFile   			项目数据库文件
>* ScriptFile  		项目有关定时、数据处理脚本文件
>* RecruitSpider 	爬虫项目代码目录

### 安装第三方库
	pip install scrapy pyvirtualdisplay fake-useragent selenium sqlalchemy requests pinyin redis mmh3
	系统需要安装redis
	系统安装 Xvfb虚拟显示环境
		* Ubuntu apt install Xvfb
		* Centos yum install Xvfb
	安装mysqlclient
		* Ubuntu下： 
			执行apt-get install libmysqlclient-devl
		* centos下： 
			Yum install python-devel mysql-devel 
		* pip install mysqlclient
	
### 在linux环境下安装chrome浏览器和chromedriver
```
# Versions
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
SELENIUM_STANDALONE_VERSION=3.4.0
SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)

# Remove existing downloads and binaries so we can start from scratch.
rm ~/google-chrome-stable_current_amd64.deb
rm ~/selenium-server-standalone-*.jar
rm ~/chromedriver_linux64.zip
sudo rm /usr/local/bin/chromedriver
sudo rm /usr/local/bin/selenium-server-standalone.jar

# Install dependencies.
sudo apt-get update
sudo apt-get install -y unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4

# Install Chrome.
wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P ~/
sudo dpkg -i --force-depends ~/google-chrome-stable_current_amd64.deb
sudo apt-get -f install -y
sudo dpkg -i --force-depends ~/google-chrome-stable_current_amd64.deb

# Install ChromeDriver.
wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver

# Install Selenium.
wget -N http://selenium-release.storage.googleapis.com/$SELENIUM_SUBDIR/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar -P ~/
sudo mv -f ~/selenium-server-standalone-$SELENIUM_STANDALONE_VERSION.jar /usr/local/bin/selenium-server-standalone.jar
sudo chown root:root /usr/local/bin/selenium-server-standalone.jar
sudo chmod 0755 /usr/local/bin/selenium-server-standalone.jar
```

### 爬虫配置介绍
#### 拉钩
>* 配置数据库 settings.py 和 tools/getFileName.py 中的数据库
>* spider/lagou.py 参数 spider_type  1 爬取全部城市 2 （默认）爬取热门城市和数据不全的城市
>* spider/lagou.py 参数 order_type  1 （默认）顺着爬 2 从最后一页往前爬
>* spider/lagou.py 参数 catch_city 指定要爬取的城市 空数组则按默认规则爬取
* middlewares.py 中的fake_useragent （默认关闭）随机user_agent

#### 智联招聘 （三种抓取模式，在configure表中选择full_city_status参数）
>* 1、全部城市全部页面
>* 2、指定爬取城市 （指定城市在default_city参数中增加，类型为城市名的pinyin）
>* 3、全部城市最新未录取职位

#### 51job （三种模式 配置字段为catch_type）
>* 1、当天数据
>* 2、全站数据
>* 3、制定城市
>* default_city 	指定城市

ps:51job是一个分布式爬虫，利用redis做任务分发机制，其中去重算法是bloomfilter


