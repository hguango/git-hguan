# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi


class LianjiaPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 名称固定 会被scrapy调用 直接可用setting的值
        # 这是链接数据库的另一种方法，在settings中写入参数
        dbpool = adbapi.ConnectionPool('pymysql',
                        host=settings['MYSQL_HOST'],
                        db=settings['MYSQL_DBNAME'],
                        user=settings['MYSQL_USER'],
                        password=settings['MYSQL_PASSWORD'],
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor,
                        use_unicode=True
                       )
        return cls(dbpool)


    def process_item(self, item, spider):
        # 使用twiest将mysql插入变成异步
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 因为异步 可能有些错误不能及时爆出
        query.addErrback(self.handle_error)

    # 处理异步的异常
    def handle_error(self, failure):
        print('failure')

    def do_insert(self, cursor, item):
        parms = self.parse_item(item)
        #print(parms)
        #lr = str(['%s'] * 16)[1:-1]
        sqlr = '''insert into lianjia(locality,url,
        title,address,housetype,floorspace,roomarea,
        floor,elevator,unitprice,totalprice,servicelife,
        propertyrigtht,concerns,lookers,publishtime)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
        # sql = sqlr % parms
        # print('_______________________________')
        # print(sql)
        cursor.execute(sqlr, parms)

    def parse_item(self, item):
        parms = (
            item['locality'],
            item['url'],
            item['title'],
            item['address'],
            item['housetype'],
            item['floorspace'],
            item['roomarea'],
            item['floor'],
            item['elevator'],
            item['unitprice'],
            item['totalprice'],
            item['servicelife'],
            item['propertyrigtht'],
            item['concerns'],
            item['lookers'],
            item['publishtime'])

        return parms
    # def _connet(self):
    #     self._conn = pymysql.connect(host='127.0.0.1',
    #                                  port=3306,
    #                                  user='root',
    #                                  passwd='password',
    #                                  db='mysql',
    #                                  charset='utf8')
    #     self._cur = self._conn.cursor()

    # def process_item(self, item, spider):
    #     parms = self.parse_item(item)
    #     #print('_______________________________')
    #     #print(parms)
    #     self._conditional_insert(parms)
    #     return item

    # def _conditional_insert(self, parms):
    #     lr = str(['%s'] * 16)[1:-1]
    #     sqlr = '''insert into lianjia values(%s) ''' % lr
    #     sql = sqlr % parms
    #     #print('_______________________________')
    #     #print(sql)
    #     self._connet()
    #     self._cur.execute(sql)
    #     self._conn.commit()
    #     self._cur.close()
    #     self._conn.close()
