import scrapy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from lxml import html
import os
import jsonlines


class JavdbSpider(CrawlSpider):
    name = 'javdb'

    rules = (Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_page", follow= True),)

    def __init__(self, *args, **kwargs):
        star_init_url_dict_path = './data/star_init_url.json'
        previous_crawl_result_path = './data/result.json'
        if os.path.isfile(previous_crawl_result_path):
            self.prev_urls =[]
            with jsonlines.open(previous_crawl_result_path) as reader:
                for item in reader:
                    self.prev_urls.append(item['movie_url'])
        else:
            self.prev_urls = []
            pass
        with jsonlines.open(star_init_url_dict_path) as reader:
            self.url_list = [url for url in reader]


    def start_requests(self):
        for url in self.url_list:
            yield scrapy.Request(url=url,  callback=self.parse_page)
    

    def parse_page(self, response):
        for m in response.css('div.grid-item.column'):
            movie_url = 'https://javdb6.com' + m.css('a::attr(href)').get()
            movie_id = m.xpath(".//*[contains(@class, 'uid')]/text()").get()
            if movie_url in self.prev_urls:
                print('\n')
                print('{} has already been downloaded before, skip...'.format(movie_id))
                print('\n')
                pass
            else:
                yield scrapy.Request(movie_url, callback=self.parse_movie, meta={'item': {
                'movie_star':m.xpath('/html/body/section/div/div[3]/div[2]/h2/span[1]/text()').get(),
                'movie_url':  movie_url,
                'movie_id' : movie_id,
                'movie_title': m.css('a::attr(title)').get(),
                'movie_meta' : m.xpath(".//*[contains(@class, 'meta')]/text()").get().strip(),
                'movie_img_src' : m.xpath(".//img/@data-src").get()
                }})
        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page)

    def parse_movie(self, response):
        item = response.meta['item']
        item['mega_link'] = response.css('td[class = magnet-name] a::attr(href)').extract()[0]
        return item
