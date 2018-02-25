#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@version: V1.0
@author: Hazza Cheng
@contact: hazzacheng@gmail.com
@time: 2018/02/22 
@file: proxy.py 
@description: Use proxy ip.
@modify: 
"""
import datetime
import logging
import traceback

import requests
from scrapy.utils.project import get_project_settings

from ProxyIpSpiders import handle_db

settings = get_project_settings()

DBKWARGS = settings.get('DBKWARGS')
IP_TABLE = settings.get('IP_TABLE')


def use_proxy(browser, proxy, url):
    """
    Open browser with proxy.
    :param browser:
    :param proxy:
    :param url:
    :return:
    """
    profile = browser.profile
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.http', proxy[0])
    profile.set_preference('network.proxy.http_port', int(proxy[1]))
    profile.set_preference('permissions.default.image', 2)
    profile.update_preferences()
    browser.profile = profile
    browser.get(url)
    browser.implicitly_wait(30)

    return browser


class Singleton(object):
    """
    Singleton class.
    """
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)

        return cls._instance


class IpProvider(Singleton):
    def __init__(self):
        today = str(datetime.date.today())
        sql = ''' 
        SELECT `ip`, `port`, `type`, `last_check_time`
        FROM `%s` 
        WHERE `last_check_time` like '%s%%' 
        AND `ttl_minutes` > 1
        AND `speed` < 5 
        ORDER BY `type` 
        ASC 
        LIMIT 5 
        ''' % (IP_TABLE, today)
        self.ips = handle_db.exec_sql(sql, **DBKWARGS)

    def del_ip(self, record):
        """
        Delete ip that cannot be used.
        :param record:
        :return:
        """
        sql = "DELETE FROM `%s` WHERE `ip` = '%s' AND `port` = '%s'" % (IP_TABLE, record[0], record[1])
        print(sql)
        res = handle_db.exec_sql(sql, **DBKWARGS)
        print(record, ' was deleted！')
        return res

    def check_ip(self, record):
        """
        Check the ip whether can be used.
        :param record:
        :return:
        """
        http_url = 'http://www.baidu.com/'
        https_url = 'https://github.com/'
        proxy_type = record[2].lower()
        url = http_url if proxy_type == 'http' else https_url
        proxy_ip = '%s:%s' % (record[0], record[1])
        proxy_dict = {
            proxy_type: proxy_ip
        }
        try:
            res = requests.get(url=url, proxies=proxy_dict, timeout=10)
            with open('html/' + proxy_ip + '.html') as f:
                f.write(res.content)
        except Exception as e:
            logging.error('Request Error: ' + traceback.format_exc())
            self.del_ip(record)
            return False
        else:
            code = res.status_code
            if 200 <= code < 300:
                logging.info('Effective proxy %s://%s:%s' % (record[2], record[0], record[1]))
                return True
            else:
                logging.info('Invalide proxy %s://%s:%s' % (record[2], record[0], record[1]))
                self.del_ip(record)
                return False

    def get_ips(self):
        """
        Get ips from database.
        :return:
        """
        print('Start to get ips...')
        http = [h[0:2] for h in self.ips if h[2] == 'HTTP' and self.check_ip(h)]
        https = [h[0:2] for h in self.ips if h[2] == 'HTTPS' and self.check_ip(h)]
        logging.info('Get %s effective proxy IPs.' % (len(http) + len(https)))

        return {'http': http, 'https': https}

