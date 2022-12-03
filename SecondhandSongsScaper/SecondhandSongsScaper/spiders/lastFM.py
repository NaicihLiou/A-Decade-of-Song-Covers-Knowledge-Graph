from email.base64mime import header_encode
import scrapy
from scrapy import Selector
from w3lib.html import remove_tags
from SecondhandSongsScaper.items import Song_LastFM_Item
from SecondhandSongsScaper.settings import SONGS_LASTFM_INPUT_PATH
import json, csv


class LastFMSpider(scrapy.Spider):
    name = "lastFM"

    def start_requests(self):
        with open(SONGS_LASTFM_INPUT_PATH, 'r') as f:
            lines = f.readlines()
            singer_names = set()
            for line in lines:
                singer_dict = json.loads(line)
                original_song_id = singer_dict['original_song_id']
                singer_name = singer_dict['singer_name']
                if singer_name not in singer_names:
                    singer_names.add(singer_name)
                    url = 'https://www.last.fm/music/{}'.format('+'.join(singer_name.split(' ')))
                    yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(url=url, original_song_id=original_song_id))
                    
        # url = 'https://www.last.fm/music/Sam+Bailey'
        # yield scrapy.Request(url, cb_kwargs=dict(url=url, original_song_id=1))

    def parse(self, response, url, original_song_id):
        item = Song_LastFM_Item()
        item['original_song_id'] = original_song_id
        item['url_lastFM'] = url

        # Check whether enter the page correctly
        try:
            item['singerName_lastFM'] = response.css('.header-new-title::text').get().strip()
        except: 
            return

        try:
            item['externalLink_homepage'] = response.css('.resource-external-link--homepage::attr(href)').get()
        except:
            pass
    
        try:
            item['externalLink_twitter'] = response.css('.resource-external-link--twitter::attr(href)').get()
        except:
            pass
        
        try:
            item['externalLink_facebook'] = response.css('.resource-external-link--facebook::attr(href)').get()
        except:
            pass
        
        try:
            item['externalLink_instagram'] = response.css('.resource-external-link--instagram::attr(href)').get()
        except:
            pass
        
        # similar_singers
        item['similar_singers'] = []        
        for elem in response.css('.artist-similar-artists-sidebar-item'):
            try:
                similar_singer = {}
                similar_singer['name'] = elem.css('.link-block-target::text').get().strip()
                similar_singer['page_url'] = 'https://www.last.fm/' + elem.css('a::attr(href)').get()
                similar_singer['img_url'] = elem.css('img::attr(src)').get()

                item['similar_singers'].append(similar_singer)
            except:
                pass

        item['tag'] = []
        try:        
            for elem in response.css('.catalogue-tags .tag'):
                tag_name = elem.css('a::text').get().strip()
                item['tag'].append(tag_name)
        except:
            pass
            
        yield item

        self.log(f'Finished')