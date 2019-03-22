import scrapy
import re
import time
from bosszhipin.items import BosszhipinItem


class bosszhipinSpider(scrapy.Spider):
    name = 'php'
    # allowed_domains = []
    #起始页
    start_urls = ['https://www.zhipin.com/job_detail/?query=PHP&scity=101270100&industry=&position=']

    def parse(self, response):
        # 循环搜索结果列表，提取相关内容
        for each in response.xpath('//div[@class = "job-list"]/ul/li'):
            item = BosszhipinItem()
            item['jobName'] = each.xpath('./div/div[1]/h3/a/div[1]/text()').extract_first()
            item['jobType'] = 'php开发'
            item['company'] = each.xpath('./div/div[2]/div/h3/a/text()').extract_first()
            item['companyType'] = each.xpath('./div/div[2]/div/p/text()[1]').extract_first()
            item['salary'] = self.transalary(each.xpath('./div/div[1]/h3/a/span/text()').extract_first())
            item['city'] = each.xpath('./div/div[1]/p/text()[1]').extract_first()
            item['workingExp'] = each.xpath('./div/div[1]/p/text()[2]').extract_first()
            item['eduLevel'] = each.xpath('./div/div[1]/p/text()[3]').extract_first()
            item['welfare'] = ' '
            item['timestate'] = self.trantime(each.xpath('./div/div[3]/p/text()').extract_first())
            item['detail'] = response.urljoin(each.xpath('./div/div[1]/h3/a/@href').extract_first())

            yield item


        #翻页
        url = response.xpath('//a[@class = "next"]/@href').extract_first()
        if url is not None:
            page = response.urljoin(url)
            yield scrapy.Request(page, callback=self.parse)

    def trantime(self, date):
        match1 = re.match(r'(发布于)(\d+月\d+)日', date)
        if match1:
            timestate = match1.group(2).replace('月', '-')
            return timestate
        elif date == "发布于昨天":
            timestate = str(time.strftime("%m-%d", time.localtime()))
            return timestate


    def transalary(self, salary):
        match1 = re.match(r'(\d+)k-(\d+)k', salary)
        low = str(int(match1.group(1))*1000)
        high = str(int(match1.group(2))*1000)
        result = low + '-' + high
        return result












