#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@version: V1.0
@author: Hazza Cheng
@contact: hazzacheng@gmail.com
@time: 2018/02/25 
@file: utils.py 
@description: 
@modify: Some helpful functions.
"""
import datetime
import re


def format_TTL(TTL):
    """
    Change the time to minutes.
    :param TTL:
    :return:
    """
    minutes = 0
    if '小时' in TTL:
        minutes = int(re.match(r'\d+', TTL).group()) * 60
    elif '天' in TTL:
        minutes = int(re.match(r'\d+', TTL).group()) * 60 * 24
    else:
        minutes = int(re.match(r'\d+', TTL).group())

    return minutes


def isToday(date_str):
    """
    Check whether the last_checkt_time is today.
    :param date:
    :return:
    """
    today = datetime.datetime.today()
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    return today.year == date.year and today.month == date.month and today.day == date.day