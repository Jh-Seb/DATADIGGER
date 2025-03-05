# Libraries
import scrapy
from scrapy.crawler import CrawlerProcess

# Spider
class ProperatiScrapper(scrapy.Spider):
    name = 'properati_realstate'
    allowed_domains = ['www.properati.com.co']
    custom_settings = { 
        'FEEDS': {'data_properati.csv': {'format': 'csv', 'overwrite': True}} 
    } 

    def __init__(self, operation:str, property:list, location:str):
        self.operation = operation
        self.property = property
        self.location = location

    def create_url(self):
        # Creating the url
        propertyType = self.property[0]
        for i in range(1, len(self.property)):
            propertyType += "%2C"+ self.property[i]

        url = "https://www.properati.com.co/s/"+self.operation+"?geos="+self.location+"&propertyType="+propertyType
        return url

    def start_requests(self):  
        url = self.create_url()      
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        publicaciones = response.css('article.snippet')
        for publicacion in publicaciones:
            yield{
                'title': publicacion.css('a.title::text').get(),
                'price': publicacion.css('div.price::text').get(),
                'area': publicacion.css('span.properties__area::text').get(),
                'habitaciones': publicacion.css('span.properties__bedrooms::text').get(), 
                'baños': publicacion.css('span.properties__bathrooms::text').get(),
                'parking': publicacion.css('span.properties__amenity__car_park::text').get(),
                'terraza': publicacion.css('span.properties__amenity__terrace::text').get(),
                'piscina': publicacion.css('span.properties__amenity__swimming_pool::text').get(),
                'agencia': publicacion.css('span.agency__name::text').get(),
                'destacado': publicacion.css('span.label__highlight::text').get(),
            }
        
        # Scraping all the posible pages
        #next_page = response.css('a.pagination__link::attr(href)')[-1].get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)

# Main -------------------------------------------------------------------------------------
# Filters
operationTypes = ["arriendo", "venta"]
propertyTypes = {"apartaestudios":"studio", 
                "apartamentos":"apartment", 
                "casas":"house", 
                "fincas":"villa", 
                "campos":"land", 
                "locales comerciales":"commercial",
                "oficinas / Consultorios":"office",
                "parqueaderos":"car_park"
                }
geoId = {
    "bogota":3688685
    }
Types = list(propertyTypes.keys())
# Choose
# input(operation)
# input(property)
# input(location)
operation = "arriendo"
property = ["apartamentos","casas","fincas"]
location = "bogota"

# Parameters
# Type of operation
#operation = operationTypes[0]

# Type of the property
for i in range(1, len(property)):
    property[i] = propertyTypes.get(property[i])

# Location
location = str(geoId.get(location))

# Scrape
#process = CrawlerProcess()
#process.crawl(ProperatiScrapper, operation, property, location)
#process.start()
