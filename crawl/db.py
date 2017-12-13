import os
import sqlite3

class Db:
    def __init__(self, db_file):
        self.db_file    = db_file
        self.table_name = 'boss'
        self.conn       = sqlite3.connect(db_file)

        self.create_db_file()
        self.create_table()

    def __del__(self):
        self.conn.close()

    def create_db_file(self):
        ''' 如果boss.db文件不存在, 则创建
        '''
        if os.path.exists(self.db_file):
            pass
        else:
            os.mknod(self.db_file)

        return True

    def create_table(self):
        ''' 创建表'''
        cursor = self.conn.cursor()
        sql = "DROP TABLE IF EXISTS '" + self.table_name + "'"
        cursor.execute(sql)

        sql = "create table %s (id integer primary key not null, area varchar(25) not null, business varchar(25) not null, salary varchar(25) not null,age varchar(25) not null, type varchar(25) not null)" % self.table_name
        cursor.execute(sql)

        cursor.close()
        self.conn.commit()

    def insert_info(self, *args):
        ''' 插入数据
        '''
        sql = "insert into boss (area, business, salary, age, type, date) values ('%s', '%s', '%s', '%s', '%s')" % args
        row = self.conn.cursor().execute(sql).rowcount
        self.conn.cursor().close()
        self.conn.commit()

        return row
