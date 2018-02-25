# ProxyIpSpider

Use scrapy to crawl proxy ip from xicidaili.com

# Table structure

The folder sql include the SQL for creating the table stored the crawled information. 

# How to use 

- `scrapy crawl xici_ip_spider`

You can set this spider run hourly (such as using crontab in Linux), and it will crawl the proxy IP without duplication.