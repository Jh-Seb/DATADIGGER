# Libraries
import scrapy
import filters
from reports.generator_dynamic import generar
from scrapy.crawler import CrawlerProcess

# Spider
class FincaraizScrapper(scrapy.Spider):
    name = 'fincaraiz_realstate'
    allowed_domains = ['www.fincaraiz.com.co']
    custom_settings = { 
        'FEEDS': {'data_fincaraiz.csv': {'format': 'csv', 'overwrite': True}} 
    } 

    def __init__(self, operation:str, property:list, location:str):
        self.operation = operation
        self.property = property
        self.location = location

    def create_url(self):
        # Creating the url
        propertyType = self.property[0]
        for i in range(1, len(self.property)):
            propertyType += "-"+self.property[i]

        url = "https://www.fincaraiz.com.co/"+self.operation+"/"+propertyType+"/"+self.location
        return url

    def start_requests(self): 
        url = self.create_url()
        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        publicaciones = response.css('div.listingCard')
        for publicacion in publicaciones:
            title = publicacion.css('span.body.body-2.body-bold.high.d-block>strong::text').get()
            if not title:
                title = publicacion.css('span.lc-title.body.body-2.body-regular.medium::text').get()
            yield{
                'title': title,
                'price': publicacion.css('span.ant-typography.price.heading.heading-3.high>strong::text').get(),
                # It can be done w pipelines
                'Habitaciones/Baños/Area': publicacion.css('span.body.body-2.body-regular.medium>strong::text').getall(),
                'agencia': publicacion.css('strong.body.body-2.high::text').get(),
                # The tags were strange to extract, like if they didnt exist
            }

        #next_page = response.css('a.ant-pagination-item-link.CO::attr(href)')[-1].get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)

# Main -------------------------------------------------------------------------------------
# Filters
operationTypes = ["arriendo", "venta"]
propertyTypes = {"casas":"casas",
                "apartamentos":"apartamentos", 
                "apartaestudios": "apartaestudios", 
                "cabañas":"cabanas",
                "casas campestres":"casas-campestres",
                "casas lotes":"casas-lotes",
                "fincas":"fincas", 
                "habitaciones":"habitaciones",
                "lotes":"lotes",
                "bodegas":"bodegas",    
                "consultorios":"consultorios",         
                "locales":"locales",
                "oficinas":"oficinas",
                "parqueaderos":"parqueaderos",
                "edificios":"edificios"
                }


Types= list(propertyTypes.keys()) 


def finca_raiz_scraper():
    propertyTypes = {"casas":"casas",
                "apartamentos":"apartamentos", 
                "apartaestudios": "apartaestudios", 
                "cabañas":"cabanas",
                "casas campestres":"casas-campestres",
                "casas lotes":"casas-lotes",
                "fincas":"fincas", 
                "habitaciones":"habitaciones",
                "lotes":"lotes",
                "bodegas":"bodegas",    
                "consultorios":"consultorios",         
                "locales":"locales",
                "oficinas":"oficinas",
                "parqueaderos":"parqueaderos",
                "edificios":"edificios"
                }
    operation = filters.operation_type
    property = propertyTypes.get(filters.property_type)
    location = filters.city

    process = CrawlerProcess()
    process.crawl(FincaraizScrapper, operation, property, location)
    process.start()
    generar()
