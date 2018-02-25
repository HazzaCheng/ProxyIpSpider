# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from ProxyIpSpiders.proxy import IpProvider


class ProxyipspidersSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyipspidersDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):
    """
    Randomly rotate user agents based on a list of predefined ones.
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ProxyMiddleware(object):

    def __init__(self):
        self.http_i = 0
        self.https_i = 0
        self.ips = IpProvider().get_ips()
        self.http_len = len(self.ips['http'])
        self.https_len = len(self.ips['https'])

    def process_request(self, request, spider):
        if spider.name != 'xici_ip_spider':
            if request.url.startswith("http://") and self.ips['http']:
                i = self.http_i
                ip = self.ips['http'][i]
                request.meta['proxy'] = "http://%s:%d" % (ip[0], int(ip[1]))
                logging.info('Use proxy ip No.%s - %s' % (i, str(ip)))
                self.http_i = (i + 1) % self.http_len

            if request.url.startswith("https://") and self.ips['https']:
                i = self.https_i
                ip = self.ips['https'][i]
                request.meta['proxy'] = "https://%s:%d" % (ip[0], int(ip[1]))
                logging.info('Use proxy ip No.%s - %s' % (i, str(ip)))
                self.https_i = (i + 1) % self.https_len

        return None
