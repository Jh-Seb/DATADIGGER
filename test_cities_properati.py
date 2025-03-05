# Libraries
import csv
import scrapy
from scrapy.crawler import CrawlerProcess

# Cities
class CitiesScrapper(scrapy.Spider):
    name = 'cities'
    allowed_domains = ['es.wikipedia.org']
    start_urls = ['https://es.wikipedia.org/wiki/Anexo:Municipios_de_Colombia_por_población']
    custom_settings = { 
        'FEEDS': {'cities.csv': {'format': 'csv', 'overwrite': True}} 
    } 

    def parse(self, response):
        ciudades = response.css('table.wikitable>tbody>tr')
        for ciudad in ciudades:
            yield{
                'lugar': ciudad.css('a::text').getall(),
            }

# Spider
class ProperatiScrapper(scrapy.Spider):
    name = 'properati_realstate'
    allowed_domains = ['www.properati.com.co']
    custom_settings = { 
        'FEEDS': {'data_properati.csv': {'format': 'csv', 'overwrite': True}} 
    } 

    def normalize(self, s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b)
        return s

    def start_requests(self): 
        with open('cities.csv', 'r', encoding="utf8") as cities:
            for line in csv.reader(cities):
                self.location = self.normalize(line[0].split("," )[0].lower()).replace(" ", "-")
                # Url
                url = "https://www.properati.com.co/s/"+self.location    
                try: 
                    yield scrapy.Request(url=url, callback=self.parse)
                except:
                    self.location = (self.normalize(line[0].split("," )[0].lower()).replace(" ", "-")+"-"+self.normalize(self.normalize(line[0].split("," )[-1].lower())).replace(" ", "-"))
                    # Url
                    url = "https://www.properati.com.co/s/"+self.location    
                    yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        yield{
            'Ciudad': f'{self.location}'
        }
# Main -------------------------------------------------------------------------------------
# Scrape
process = CrawlerProcess()
process.crawl(ProperatiScrapper)
#process.crawl(CitiesScrapper)
process.start()
