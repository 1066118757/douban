# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors


class DoubanmoviePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db='test',
                                            user='root',
                                            passwd='123456',
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=False
        )

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def _conditional_insert(self, tx, item):
        tx.execute("select * from doubanmovie where m_name= %s", (item['name'][0],))
        result = tx.fetchone()
        log.msg(result, level=log.DEBUG)
        print result
        if result:
            log.msg("Item already stored in db:%s" % item, level=log.DEBUG)
        else:
            classification = actor = ''
            lenClassification = len(item['classification'])
            lenActor = len(item['actor'])
            for n in xrange(lenClassification):
                classification += item['classification'][n]
                if n < lenClassification - 1:
                    classification += '/'
            for n in xrange(lenActor):
                actor += item['actor'][n]
                if n < lenActor - 1:
                    actor += '/'
            tags = item['tags'][0]
            tx.execute( \
                "insert into doubanmovie (m_name,m_year,m_score,m_director,m_classification,m_actor,m_summary,m_tags) values (%s,%s,%s,%s,%s,%s,%s,%s)", \
                (item['name'][0], item['year'][0], item['score'][0], item['director'][0], classification, actor,
                 item['summary'][0], tags))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)
