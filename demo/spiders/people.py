import scrapy
import datetime
from urllib.parse import urljoin
from demo.items import PeopleItem


class PeopleSpider(scrapy.Spider):
    name = 'people'
    start_urls = ['https://www.morganlewis.com/api/custom/peoplesearch/search?keyword=&category=bb82d24a9d7a45bd938533994c4e775a&sortBy=lastname&pageNum=1&numberPerPage=5&numberPerSection=5&enforceLanguage=&languageToEnforce=&school=&position=&location=&court=&judge=&isFacetRefresh=true']

    def parse(self, response):
        for person_link in response.xpath("//div[@class='c-content_team__card-info']/a/@href").extract():
            url = urljoin(response.url, person_link)
            yield response.follow(url, callback=self.parse_profile)

    def parse_profile(self, response):
        item = PeopleItem()
        item['url_to_profile'] = response.url
        item['photo_url'] = response.url + response.xpath("//img[@itemprop='image']/@src").extract_first()
        item['full_name'] = response.xpath("//span[@itemprop='name']/text()").extract_first()
        item['position'] = response.xpath("//section[@class='person-heading']/h2/text()").extract_first()
        phone_number = response.xpath("//p[@itemprop='telephone']/a/text()").extract()
        if len(phone_number) > 1:
            item['phone_numbers'] = phone_number
        else:
            item['phone_numbers'] = phone_number[0]
        item['email'] = response.xpath("//a[@itemprop='email']/text()").extract_first()
        item['services'] = response.xpath("(//section[@class='person-depart-info'])[1]/ul//a/span/following-sibling::text()[1]").extract()
        sectors = response.xpath("//div[@class='person-depart-info']/ul/li/a/@title").extract()
        if sectors:
            if len(sectors) > 1:
                item['sectors'] = sectors
            else:
                item['sectors'] = sectors[0]
        item['person_brief'] = response.xpath("//div[@class='people-intro']/div/p/text()").extract_first()
        item['datetime'] = datetime.datetime.now()
        yield item
