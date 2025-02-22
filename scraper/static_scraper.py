import requests
from bs4 import BeautifulSoup

class WIKISCRAPER:
    def __init__(self, url=None):
        # Si no se proporciona URL se usa una por defecto
        self.URL = url if url else "https://es.wikipedia.org/wiki/Bogotazo"
        self.page = requests.get(self.URL)
        if self.page.status_code == 200:
            self.soup = BeautifulSoup(self.page.text, 'html.parser')
        else:
            raise ValueError("Error al cargar la página. Verifica que la URL sea válida.")
    
    def title_extractor(self):
        title = self.soup.find('span', class_='mw-page-title-main')
        return title.get_text() if title else None

    def general_content_extractor(self):
        general_content = self.soup.find_all('h2')
        sections = [section.get_text() for section in general_content]
        return sections

    def paragraphs_extractor(self, selected_sections):
    #"""
    #Retorna un diccionario donde cada llave es una sección y el valor es una lista 
    #de párrafos y elementos de lista asociados a dicha sección.
    #"""
        paragraphs = {}
        current_section = None
        # Se incluye 'ul' para capturar listas
        for e in self.soup.find_all(['h2', 'p', 'dl', 'ul']):
            if e.name == 'h2':
                current_section = e.get_text().strip()
            if current_section in selected_sections:
                if e.name == 'p':
                    if current_section not in paragraphs:
                        paragraphs[current_section] = []
                    paragraphs[current_section].append(e.get_text())
                elif e.name == 'dl':
                    dd = e.find('dd')
                    if dd:
                        i_tag = dd.find('i')
                        if i_tag:
                            if current_section not in paragraphs:
                                paragraphs[current_section] = []
                            paragraphs[current_section].append(i_tag.get_text())
                elif e.name == 'ul':
                    # Iterar sobre cada <li> en el contenedor <ul>
                    for li in e.find_all('li'):
                        # Extraer el texto del <li> (incluye el contenido de <a> si lo hubiera)
                        li_text = li.get_text().strip()
                        # Preceder con guion para indicar que es un elemento de lista
                        list_item = "- " + li_text
                        if current_section not in paragraphs:
                            paragraphs[current_section] = []
                        paragraphs[current_section].append(list_item)
        return paragraphs



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
