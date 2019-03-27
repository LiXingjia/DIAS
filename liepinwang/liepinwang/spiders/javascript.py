import scrapy
import re
import datetime
import time
from liepinwang.items import LiepinwangItem


class bosszhipinSpider(scrapy.Spider):
    name = 'js'
    # allowed_domains = []
    #起始页
    start_urls = ['https://www.liepin.com/zhaopin/?imscid=R000000035&key=Javascript&dqs=280020']


    def parse(self, response):
        # 循环搜索结果列表，提取相关内容
        for each in response.xpath('//ul[@class="sojob-list"]/li'):
            item = LiepinwangItem()
            item['jobName'] = each.xpath('./div/div[1]/h3/a/text()').extract_first().strip()
            item['jobType'] = 'javascript'
            item['company'] = each.xpath('./div/div[2]/p[1]/a/text()').extract_first()
            item['companyType'] = self.company(each.xpath('./div/div[2]/p[2]//text()').extract())
            info = each.xpath('./div/div[1]/p[1]/@title').extract_first().split('_')
            item['salary'] = self.transalary(info[0])
            item['city'] = info[1]
            item['workingExp'] = info[3]
            item['eduLevel'] = info[2]
            item['welfare'] = self.welfare(each.xpath('./div/div[2]/p[3]//text()').extract())
            item['timestate'] = self.transtime(each.xpath('./div/div[1]/p[2]/time/text()').extract_first())
            item['detail'] = response.urljoin(each.xpath('./div/div[1]/h3/a/@href').extract_first())

            yield item


        #翻页
        url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if url is not None:
            page = response.urljoin(url)
            yield scrapy.Request(page, callback=self.parse)

    def welfare(self, info):
            result = ''
            for i in info:
                if i.strip() == '':
                    continue
                else:
                    result = result + i + ','
            return result.strip(',')

    def company(self, company_type):
            result = ''
            for i in company_type:
                if i.strip() == '':
                    continue
                else:
                    result = result + i.strip() + ','
            return result.strip(',')

    def transtime(self, timestate):
        if timestate == '前天':
            today = datetime.date.today()
            twoday = datetime.timedelta(days=2)
            the_day_before_yesterday = today - twoday
            return the_day_before_yesterday
        elif timestate == '昨天':
            today = datetime.date.today()
            oneday = datetime.timedelta(days=1)
            yesterday = today - oneday
            return yesterday
        elif re.match('\d+小时前|\d+分钟前', timestate):
            today = datetime.date.today()
            return today
        else:
            return timestate

    def transalary(self, salary):
        match1 = re.match(r'(\d+)-(\d+)万', salary)
        if match1:
            low = round(float(match1.group(1)) / 12 * 10, 1)
            high = round(float(match1.group(2)) / 12 * 10, 1)
            result = str(low)+'K-'+str(high)+'K'
            return result
        else:
            return salary





