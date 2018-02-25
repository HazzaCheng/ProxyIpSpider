# ProxyIpSpider

Use scrapy to crawl proxy IP from xicidaili.com

# Table structure

The folder `sql` include the SQL for creating the table stored the crawled information. 

# How to use 

- start spider

`scrapy crawl xici_ip_spider`

You can set this spider run hourly (such as using crontab in Linux), and it will crawl the proxy IP without duplication.

- write a shell script to start spider
```
> vim get_proxy_ip.sh
```

contents:
```
#!/bin/sh

cd /home/hazzacheng/AutoRun/spider/ProxyIpSpiders
scrapy crawl xici_ip_spider
```

```
> chmod +x get_proxy_ip.sh
```

- set crontab
```
> crontab -e
```
Edit:
```
* */2 * * * /usr/bin/sh /home/hazzacheng/AutoRun/spider/get_proxy_ip.sh
# It will run it every two hours.
```

# More

The `proxy.py` and `ProxyMiddleware` provide the methods to use proxy IPs, including read them from database and add them to the requests.