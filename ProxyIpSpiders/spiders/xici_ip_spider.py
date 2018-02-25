# -*- coding: utf-8 -*-
import scrapy

from ProxyIpSpiders.items import IpItem
from ProxyIpSpiders.utils import isToday, format_TTL


class XiciIpSpider(scrapy.Spider):
    name = 'xici_ip_spider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com']

    def start_requests(self):
        reqs = []

        for i in range(1, 8):
            req = scrapy.Request('http://www.xicidaili.com/nn/%s' % i)
            reqs.append(req)

        return reqs

    def parse(self, response):
        ip_list = response.xpath('//table[@id="ip_list"]')
        trs = ip_list[0].xpath('tr')
        items = []

        for ip in trs[1:]:
            item = IpItem()
            item['IP'] = ip.xpath('td[2]/text()')[0].extract()
            item['PORT'] = int(ip.xpath('td[3]/text()')[0].extract())
            item['POSITION'] = ip.xpath('string(td[4])')[0].extract().strip()
            item['ANONYMOUS'] = ip.xpath('td[5]/text()')[0].extract()
            item['TYPE'] = ip.xpath('td[6]/text()')[0].extract()
            item['SPEED'] = float(ip.xpath('td[7]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0])
            item['LINK_TIME'] = float(ip.xpath('td[8]/div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0])
            item['TTL'] = ip.xpath('td[9]/text()')[0].extract()
            item['TTL_MINUTES'] = format_TTL(item['TTL'])
            item['LAST_CHECK_TIME'] = '20' + ip.xpath('td[10]/text()')[0].extract()
            if isToday(item['LAST_CHECK_TIME']):
                items.append(item)

        return items





