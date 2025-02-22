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

    def paragraphs_extractor(self, selected_sections=None):
        paragraphs = {}
        default_section = "Introducción"
        paragraphs[default_section] = []
        
        # Buscar el contenedor específico
        content_div = self.soup.find('div', id="bodyContent")
        if not content_div:
            content_div = self.soup
        
        current_section = None
        found_first_h2 = False
        
        # Recorrer los elementos en orden dentro del contenedor
        for e in content_div.find_all(['h2', 'p', 'dl', 'ul'], recursive=True):
            if e.name == 'h2':
                found_first_h2 = True
                current_section = e.get_text().strip()
                if current_section not in paragraphs:
                    paragraphs[current_section] = []
            else:
                if not found_first_h2:
                    # Antes del primer <h2>, solo extraer <p>
                    if e.name == 'p':
                        paragraphs[default_section].append(e.get_text())
                else:
                    # Después del primer <h2>, extraer de forma habitual
                    if e.name == 'p':
                        if current_section is not None:
                            paragraphs[current_section].append(e.get_text())
                    elif e.name == 'dl':
                        dd = e.find('dd')
                        if dd:
                            i_tag = dd.find('i')
                            if i_tag and current_section is not None:
                                paragraphs[current_section].append(i_tag.get_text())
                    elif e.name == 'ul':
                        if current_section is not None:
                            for li in e.find_all('li'):
                                li_text = li.get_text().strip()
                                list_item = "- " + li_text
                                paragraphs[current_section].append(list_item)
        
        # Si se especificaron secciones, filtrar el resultado
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
