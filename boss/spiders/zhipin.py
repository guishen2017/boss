import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem
from boss.common import get_md5
import re

class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/']

    rules = (
        #https://www.zhipin.com/c101280100-p100101/
        Rule(LinkExtractor(allow=r'.*/c\d+-p\d+/'),follow=True),
        # https://www.zhipin.com/gongsir/a67b361452e384e71XV82N4~.html
        Rule(LinkExtractor(allow=r'.*/gongsir/.*\.html'), follow=True),
        #https://www.zhipin.com/job_detail/30451994e407800b1n1z2Nq0Fls~.html
        Rule(LinkExtractor(allow=r'.*/job_detail/.*\.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        position_name = response.xpath('//div[@class="name"]/h1/text()').get()
        salary = response.xpath('//div[@class="info-primary"]//span[@class="badge"]/text()').get()
        info = response.xpath('//div[@class="job-primary detail-box"]//div[@class="info-primary"]/p/text()').getall()
        city,work_experience,education =  list(map(lambda x:x.split("：")[1],info))
        tags = ",".join(response.xpath('//div[@class="job-tags"]/span/text()').getall())
        describe = response.xpath('//div[@class="job-sec"]/div[@class="text"]//text()').getall()
        describe = ",".join(describe).replace("\n","").strip()
        company_describe = response.xpath('//div[@class="job-sec company-info"]/div[@class="text"]/text()').getall()
        company_describe = ",".join(company_describe).replace("\n", "").strip()
        info_content = ",".join(response.xpath('//div[@class="job-sec"]//div[@class="level-list"]//text()').getall())
        information = re.sub(r"[\n\s,，]","",info_content)
        work_location = response.xpath('//div[@class="location-address"]/text()').get()
        company_name = response.xpath('//h3[@class="name"]/a/text()').get()
        company_url = response.xpath('//div[@class="info-company"]/p[last()]/text()').get()
        item = BossItem(position_name=position_name,salary=salary,city=city,work_experience=work_experience, \
                        education=education,tags=tags, describes=describe,company_describe=company_describe, \
                        information=information,work_location=work_location,company_name=company_name,\
                        company_url=company_url, url=response.url, url_object_id = get_md5(response.url))
        yield item
