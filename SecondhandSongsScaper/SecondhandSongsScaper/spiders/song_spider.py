from email.base64mime import header_encode
import scrapy
from scrapy import Selector
from w3lib.html import remove_tags
from SecondhandSongsScaper.items import SongItem, CoverItem, SingerItem
from SecondhandSongsScaper.settings import SONGS_INPUT_PATH
import json, csv


class SongSpider(scrapy.Spider):
    name = "secondhandsongSpider"

    def start_requests(self):
        # url = 'https://secondhandsongs.com/work/136771/versions'
        # title = 'Let it Go'
        # line_n = 1
        # yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(ori_idx=line_n, song_title=title))

        # with open('input/t.txt', 'r') as f:
        #     lines = f.readlines()
        #     line_n = 8900
        #     for line in lines:
        #         url = line.strip()
        #         try:
        #             yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(ori_idx=line_n))            
        #         except: 
        #             pass
        #         line_n += 1

        with open(SONGS_INPUT_PATH, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            line_n = 0
            for line in reader:
                try:
                    if line_n==0:
                        line_n += 1
                        continue            
                    idx, title, url = line[:3]
                    url = f'{url}/versions'
                    self.log(f'checking {idx} {title} {url}')
                    yield scrapy.Request(url, callback=self.parse, cb_kwargs=dict(ori_idx=idx, song_title=title))
                    
                except: continue

    def parse(self, response, ori_idx, song_title):            
        # Covers table: cover song url => Back to Step 3 without get covers
        cover_table_elem = response.css('table')[0]
        for elem in cover_table_elem.css('tr'):
            cover_selectors = {'.field-title': 'song_name', '.field-player': 'song_interlink', 
                                '.field-performer': 'singer_name', '.field-performer': 'singer_interlink',
                                '.field-date': 'release_date', '.field-info': 'info'}
            cover_item = CoverItem()
            cover_item['original_song_id'] = ori_idx
            for selector, col in cover_selectors.items():
                try:
                    if col in[ 'release_date', 'song_name', 'singer_name']:
                        cover_item[col] = elem.css(f'{selector} ::text').get()
                    else:
                        cover_item[col] = 'https://secondhandsongs.com' + elem.css(f'{selector} a ::attr(href)').get()
                except:
                    cover_item[col] = ''      
            yield cover_item  
            yield scrapy.Request(url=cover_item['singer_interlink'], callback=self.Singerparse, cb_kwargs=dict(ori_idx=ori_idx))
    
        # item = SongItem()

        # item['original_song_id'] = ori_idx
        # item['name'] = song_title
        # # item['name'] = response.css('#content-title .link-performance::text').get().strip()
        # item['language'] = response.css('[itemprop="inLanguage"]::text').get()
        
        # try:        
        #     item['released_on'] = response.css('[itemprop="inAlbum"] .media-body p::text')[2].get().strip()
        # except:
        #     item['released_on'] = ''
            
        # # Optionals: Album thumbnail'
        # try: 
        #     item['album_thumbnail'] =  'https://secondhandsongs.com/'+response.css('[itemprop="inAlbum"] img::attr(src)').get()
        # except:
        #     item['album_thumbnail'] =  ''

        # # Optionals: Album name
        # try:
        #     item['album_name'] = response.css('[itemprop="inAlbum"] .link-release span::text').get()
        # except:
        #     item['album_name'] = ''

        # # Optionals: Album Link
        # try:
        #     item['album_interlink'] = 'https://secondhandsongs.com/' + response.css('[itemprop="inAlbum"] .link-release::attr(href)').get()
        # except:
        #     item['album_interlink'] = '' 
        # yield item

        self.log(f'Finished')
    
    
    def Singerparse(self, response, ori_idx):
        singer_item = SingerItem()
        singer_item['original_song_id'] = ori_idx
        singer_item['singer_name'] = response.css('h1::text').get()

        singer_selectors = {'Real name': 'singer_real_name', 'Born': 'born_date', 'Country': 'born_place'}
        dt_elems, dd_elems = response.css('dt'), response.css('dd')
        for i, dt_elem in enumerate(dt_elems): 
            header = dt_elem.css('::text').get()
            for col, item_col in singer_selectors.items():
                if header == col:
                    singer_item[item_col] = dd_elems[i].css('::text').get()

        yield singer_item

