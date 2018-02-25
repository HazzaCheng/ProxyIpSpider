# -*- coding: utf-8 -*-

BOT_NAME = 'ProxyIpSpiders'

SPIDER_MODULES = ['ProxyIpSpiders.spiders']
NEWSPIDER_MODULE = 'ProxyIpSpiders.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 301,
    'ProxyIpSpiders.middlewares.FakeUserAgentMiddleware': 543,
}

ITEM_PIPELINES = {
    'ProxyIpSpiders.pipelines.DbPipeline': 400,
}

# Configure log file name
LOG_FILE = "scrapy.log"
# LOG_STDOUT = False

# database connection parameters
DBKWARGS={'db': 'my_data_db', 'user': 'hazza', 'passwd': 'cheng55', 'host': 'localhost', 'use_unicode': True, 'charset': 'utf8'}
IP_TABLE = 'proxy_ip'

