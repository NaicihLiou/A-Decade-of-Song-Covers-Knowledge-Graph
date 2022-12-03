from email.base64mime import header_encode
import scrapy
from scrapy import Selector
from w3lib.html import remove_tags
from SecondhandSongsScaper.items import Singer_Name_Url_Item
from SecondhandSongsScaper.settings import SINGER_URL_NAME_INPUT_PATH
import json


class SingerSpider(scrapy.Spider):
    name = "secondhandsongSpider_singer"

    def start_requests(self):
        with open(SINGER_URL_NAME_INPUT_PATH, 'r') as f:
            lines = f.readlines()

            singer_urls = set()
            for line in lines:
                # self.log(f'line {line}')
                data = json.loads(line)
                singer_url = data.get('singer_interlink')
                if singer_url:
                    singer_urls.add(singer_url)
        
            for singer_url in singer_urls:
                yield scrapy.Request(singer_url, callback=self.parse, cb_kwargs=dict(url=singer_url))
                    

    def parse(self, response, url):         
        singer_name_url_item = Singer_Name_Url_Item()
        
        singer_name_url_item['singer_name'] = response.css('h1::text').get().strip()
        singer_name_url_item['singer_url'] = url

        yield singer_name_url_item

