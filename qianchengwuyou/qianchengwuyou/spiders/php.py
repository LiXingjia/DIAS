import scrapy
import re
from qianchengwuyou.items import QianchengwuyouItem


class qianchengwuyouSpider(scrapy.Spider):
    name = 'php'
    # allowed_domains = []
    #起始页
    start_urls = ['https://search.51job.com/list/090200,000000,0000,00,9,99,PHP%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    def parse(self, response):
        #循环搜索结果列表，提取相关内容
        for each in response.xpath('//*[@id="resultList"]/div[@class="el"]'):
            url = each.xpath('./p/span/a/@href').extract()[0]
            yield scrapy.Request(url, callback=self.parseinfo)


        #翻页
        url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if url is not None:
            page = response.urljoin(url)
            yield scrapy.Request(page, callback=self.parse)


    def parseinfo(self, response):
        item = QianchengwuyouItem()
        item['jobName'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').extract_first()
        item['jobType'] = 'php开发'
        item['company'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').extract_first()
        item['companyType'] = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/@title').extract_first()
        item['salary'] = self.transalary(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').extract_first())
        message = self.requirements(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/@title').extract_first())
        item['city'] = message['city']
        item['workingExp'] = message['workingExp']
        item['eduLevel'] = message['eduLevel']
        item['welfare'] = self.welfare(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div//text()').extract())
        item['timestate'] = self.transtime(message['timestate'])
        item['detail'] = response.url

        yield item

    def requirements(self,message):
        # 切分字符串,获取城市，工作经验，学历要求和发布日期
        information = message.split('\xa0\xa0|\xa0\xa0')
        result = dict()
        result['city'] = information[0]
        result['workingExp'] = information[1]
        if re.match(r'^招[\s\S]+', information[2]):
            result['eduLevel'] = '无'
            result['timestate'] = re.match(r'(\d+\-\d+)(发布)$', information[3]).groups()[0]
        else:
            result['eduLevel'] = information[2]
            result['timestate'] = re.match(r'(\d+\-\d+)(发布)$', information[4]).groups()[0]
        return result

    def welfare(self, message):
        result = ''
        for one in message:
            if one.strip() == '':
                continue
            else:
                result = result + one.strip() + ','
        return result

    def transalary(self, salary):
        match1 = re.match('(\d+|\d+.\d+)-(\d+|\d+.\d+)千/月', salary)
        match2 = re.match('(\d+|\d+.\d+)-(\d+|\d+.\d+)万/月', salary)
        match3 = re.match('(\d+|\d+.\d+)-(\d+|\d+.\d+)万/年', salary)
        if match1:
            result = match1.group(1)+'K-'+match1.group(2)+'K'
            return result
        elif match2:
            low = str(int(float(match2.group(1)) * 10))
            high = str(int(float(match2.group(2)) * 10))
            result = low + 'K-' + high + 'K'
            return result
        elif match3:
            low = round(float(match3.group(1)) / 12 * 10, 1)
            high = round(float(match3.group(2)) / 12 * 10, 1)
            result = str(low) + 'K-' + str(high) + 'K'
            return result
        else:
            return salary

    def transtime(self, timestate):
        result = '2019-'+timestate
        return result




