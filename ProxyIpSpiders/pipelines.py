# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
from DBUtils.PooledDB import PooledDB
from scrapy.utils.project import get_project_settings

from ProxyIpSpiders import handle_db
from ProxyIpSpiders.utils import isToday

settings = get_project_settings()

# database configurations
DBKWARGS = settings.get('DBKWARGS')
IP_TABLE = settings.get('IP_TABLE')
pool = PooledDB(pymysql, 10, **DBKWARGS)


def ip_is_in_db(ip, port):
    """
    Check the ip whether in DB already.
    :param ip:
    :param port:
    :return:
    """
    sql = '''
    SELECT `ip`, `port`, `last_check_time`
    FROM `%s`
    WHERE `ip` = '%s' and `port` = '%s' 
    ''' % (IP_TABLE, ip, port)
    ips = handle_db.pool_exec_sql(pool, sql)
    if ips:
        for ip in ips:
            if isToday(ip[2]):
                return True

    return False


class DbPipeline(object):
    ip_count = 0

    @staticmethod
    def process_item(item, spider):
        if spider.name == 'xici_ip_spider':
            data = {
                'ip': item['IP'],
                'port': item['PORT'],
                'position': item['POSITION'],
                'anonymous': item['ANONYMOUS'],
                'type': item['TYPE'],
                'speed': item['SPEED'],
                'link_time': item['LINK_TIME'],
                'ttl': item['TTL'],
                'ttl_minutes': item['TTL_MINUTES'],
                'last_check_time': item['LAST_CHECK_TIME']
            }
            if not ip_is_in_db(data['ip'], data['port']):
                if handle_db.pool_insert_data(pool, data, IP_TABLE):
                    DbPipeline.ip_count += 1
                    logging.info('Data inserted!', data)

        return item

    @staticmethod
    def close_spider(spider):
        logging.info('Update %s proxy ips totally.' % DbPipeline.ip_count)
