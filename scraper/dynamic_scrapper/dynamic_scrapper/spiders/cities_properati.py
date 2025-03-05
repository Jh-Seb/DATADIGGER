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
class ProperatiCitiesScrapper(scrapy.Spider):
    name = 'properati_cities'
    allowed_domains = ['www.properati.com.co']
    custom_settings = { 
        'FEEDS': {'data_cities_properati.csv': {'format': 'csv', 'overwrite': True}} 
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
                location = self.normalize(line[0].split(",")[0].lower()).replace(" ", "-")
                department = self.normalize(line[0].split(",")[-1].lower()).replace(" ", "-")
                # Url
                url = "https://www.properati.com.co/s/"+location   
                url2 = url+'-'+department 
                yield scrapy.Request(url=url, callback=self.parse)
                yield scrapy.Request(url=url2, callback=self.parse)
    
    def parse(self, response):
        yield{
            'Ciudad': f'{response.url}'
        }
# Main -------------------------------------------------------------------------------------
# Scrape
process = CrawlerProcess()
process.crawl(CitiesScrapper)
process.crawl(ProperatiCitiesScrapper)
process.start()
