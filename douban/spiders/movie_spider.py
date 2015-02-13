# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from demo01.items import DoubanmovieItem

class MovieSpider(CrawlSpider):

    url_list=[]
    url_list.extend(["http://movie.douban.com/tag/爱情?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/喜剧?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/动画?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/科幻?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/经典?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/剧情?start="+str(20*i) for i in xrange(40)])
    url_list.extend(["http://movie.douban.com/tag/动作?start="+str(20*i) for i in xrange(40)])

    name="demo01"
  #  allowed_domains=["movie.douban.com"]
  #  start_urls=["http://movie.douban.com/top250"]
  #  rules=[
  #      Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/top250\?start=\d+.*'))),
  #      Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+')),callback="parse_item"),
  #  ]
    start_urls=url_list
        #list(["http://movie.douban.com/tag/爱情?start="+str(20*i) for i in xrange(40)]).\
        #extend(["http://movie.douban.com/tag/喜剧?start="+str(20*i) for i in xrange(40)])\
        #.extend(["http://movie.douban.com/tag/动画?start="+str(20*i) for i in xrange(40)])\
        #.extend(["http://movie.douban.com/tag/科幻?start="+str(20*i) for i in xrange(40)])\
        #.extend(["http://movie.douban.com/tag/经典?start="+str(20*i) for i in xrange(40)])\
        #.extend(["http://movie.douban.com/tag/cult?start="+str(20*i) for i in xrange(20)])\
        #.extend(["http://movie.douban.com/tag/剧情?start="+str(20*i) for i in xrange(40)])\
        #.extend(["http://movie.douban.com/tag/动作?start="+str(20*i) for i in xrange(40)])
    rules=[
        #Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/\s+?start=\d+.*')),follow=True),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/爱情?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/tag/\s+'))),
        Rule(SgmlLinkExtractor(allow=(r'http://movie.douban.com/subject/\d+.*')),callback="parse_item"),
    ]

    def parse_item(self,response):
        sel=Selector(response)
        item=DoubanmovieItem()
        item['name']=sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year']=sel.xpath('//*[@id="content"]/h1/span[2]/text()').re(r'\((\d+)\)')
        item['score']=sel.xpath('//*[@id="interest_sectl"]/div/p[1]/strong/text()').extract()
        item['director']=sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification']= sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor']= sel.xpath('//*[@id="info"]/span[3]/span[2]/*/text()').extract()
        item['summary']=sel.xpath('//*[@id="link-report"]/span/text()').extract()
        item['tags']=sel.xpath('//*[@id="info"]/span[5]/text()').extract()
        return item
