import requests
from bs4 import BeautifulSoup
import shared_state

# Clase principal para realizar el scraping de una página de Wikipedia
class WIKISCRAPER:
    def __init__(self, url=None):
        """
        Constructor de la clase.
        Inicializa la URL a usar y carga la página.
        Si la URL no se proporciona, se usa una URL por defecto (Bogotazo en Wikipedia).
        """
        self.URL = url if url else "https://es.wikipedia.org/wiki/Bogotazo"
        self.page = requests.get(self.URL)
        # Verifica si la solicitud fue exitosa (código 200)
        if self.page.status_code == 200:
            self.soup = BeautifulSoup(self.page.text, 'html.parser')
        else:
            raise ValueError("Error al cargar la página. Verifica que la URL sea válida.")
    
    def title_extractor(self):
        """
        Extrae y retorna el título de la página.
        Busca el elemento <span> con clase 'mw-page-title-main' y obtiene su texto.
        """
        title = self.soup.find('span', class_='mw-page-title-main')
        return title.get_text() if title else None

    def general_content_extractor(self):
        """
        Extrae y retorna las secciones generales de la página.
        Busca todos los elementos <h2> y retorna una lista con los nombres de las secciones,
        agregando "Introducción" al inicio.
        """
        general_content = self.soup.find_all('h2')
        sections_r = [section.get_text() for section in general_content]
        sections = ["Introducción"] + sections_r
        return sections

    def paragraphs_extractor(self, selected_sections=None):
        """
        Extrae y organiza los párrafos de la página en secciones.
        - Antes del primer <h2>, los párrafos se asignan a la sección "Introducción".
        - Después del primer <h2>, los párrafos se asignan a la sección actual.
        También procesa elementos <dl> y <ul> para extraer texto adicional.
        Si se especifica la lista selected_sections, filtra los resultados para incluir solo esas secciones.
        """
        paragraphs = {}
        default_section = "Introducción"
        paragraphs[default_section] = []
        
        # Intenta obtener la parte principal del contenido
        content_div = self.soup.find('div', id="bodyContent")
        if not content_div:
            content_div = self.soup
        
        current_section = None
        found_first_h2 = False
        
        # Recorrer los elementos de interés: <h2>, <p>, <dl> y <ul>
        for e in content_div.find_all(['h2', 'p', 'dl', 'ul'], recursive=True):
            if e.name == 'h2':
                found_first_h2 = True
                current_section = e.get_text().strip()
                if current_section not in paragraphs:
                    paragraphs[current_section] = []
            else:
                if not found_first_h2:
                    # Antes del primer <h2>, se extraen los párrafos y se asignan a "Introducción"
                    if e.name == 'p':
                        paragraphs[default_section].append(e.get_text())
                else:
                    # Después del primer <h2>, se asignan los párrafos a la sección actual
                    if e.name == 'p':
                        if current_section is not None:
                            paragraphs[current_section].append(e.get_text())
                    elif e.name == 'dl':
                        # Extrae texto de etiquetas <dd> que contienen <i>
                        dd = e.find('dd')
                        if dd:
                            i_tag = dd.find('i')
                            if i_tag and current_section is not None:
                                paragraphs[current_section].append(i_tag.get_text())
                    elif e.name == 'ul':
                        # Extrae cada elemento de la lista y lo formatea
                        if current_section is not None:
                            for li in e.find_all('li'):
                                li_text = li.get_text().strip()
                                list_item = "- " + li_text
                                paragraphs[current_section].append(list_item)
    
        # Filtrar el resultado si se especifican secciones
        if selected_sections:
            filtered = {}
            if paragraphs.get(default_section):
                filtered[default_section] = paragraphs[default_section]
            for sec, content in paragraphs.items():
                if sec in selected_sections:
                    filtered[sec] = content
            return filtered
        else:
            return paragraphs
    
    def related_words_extractor(self):
        """
        Extrae enlaces (palabras relacionadas) presentes en los párrafos.
        Separa el contenido en dos grupos:
         - Párrafos antes del primer <h2>
         - Párrafos después del primer <h2>
        Luego, recorre cada párrafo para buscar enlaces (<a>) y extraer el texto y el href,
        ignorando aquellos enlaces que contienen un <span>.
        """
        RW = {}
        content_div = self.soup.find('div', id="bodyContent")
        if not content_div:
            content_div = self.soup

        paragraphs_before = []
        paragraphs_after = []
        found_first_h2 = False

        # Recorrer elementos <h2> y <p> en orden para separar antes y después del primer <h2>
        for element in content_div.find_all(['h2', 'p'], recursive=True):
            if element.name == 'h2':
                found_first_h2 = True
            elif element.name == 'p':
                if not found_first_h2:
                    paragraphs_before.append(element)
                else:
                    paragraphs_after.append(element)

        paragraphs_to_use = paragraphs_before + paragraphs_after

        # Extraer enlaces de los párrafos seleccionados
        for p in paragraphs_to_use:
            for a in p.find_all('a'):
                # Si el enlace contiene un <span>, se omite
                if a.find('span'):
                    continue
                word = a.get_text().strip()
                href = a.get('href')
                if word and href:
                    RW[word] = href

        return RW

# Bloque principal de ejecución: permite interactuar con el usuario
if __name__ == "__main__":

    url = input("Introduce una URL de Wikipedia: ").strip()
    wiki = WIKISCRAPER(url)
    

    title = wiki.title_extractor()
    print(f"Título: {title}")


    sections = wiki.general_content_extractor()
    print("Secciones disponibles:")
    for i, section in enumerate(sections):
        print(f"{i+1}. {section}")


    selected_indices = input("Selecciona las secciones por número (separadas por comas): ")
    selected_sections = [sections[int(i)-1] for i in selected_indices.split(",")]


    paragraphs = wiki.paragraphs_extractor(selected_sections)
    print("\nPárrafos seleccionados:\n")
    for section, paras in paragraphs.items():
        print(f"Sección: {section}")
        for para in paras:
            print(para)
            print("\n---\n")


    RW = wiki.related_words_extractor()
    print("\nPalabras Relacionadas:\n")
    for w, link in RW.items():
        print(f"Palabra: {w}")
        print(link)
