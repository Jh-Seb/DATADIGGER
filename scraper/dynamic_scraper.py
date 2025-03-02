import scrapy
from scrapy.crawler import CrawlerProcess #Iniciar el proceso

# Pagina 1: Properati ---------------------------------------------------------------------------------------------
class ProperatiScrapper(scrapy.Spider):
    name = 'properati_realstate'
    allowed_domains = ['www.properati.com.co']
    custom_settings = { 
        'FEEDS': {'data_properati.csv': {'format': 'csv', 'overwrite': True}} 
    } 

    def start_requests(self):
        # Parametros
        operationTypes = ["arriendo", "venta"]
        propertyTypes = {"apartaestudios": "studio", 
                        "apartamentos":"apartment", 
                        "casas":"house", 
                        "fincas":"villa", 
                        "campos":"land", 
                        "locales comerciales":"commercial",
                        "oficinas / Consultorios":"office",
                        "parqueaderos":"car_park"
                        }
        geoId = {
            "bogota": 3688685}
        
        # Crear la url
        tipos = ["apartamentos","casas","fincas"]
        propertyType = propertyTypes.get(tipos[0])
        for i in tipos:
            propertyType += "%2C"+ propertyTypes.get(i)

        geo = str(geoId.get("bogota"))

        url = "https://www.properati.com.co/s/"+operationTypes[0]+"?geos="+geo+"&propertyType="+propertyType
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
        
        next_page = response.css('a.pagination__link::attr(href)')[-1].get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# Pagina 2: FincaRaiz  ------------------------------------------------------------------------------------------------     
class FincaRaizScrapper(scrapy.Spider):
    name = 'fincaraiz_realstate'
    allowed_domains = ['www.fincaraiz.com.co']
    start_urls = ["https://www.fincaraiz.com.co/venta/casas-y-apartamentos/bogota"]
    custom_settings = { 
        'FEEDS': {'data_fincaraiz.csv': {'format': 'csv', 'overwrite': True}} 
    } 
    def start_requests(self):
        # Parametros
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
        geoId = {
            "bogota": "bogota"}
        
        # Crear la url
        tipos = ["apartamentos","casas","fincas"]
        propertyType = propertyTypes.get(tipos[0])
        for i in tipos:
            propertyType += "-"+ propertyTypes.get(i)

        geo = str(geoId.get("bogota"))

        url = "https://www.fincaraiz.com.co/"+operationTypes[0]+"/"+propertyType+"/"+geo
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
                # Si se fuera a separar cada atributo, seria muy largo y dificil
                'Habitaciones/Baños/Area': publicacion.css('span.body.body-2.body-regular.medium>strong::text').getall(),
                'agencia': publicacion.css('strong.body.body-2.high::text').get(),
                # Intente sacar las etiquetas pero es como si no existieran, no se pueden seleccionar
            }

        next_page = response.css('a.ant-pagination-item-link.CO::attr(href)')[-1].get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# Pagina 3: MetroCuadrado

#Main 
process = CrawlerProcess()
process.crawl(ProperatiScrapper)
process.crawl(FincaRaizScrapper)
process.start() 
