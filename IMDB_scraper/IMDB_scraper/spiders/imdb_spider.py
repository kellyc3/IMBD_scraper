# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0475293/']

    prefix = start_urls[0]

    def parse(self, response):
        nav_bar = response.css("div.SubNav__SubNavContentBlock-sc-11106ua-2.bAolrB")
        cast_box = nav_bar.css("li.ipc-inline-list__item")
        cast_link = cast_box.css("a:first-child").attrib["href"]
        link = self.prefix + cast_link
        yield Request(link, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        suffixes = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        actor_urls = [self.prefix + suffix for suffix in suffixes]
        for url in actor_urls:
            yield Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        film_rows = response.css("div.filmo-row")
        credits = []

        # add the name of the movie to the credits array
        for row in film_rows:
            id = row.css("::attr(id)").get()
            if "actor" in id:
                credits.append(row.css("a::text")[0].get())
        
        # find the name of the actor
        name = response.css("h1.header").css("span::text").get()

        # create and yield a dictionary d
        d = {name : credits}
        yield d

