import requests
from bs4 import BeautifulSoup
from gui.app_gui import Static_Scraper
URL = Static_Scraper.url_entry.get()
class WIKISCRAPER:
    def __init__(self):
        self.URL = URL
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
        paragraphs = []
        current_section = None
        for e in self.soup.find_all(['h2', 'p', 'dl']):
            if e.name == 'h2':
                current_section = e.get_text()
            if current_section in selected_sections:
                if e.name == 'p':
                    paragraphs.append(e.get_text())
                elif e.name == 'dl':
                    quote = e.find('dd').find('i')
                    if quote:
                        paragraphs.append(quote.get_text())
        return paragraphs

if __name__ == "__main__":
    wiki = WIKISCRAPER()
    title = wiki.title_extractor()
    print(f"Título: {title}")

    sections = wiki.general_content_extractor()
    print("Secciones disponibles:")
    for i, section in enumerate(sections):
        print(f"{i+1}. {section}")

    selected_indices = input("Selecciona las secciones por número (separadas por comas): ")
    selected_sections = [sections[int(i)-1] for i in selected_indices.split(",")]

    paragraphs = wiki.paragraphs_extractor(selected_sections)
    print("\nParrafos seleccionados:\n")
    for para in paragraphs:
        print(para)
        print("\n---\n")