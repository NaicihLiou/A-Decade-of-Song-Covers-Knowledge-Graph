from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get('https://secondhandsongs.com/statistics/stats_work_covered?pageSize=100')

driver.find_element(By.NAME, 'root.filter.year').send_keys('2012-2022')
driver.find_element(By.NAME, 'search_text').click()
time.sleep(15)

def list_to_str(l):
    return ', '.join(l).rstrip(',')

result = dict()
index_list = []
title_list = []
title_url_list = []
written_by_list = []
written_by_url_list = []
originally_by_list = []
originally_by_url_list = []
covers_list = []
adaptations_list = []

for i in range(101):
    for i in range(1,101):
        i = str(i)
        xpath = driver.find_elements(By.XPATH, '//*[@id="root.vw"]/table/tbody/tr['+i+']')
        index = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'field-index ')]
        title = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'link-work')]
        title_url = [value.get_attribute("href") for value in xpath[0].find_elements(By.CLASS_NAME, 'link-work')]
        written_by = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'link-artist')]
        written_by_url = [value.get_attribute("href") for value in xpath[0].find_elements(By.CLASS_NAME, 'link-artist')]
        # print(written_by_url)
        originally_by = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'link-performer')]
        # print(originally_by)
        originally_by_url = [value.get_attribute("href") for value in xpath[0].find_elements(By.CLASS_NAME, 'link-performer')]
        # print(originally_by_url)
        covers = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'field-covers.text-right')]
        adaptations = [value.text for value in xpath[0].find_elements(By.CLASS_NAME, 'field-fullAdaptations.text-right')]

        index_list.append(list_to_str(index))
        title_list.append(list_to_str(title))
        title_url_list.append(list_to_str(title_url))
        written_by_list.append(list_to_str(written_by))
        written_by_url_list.append(list_to_str(written_by_url))
        originally_by_list.append(list_to_str(originally_by))
        originally_by_url_list.append(list_to_str(originally_by_url))
        covers_list.append(list_to_str(covers))
        adaptations_list.append(list_to_str(adaptations))

    driver.find_element(By.CLASS_NAME, 'refresh-click.btn.btn-secondary').click()
    time.sleep(5)

song_list = pd.DataFrame({'index': index_list,
                          'title': title_list,
                          'title_url': title_url_list,
                          'written_by': written_by_list,
                          'written_by_url': written_by_url_list,
                          'originally_by': originally_by_list,
                          'originally_by_url': originally_by_url_list,
                          'covers': covers_list,
                          'adaptations': adaptations_list})
song_list.to_csv('original_song_stats.csv', index=False)
