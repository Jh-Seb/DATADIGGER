from gui.app_gui import APPGUI
from scraper.static_scraper import WIKISCRAPER  # Asegúrate de que el archivo se llama static_scraper.py

def ejecutar_wiki_scraper(URL):
    pass

def main():
    app = APPGUI()
    app.url_scraper_callback = ejecutar_wiki_scraper
    app.mainloop()

if __name__ == "__main__":
    main()
