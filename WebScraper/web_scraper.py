# SCRAPING WITH BEAUTIFUL SOUP
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

class WebScraper:
  def __init__(self, url):
    self.url = url
    
  def page_scrap(self):
    scraping_data = []
    page = req.get(self.url).text
    parsed_page = bs(page, 'html.parser')
    labels = [label for label in parsed_page.find_all('tr')[0].get_text().splitlines()[1:]]
    temp = [scraping_data.append((t, [])) for t in labels]
    return self.__td_scrap(parsed_page, scraping_data)
  
  def __td_scrap(self, parsed_page, scraping_data):
    td_data = parsed_page.find_all('tr')
    for j in range(1, len(parsed_page.find_all('tr')[1:])):
      i = 0
      td = td_data[j].get_text().splitlines()[1:]
      if len(td) != len(td_data[0].get_text().splitlines()[1:]):
        break
      for row_data in td:
        scraping_data[i][1].append(row_data)
        i+=1
    return self.__data_csv(scraping_data)
              
  def __data_csv(self, scraping_data):
    data = {title:column for (title, column) in scraping_data}
    return pd.DataFrame(data)    

if __name__ == '__main__':
    url = 'https://www.mohfw.gov.in/'
    df = WebScraper(url)
    data = df.page_scrap()
    print(data)

