#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@version: V1.0
@author: Hazza Cheng
@contact: hazzacheng@gmail.com
@time: 2018/02/23 
@file: handle_db.py
@description: Some operations for database.
@modify:
"""
import pymysql


def get_db(**kwargs):
    """
    Connect the database.
    :param kwargs:
    :return: The db source.
    """
    try:
        db = pymysql.connect(**kwargs)
    except Exception as e:
        print('Link DB error:', e)
    else:
        return db


def exec_sql(sql, data='', **kwargs):
    """
    Execute sql operations.
    :param sql:
    :param data:
    :param kwargs:
    :return:
    """
    conn = get_db(**kwargs)
    cur = conn.cursor()
    result = []
    try:
        if data == '':
            cur.execute(sql)
        else:
            cur.execute(sql, data)
        result = cur.fetchall()
        conn.commit()
    except Exception as e:
        print("DataBase Error!", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return result


def pool_exec_sql(pool, sql, data=''):
    """
    Use database pool to execute sql operations.
    :param sql:
    :param data:
    :param kwargs:
    :return:
    """
    conn = pool.connection()
    cur = conn.cursor()
    result = []
    try:
        if data == '':
            cur.execute(sql)
        else:
            cur.execute(sql, data)
        result = cur.fetchall()
        conn.commit()
    except Exception as e:
        print("DataBase Error!", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

    return result


def insert_data(data_, table, **kwargs):
    """
    Insert into database with data.
    :param data_:
    :param table:
    :param kwargs:
    :return:
    """
    insertSQL="insert into `"+table+"`(%s) values (%s)"
    keys = data_.keys()
    fields = ','.join(['`%s`' % k for k in keys])
    qm = ','.join(['%s'] * len(keys))
    sql = insertSQL % (fields, qm)
    lis = [data_[k] for k in keys]
    exec_sql(sql, lis, **kwargs)


def pool_insert_data(pool, item, table):
    """
    Use db pool to insert data.
    :param pool:
    :param item:
    :param table:
    :return:
    """
    keys = item.keys()
    fields = u','.join(keys)
    qm = u','.join([u'%s'] * len(keys))
    insert_sql = "insert into `" + table + "`(%s) values (%s)"
    sql = insert_sql % (fields, qm)
    data = [item[k] for k in keys]

    conn = pool.connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        conn.commit()
    except Exception as e:
        print('Pool Insert Error', e)
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

    return True


