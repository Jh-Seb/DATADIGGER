import scrapy
from scrapy.crawler import CrawlerProcess 
#from scrapy_playwright.page import PageCoroutine

class MetrocuadradoSpider(scrapy.Spider):
    name = 'metrocuadrado_realstate'
    allowed_domains = ['www.metrocuadrado.com']
    custom_settings = { 
        'FEEDS': {'data_metrocuadrado.csv': {'format': 'csv', 'overwrite': True}} 
    } 
    
    def __init__(self, operation:str, property:list, location:str):
        self.operation = operation
        self.property = property
        self.location = location
    
    def create_url(self):
        # Creating the url
        propertyType = self.property[0]
        for i in range(1, len(self.property)):
            propertyType += "-"+ self.property[i]

        url = "https://www.metrocuadrado.com/"
        return url
    
    def start_requests(self): 
        #url = self.create_url()
        url="https://www.metrocuadrado.com/casa/venta/usado/bogota/?search=form"
        yield scrapy.Request(url=url, callback=self.parse, meta={'playwright': True})

    def parse(self, response):
        yield{
            'html_raw': response.body.decode('utf-8'),

        }
        
        publicaciones = response.css('ul.Ul-sctud2-0.jyGHXP.realestate-results-list.browse-results-list > li')
        for publicacion in publicaciones:
            yield{
                'title': publicacion.css('div').get(),
                #'price': publicacion.css('p.sc-fMiknA ZUMHA card-subitem text-black::text').get(),
                #'area': publicacion.css('span.properties__area::text').get(),
                #'habitaciones': publicacion.css('span.properties__bedrooms::text').get(),
                #'parking': publicacion.css('span.properties__amenity__car_park::text').get(),
                #'baños': publicacion.css('span.properties__bathrooms::text').get(),
                #'agencia': publicacion.css('span.agency__name::text').get(),
                
            }
        
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
#process.crawl(MetrocuadradoSpider, operation, property, location)
#process.start()
