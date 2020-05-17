import scrapy


class PeopleItem(scrapy.Item):
    url_to_profile = scrapy.Field()
    photo_url = scrapy.Field()
    full_name = scrapy.Field()
    position = scrapy.Field()
    phone_numbers = scrapy.Field()
    email = scrapy.Field()
    services = scrapy.Field()
    sectors = scrapy.Field()
    publications = scrapy.Field()
    person_brief = scrapy.Field()
    datetime = scrapy.Field()
