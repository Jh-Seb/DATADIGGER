# Data Digger

## Descripción
**Data Digger** es una aplicación de escritorio diseñada para facilitar la extracción de datos de sitios web estáticos y dinámicos. Su principal objetivo es proporcionar herramientas eficientes para procesar información y entregarla en formatos organizados, como PDF o Excel. La aplicación es completamente portable, ya que está empaquetada como un archivo ejecutable (.exe) que no requiere instalación.

---

## Funcionalidades

### 1. Wiki Scraper
Este módulo permite a los usuarios:
- Extraer información relevante de páginas de Wikipedia.
- Generar un archivo PDF con el contenido seleccionado.
- Identificar palabras clave con enlaces a otros artículos relacionados y mostrarlas como recomendaciones.

**Flujo de trabajo:**
1. Introducir la URL de la página de Wikipedia.
2. Procesar el contenido para extraer texto relevante y enlaces.
3. Generar un archivo PDF con los resultados.

### 2. Real State Scraper
Este módulo se enfoca en páginas de bienes raíces y permite:
- Extraer publicaciones según los filtros proporcionados (ciudad, barrio, tipo de inmueble, etc.).
- Generar un archivo Excel con los datos estructurados.
- Buscar automáticamente la mejor opción según los criterios del usuario.

**Flujo de trabajo:**
1. Introducir la URL del sitio de bienes raíces.
2. Configurar los filtros deseados.
3. Generar un archivo Excel con los resultados y resaltar la mejor opción.

---

## Requisitos Técnicos

### Lenguaje de programación:
- **Python**

### Bibliotecas utilizadas:
- `customtkinter` para la interfaz gráfica.
- `Pillow` para la manipulación de imágenes.
- `requests` y `beautifulsoup4` para scraping web.
- `pandas` y `openpyxl` para manipulación de datos en Excel.
- `reportlab` para generación de PDFs.
- `PyInstaller` para empaquetar la aplicación como archivo ejecutable.

---

## Estructura de la Aplicación

```
DATADIGGER/
│
├── main.py       
├── shared_state.py  
├── config_manager.py      
├── scraper/
│   ├── __init__.py       
│   ├── static_scraper.py  
│   └── dynamic_scrapper/
│       ├── scrapy.cfg
│       └── dynamic_scrapper/
│           ├── __init__.py 
│           ├── items.py       
│           ├── middlewares.py 
│           ├── pipelines.py
│           ├── settings.py  
│           └── spiders/
│               ├── __init__.py 
│               ├── fincaraiz.py 
│               ├── metrocuadrado.py 
│               └── properati/
│
├── gui/
│   ├── __init__.py
│   ├── app_gui_start.py
│   ├── DKDE.py
│   ├── gui_blue_theme.py
│   ├── gui_green_theme.py
│   └── gui_red_theme.py       
│
├── reports/
│   ├── __init__.py
│   ├── dynamic_report.py
│   └── static_report.py  
│
└── assets/              
```

---

## Instalación y Uso

1. Descargar el archivo ejecutable (.exe) desde el repositorio.
2. Ejecutar el archivo en cualquier computador con Windows (no requiere instalación).
3. Seguir las instrucciones de la interfaz para seleccionar el módulo deseado y realizar el scraping.

---

## GUI

### Pantalla Principal
![Pantalla Principal](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/pantalla%20principal.png)

### Wiki Scraper
![Wiki Scraper](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/wiki%201.png)
![Wiki Scraper](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/wiki%202.png)
![Wiki Scraper](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/wiki%203.png)

### Real State Scraper
![Real State Scraper](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/real%201.png)
![Real State Scraper](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/real%202.png)

