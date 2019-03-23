import scrapy
from zhonghuayingcaiwang.items import ZhonghuayingcaiwangItem


class zhonghuayingcaiwangSpider(scrapy.Spider):
    name = 'php'
    # allowed_domains = []
    # 起始页
    start_urls = ['http://www.chinahr.com/jobs/57197/']
    number = 0
    def parse(self, response):
        self.number = self.number + 1
        # 循环搜索结果列表，提取相关内容
        for each in response.xpath('//*[@class="resultList"]/div[@class="jobList"]'):
            item = ZhonghuayingcaiwangItem()
            item['jobName'] = "".join(each.xpath('./ul/li[1]/span[1]/a//text()').extract())
            item['jobType'] = 'php开发'
            item['company'] = each.xpath('./ul/li[1]/span[3]/a/text()').extract_first()
            item['companyType'] = each.xpath('./ul/li[2]/span[3]/em[2]/text()').extract_first()
            item['salary'] = each.xpath('./ul/li[2]/span[2]/text()').extract_first()
            info = each.xpath('./ul/li[2]/span[1]//text()').extract_first().split(']')
            item['city'] = info[0].strip().strip('[')
            try:
                item['workingExp'] = info[1].split('/')[0].strip()
                item['eduLevel'] = info[1].split('/')[1]
            except:
                continue
            item['welfare'] = ''
            item['timestate'] = each.xpath('./ul/li[1]/span[2]/text()').extract_first()
            item['detail'] = each.xpath('./ul/li[1]/span[1]/a/@href').extract_first()
            yield item

        # 翻页
        # if self.number < 10:
        url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if url is not None:
            page = response.urljoin(url)
            yield scrapy.Request(page, callback=self.parse)

