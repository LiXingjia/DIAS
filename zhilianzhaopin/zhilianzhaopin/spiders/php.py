import scrapy
import json
import re
from zhilianzhaopin.items import ZhilianzhaopinItem


class phpSpider(scrapy.Spider):
    name = 'php'
    # allowed_domains = []
    #起始页
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=801&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=php&kt=3&_v=0.12879281&x-zp-page-request-id=679576663f3843d8b80d670a4c280749-1545831661736-20888']
    number = 0
    def parse(self, response):
        #循环结果列表，提取相关内容
        data = json.loads(response.text)['data']
        numFound = data['numFound']
        self.number = self.number + 1
        for each in data['results']:
            item = ZhilianzhaopinItem()

            item['jobName'] = each['jobName']
            item['jobType'] = each['jobType']['display']
            item['company'] = each['company']['name']
            item['companyType'] = each['company']['type']['name']
            item['salary'] = each['salary']
            item['city'] = each['city']['display']
            item['workingExp'] = each['workingExp']['name']
            item['eduLevel'] = each['eduLevel']['name']
            item['welfare'] = ",".join(each['welfare'])
            item['timestate'] = each['timeState']
            item['detail'] = each['positionURL']
            yield item
        #翻页
        start = self.number * 90 - 1
        if start < numFound:
            start = str(start)
            url = 'https://fe-api.zhaopin.com/c/i/sou?start='+start+'&pageSize=90&cityId=801&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=php&kt=3&_v=0.12879281&x-zp-page-request-id=679576663f3843d8b80d670a4c280749-1545831661736-20888'
            page = response.urljoin(url)
            yield scrapy.Request(page, callback=self.parse)

    # 把工资转换成5000-6000这种格式的
    # def transalary(self, salary):
    #     print(salary)
    #     match1 = re.match(r'(\d+|\d+.\d+)K-(\d+|\d+.\d+)K', salary)
    #     low = str(int(float(match1.group(1)) * 1000))
    #     high = str(int(float(match1.group(2)) * 1000))
    #     result = low + '-' + high
    #     return result





