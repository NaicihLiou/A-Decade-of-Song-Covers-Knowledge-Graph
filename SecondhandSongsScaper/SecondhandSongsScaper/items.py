# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SongItem(scrapy.Item):
    original_song_id = scrapy.Field()
    name = scrapy.Field()
    language = scrapy.Field()
    released_on = scrapy.Field()
    # album_thumbnail = scrapy.Field()
    # album_name = scrapy.Field()
    # album_interlink = scrapy.Field()	


class CoverItem(scrapy.Item):   
    original_song_id = scrapy.Field()
    song_name = scrapy.Field()
    song_interlink = scrapy.Field()	
    singer_name = scrapy.Field()
    singer_interlink = scrapy.Field()	
    release_date  = scrapy.Field()	
    info = scrapy.Field()

class SingerItem(scrapy.Item):  
    original_song_id = scrapy.Field()
    singer_name = scrapy.Field()
    singer_real_name = scrapy.Field()
    born_place = scrapy.Field()
    born_date = scrapy.Field()
    country = scrapy.Field()

class Singer_Name_Url_Item(scrapy.Item):  
    singer_name = scrapy.Field()
    singer_url = scrapy.Field()

class Song_LastFM_Item(scrapy.Item):       
    original_song_id = scrapy.Field()
    url_lastFM = scrapy.Field()
    singerName_lastFM = scrapy.Field()
    externalLink_homepage = scrapy.Field()
    externalLink_twitter = scrapy.Field()
    externalLink_facebook = scrapy.Field()
    externalLink_instagram = scrapy.Field()
    similar_singers = scrapy.Field()
    tag = scrapy.Field()