### Reports
![Reports](https://github.com/Jh-Seb/DATADIGGER/blob/main/assets/repo_screenshots/reports.png)

---
## DIAGRAMA DE CLASES
```mermaid
classDiagram
    %%================= Scraper and Report Classes =================
    class WIKISCRAPER {
      - URL : str
      - page : Response
      - soup : BeautifulSoup
      + __init__(url: str = None)
      + title_extractor() : str
      + general_content_extractor() : list
      + paragraphs_extractor(selected_sections: list) : dict
      + related_words_extractor() : dict
    }

    class ReportPDF {
      + header()
      + footer()
      + nickname(title: str)
      + indice(secciones, parrafos)
    }

    class Generator_report {
      + __init__()
      + generar()
    }
    ReportPDF <|-- Generator_report

    %%================= Shared State and Configuration =================
    class SharedState {
      - titulo : str
      - parrafos : dict
      - secciones : list
      - archive : str = "extracto_wikipedia.json"
      + cargar() : dict
      + guardar(estado: dict)
      + set_titulo(value: str)
      + get_titulo() : str
      + set_parrafos(value: dict)
      + get_parrafos() : dict
    }

    class ConfigManager {
      <<static>>
      + CONFIG_FILE : str = "config.json"
      + load_config() : dict
      + update_config(theme: str = None, reports_directory: str = None) : dict
    }

    %%================= GUI Base and Application =================
    class BaseScreen {
      - parent
      + __init__(parent)
      + clear_widget(widget_name: str)
    }

    class APPGUIRED {
      - pantalla_principal
      - pantalla_configuracion
      - pantalla_creadores
      - pantalla_informacion_static
      - static_scraper
      - dynamic_scraper
      - pantalla_properati
      - pantalla_metro_cuadrado
      - pantalla_finca_raiz
      - reports
      + __init__()
      + show_frame(frame)
    }

    %%================= GUI Screen Classes =================
    class Pantalla_Principal {
      - buttom_frame_1
      - buttom_frame_2
      - info_frame
      - config_frame
      - version_frame
      - title_label
      - version_label
      + __init__(parent)
    }
    class Pantalla_Configuracion {
      - house_button
      - title_label
      - config_frame
      - theme_picker
      - directory_entry
      - directory_button
      + __init__(parent)
      + change_theme()
      + change_directory()
    }
    class Pantalla_Creadores {
      - house_button
      - title_label
      - creators_frame
      - creators_label
      - gif_frame
      - gif_label
      + __init__(parent)
      + animate_gif()
    }
    class Pantalla_Informacion_Static {
      - return_button_static
      - info_label
      + __init__(parent)
    }
    class Pantalla_Informacion_Dynamic {
      - return_button_dynamic
      - info_label
      + __init__(parent)
    }
    class Static_Scraper {
      - url : str
      - scraper : WIKISCRAPER
      - title : str
      - sections : list
      - related_words : dict
      - paragraphs : dict
      - section_vars : dict
      + __init__(parent)
      + start_scraping()
      + search_url()
      + show_related_frame()
      + show_sections_frame()
      + show_wiki_frame()
      + global_atributes()
    }
    class Dynamic_Scraper {
      + __init__(parent)
    }
    class Pantalla_Properati {
      - city_list : list
      - return_button_dynamic
      - info_label
      - url_frame
      - url_entry
      - search_button
      - city_scroll_frame
      - list_frame
      - list_box_1
      - list_box_2
      + __init__(parent)
      + update_city_suggestions(event)
      + select_city(city)
      + export_filters()
    }
    class Pantalla_Metro_Cuadrado {
      - city_list : list
      - return_button_dynamic
      - info_label
      - url_frame
      - url_entry
      - search_button
      - city_scroll_frame
      - list_frame
      - list_box_1
      - list_box_2
      + __init__(parent)
      + update_city_suggestions(event)
      + select_city(city)
      + export_filters()
    }
    class Pantalla_Finca_Raiz {
      - city_list : list
      - return_button_dynamic
      - info_label
      - url_frame
      - url_entry
      - search_button
      - city_scroll_frame
      - list_frame
      - list_box_1
      - list_box_2
      + __init__(parent)
      + update_city_suggestions(event)
      + select_city(city)
      + export_filters()
    }
    class Reports {
      - house_button
      - title_label
      - files_frame
      + __init__(parent)
      + refresh_files()
      + tkraise(aboveThis)
    }

    %%================= Alternative GUI Startup =================
    class DKDE {
      + start_app()
    }

    %%================= Inheritance and Relationships =================
    %% Inheritance for GUI Screens
    BaseScreen <|-- Pantalla_Principal
    BaseScreen <|-- Pantalla_Configuracion
    BaseScreen <|-- Pantalla_Creadores
    BaseScreen <|-- Pantalla_Informacion_Static
    BaseScreen <|-- Pantalla_Informacion_Dynamic
    BaseScreen <|-- Static_Scraper
    BaseScreen <|-- Dynamic_Scraper
    BaseScreen <|-- Pantalla_Properati
    BaseScreen <|-- Pantalla_Metro_Cuadrado
    BaseScreen <|-- Pantalla_Finca_Raiz
    BaseScreen <|-- Reports

    %% APPGUIRED Composition (contains multiple screens)
    APPGUIRED --> Pantalla_Principal : contains
    APPGUIRED --> Pantalla_Configuracion : contains
    APPGUIRED --> Pantalla_Creadores : contains
    APPGUIRED --> Pantalla_Informacion_Static : contains
    APPGUIRED --> Static_Scraper : contains
    APPGUIRED --> Dynamic_Scraper : contains
    APPGUIRED --> Pantalla_Properati : contains
    APPGUIRED --> Pantalla_Metro_Cuadrado : contains
    APPGUIRED --> Pantalla_Finca_Raiz : contains
    APPGUIRED --> Reports : contains

    %% Module Dependencies
    Static_Scraper --> WIKISCRAPER : uses
    Static_Scraper --> SharedState : updates (set_titulo, set_parrafos)
    Generator_report --> SharedState : reads/writes state
    Generator_report --> ConfigManager : reads configuration
    APPGUIRED --> DKDE : alternative startup option

```
¿Por qué se extinguieron los mamuts? Porque no habian paputs
