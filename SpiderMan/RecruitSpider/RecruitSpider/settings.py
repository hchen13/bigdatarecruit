# -*- coding: utf-8 -*-

# Scrapy settings for RecruitSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'RecruitSpider'

SPIDER_MODULES = ['RecruitSpider.spiders']
NEWSPIDER_MODULE = 'RecruitSpider.spiders'

# REDIRECT_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'RecruitSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Accept-Language': 'en',
    "Referer": "https://www.lagou.com/jobs/list_",
    "cookie":"Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504850195;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504850192;_ga=GA1.2.1169007339.1504850192;_gat=1;showExpriedCompanyHome=1;showExpriedIndex=1;PRE_UTM=;JSESSIONID=ABAAABAACBHABBI3934EE2F1FA97677EB6459A948D77F55;hasDeliver=32;unick=%E6%AD%A6%E6%99%93%E5%9D%A4;LGUID=20170908135632-76decf24-945a-11e7-9139-5254005c3644;login=true;_putrc=8F0B15F565452CFB;PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fservice%3Dhttps%253a%252f%252fwww.lagou.com%252f;LGRID=20170908135634-788fcf2b-945a-11e7-8abe-525400f775ce;_gid=GA1.2.207976112.1504850192;index_location_city=%E6%88%90%E9%83%BD;showExpriedMyPublish=1;PRE_HOST=;PRE_SITE=;X_HTTP_TOKEN=429027a4583e02a86151e9572eb67d20;LGSID=20170908135632-76decd3d-945a-11e7-9139-5254005c3644;user_trace_token=20170908135631-7fa777d9-8d08-4452-ad75-5bfe82a5b151"
}

# USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
USER_AGENT_TYPE = 'random'
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'RecruitSpider.middlewares.RecruitspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'RecruitSpider.middlewares.RandomUserAgentMiddleware': 543,
    # 'RecruitSpider.middlewares.MyProxiesSpiderMiddleware': 542,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'RecruitSpider.pipelines.RecruitSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "spider"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""