# encoding: utf-8
# python sqlite

# DB-API 2.0 interface for SQLite databases

import sqlite3
import os

'''SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说
没有独立的维护进程，所有的维护都来自于程序本身。
在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
数据库文件，而是直接打开该数据库文件。
    连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
    执行完任何操作后，都不需要提交事务的(commit)

    创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
    创建在内存上面： conn = sqlite3.connect('"memory:')

    下面我们一硬盘上面创建数据库文件为例来具体说明：
    conn = sqlite3.connect('c:\\test\\hongten.db')
    其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动

'''
# global var
# 数据库文件绝句路径
DB_FILE_PATH = 'rasp.db'
# 表名称
TABLE_NAME = 'devices'
# 是否打印sql
SHOW_SQL = True


class RBSqlite:
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径
        如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
        路径下的数据库文件的连接对象；否则，返回内存中的数据接
        连接对象'''

    def __init__(self,path):
        conn = sqlite3.connect(path)
        if os.path.exists(path) and os.path.isfile(path):
            print('硬盘上面:[{}]'.format(path))
            self.conn = conn
        else:
            conn = None
            print('内存上面:[:memory:]')
            self.conn = sqlite3.connect(':memory:')

    '''该方法是获取数据库的游标对象，参数为数据库的连接对象
    如果数据库的连接对象不为None，则返回数据库连接对象所创
    建的游标对象；否则返回一个游标对象，该对象是内存中数据
    库连接对象所创建的游标对象'''

    def get_cursor(self):
        if self.conn is not None:
            return self.conn.cursor()

    ''' 创建|删除表操作
    如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！'''

    def drop_table(self, table):
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table
            if SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            cu = self.get_cursor()
            cu.execute(sql)
            self.conn.commit()
            print('删除数据库表[{}]成功!'.format(table))
            self.close_all(cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    '''创建数据库表：'''
    def create_table(self, sql):
        if sql is not None and sql != '':
            cu = self.get_cursor()
            if SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            cu.execute(sql)
            self.conn.commit()
            print('创建数据库表[%s]成功!' % TABLE_NAME)
            self.close_all(cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def close_all(self, cu):
        '''关闭数据库游标对象和数据库连接对象'''
        if cu is not None:
            cu.close()

    def save(self, sql, data):
        '''插入数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    if SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    self.conn.commit()
                self.close_all(cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def fetchall(self, sql):
        '''查询所有数据'''
        if sql is not None and sql != '':
            cu = self.get_cursor()
            if SHOW_SQL:
                print('执行sql:[{}]'.format(sql))
            cu.execute(sql)
            r = cu.fetchall()
            if len(r) > 0:
                for e in range(len(r)):
                    print(r[e])
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def fetchone(self, sql, data):
        '''查询一条数据'''
        if sql is not None and sql != '':
            if data is not None:
                # Do this instead
                d = (data,)
                cu = self.get_cursor()
                if SHOW_SQL:
                    print('执行sql:[{}],参数:[{}]'.format(sql, data))
                cu.execute(sql, d)
                r = cu.fetchall()
                if len(r) > 0:
                    for e in range(len(r)):
                        print(r[e])
            else:
                print('the [{}] equal None!'.format(data))
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def update(self, sql, data):
        '''更新数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    if SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    self.conn.commit()
                self.close_all(cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))


    def delete(self, sql, data):
        '''删除数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    if SHOW_SQL:
                        print('执行sql:[{}],参数:[{}]'.format(sql, d))
                    cu.execute(sql, d)
                    self.conn.commit()
                self.close_all(cu)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

'''
if __name__ == '__main__':
    sqlite=RBSqlite(DB_FILE_PATH);
    sqlite.drop_table(TABLE_NAME)
    sql = ''CREATE TABLE if not EXISTS %s (
				`id` int(11) NOT NULL,
				`name` varchar(20) NOT NULL,
				`categeory` varchar(4) DEFAULT NULL,
				PRIMARY KEY (`id`)
			)'' % TABLE_NAME
    sqlite.create_table(sql)

    sql = 'SELECT * FROM %s' % TABLE_NAME
    sqlite.fetchall(sql)

    sql='select * from %s where ID = ?' % TABLE_NAME
    sqlite.fetchone(sql,1)
'''
