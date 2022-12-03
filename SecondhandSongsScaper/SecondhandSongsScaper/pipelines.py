# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from SecondhandSongsScaper.settings import SONG_PATH, COVER_PATH, SINGER_PATH, SINGER_LASTFM_OUTPUT_PATH, SINGER_URL_NAME_OUTPUT_PATH
import json

class SecondhandsongsscaperPipeline:
    def open_spider(self, spider):
        self.song_file = open(SONG_PATH, 'a+')
        self.cover_file = open(COVER_PATH, 'a+')
        self.singer_file = open(SINGER_PATH, 'a+')
        self.singer_name_url_file = open(SINGER_URL_NAME_OUTPUT_PATH, 'a+')
        self.singer_lastFM_file = open(SINGER_LASTFM_OUTPUT_PATH, 'a+')
       

    def close_spider(self, spider):
        self.song_file.close()
        self.cover_file.close()
        self.singer_file.close()
        self.singer_lastFM_file.close()
        self.singer_name_url_file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(adapter.asdict()) + "\n"

        if adapter.get('language'):
            self.song_file.write(line)
        elif adapter.get('born_date'):
            self.singer_file.write(line)
        elif adapter.get('singerName_lastFM'):
            self.singer_lastFM_file.write(line)
        elif adapter.get('singer_url'):
            self.singer_name_url_file.write(line)
        else:
            self.cover_file.write(line)

        return item
