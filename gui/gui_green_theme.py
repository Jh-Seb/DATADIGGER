import tkinter
import os
import customtkinter
import webbrowser
import shared_state
import filters
import tkinter.messagebox as mbox
from tkinter import filedialog
from config_manager import load_config, update_config
from PIL import Image, ImageTk, ImageSequence
from scraper.static_scraper import WIKISCRAPER
import scraper.dynamic_scrapper.dynamic_scrapper.spiders.fincaraiz as FincaRaiz
import scraper.dynamic_scrapper.dynamic_scrapper.spiders.properati as Properati
import scraper.dynamic_scrapper.dynamic_scrapper.spiders.metrocuadrado as MetroCuadrado

# Configuración de apariencia
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

# --------- PALETA DE COLORES VERDE ORIGINAL ---------
COLOR_BG               = "#111612"  # Fondo principal de la app
COLOR_BUTTON           = "#0f0f0f"  # Fondo de botones ("WIKI", "REAL STATE", "SOON...")
COLOR_BORDER           = "#383838"  # Contorno de botones
COLOR_HOVER            = "#27ba58"  # Color hover de botones
COLOR_TITLE            = "#32ff7e"  # Color de los títulos
COLOR_TEXT             = "#626262"  # Texto general (por ejemplo, versión)
COLOR_FRAME            = "#111612"  # Fondo para frames oscuros
COLOR_HIGHLIGHT_FRAME  = "#32ff7e"  # Fondo para frames “destacados” o scrollable
COLOR_ERROR_TEXT       = "red"      # Texto para mensajes de error

# Definir Imágenes (una sola vez)
logo = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\logo2.png'),
    dark_image=Image.open(r'assets\green_theme\logo2.png'),
    size=(50, 50)
)
bgimage = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\bgimage.png'),
    dark_image=Image.open(r'assets\green_theme\bgimage.png'),
    size=(1381.25, 1056)
)
questionicon = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\Questionicon.png'),
    dark_image=Image.open(r'assets\green_theme\Questionicon.png'),
    size=(60, 60)
)
configicon = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\configicon.png'),
    dark_image=Image.open(r'assets\green_theme\configicon.png'),
    size=(60, 60)
)
homeicon = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\homeicon.png'),
    dark_image=Image.open(r'assets\green_theme\homeicon.png'),
    size=(60, 60)
)
returnicon = customtkinter.CTkImage(
    light_image=Image.open(r'assets\green_theme\returnimage.png'),
    dark_image=Image.open(r'assets\green_theme\returnimage.png'),
    size = (60,60)
)
dogs = customtkinter.CTkImage(
    light_image=Image.open(r'assets/dogs.gif'),
    dark_image=Image.open(r'assets/dogs.gif')
)


# Clase base para pantallas comunes
class BaseScreen(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color=COLOR_BG)
        # Fondo común
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)
    
    def clear_widget(self, widget_name):
        widget = getattr(self, widget_name, None)
        if widget is not None:
            widget.place_forget()
            widget.destroy()
            setattr(self, widget_name, None)

# Ventana principal
class APPGUIGREEN(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DataDigger")
        self.configure(bg_color=COLOR_BG)
        
        # Inicialización de pantallas
        self.pantalla_principal = Pantalla_Principal(self)
        self.static_scraper = Static_Scraper(self)
        self.dynamic_scraper = Dynamic_Scraper(self)
        self.pantalla_creadores = Pantalla_Creadores(self)
        self.pantalla_configuracion = Pantalla_Configuracion(self)
        self.reports = Reports(self)
        self.pantalla_properati = Pantalla_Properati(self)
        self.pantalla_metro_cuadrado = Pantalla_Metro_Cuadrado(self)
        self.pantalla_finca_raiz = Pantalla_Finca_Raiz(self)
        
        self.show_frame(self.pantalla_principal)

    def show_frame(self, frame):
        """Muestra el frame seleccionado y oculta los demás."""
        frame.tkraise()

# Pantalla principal
class Pantalla_Principal(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        # Frames internos
        self.buttom_frame_1 = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=200, width=700)
        self.buttom_frame_1.place(relx=0.5, y=220, anchor="center")

        self.buttom_frame_2 = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=200, width=240)
        self.buttom_frame_2.place(relx=0.5, y=430, anchor="center")

        self.info_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=60, width=60)
        self.info_frame.place(x=50, rely=1, anchor="s")

        self.config_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=190, width=100)
        self.config_frame.place(relx=0.98, y=20, anchor="ne")

        self.version_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=30, width=240)
        self.version_frame.place(relx=0.9, rely=1, anchor="s")

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="DATA DIGGER",
            font=("Segoe UI Black", 80, "bold"),
            text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=60, anchor="center")
        
        # Versión
        self.version_label = customtkinter.CTkLabel(
            self.version_frame,
            text="DATA DIGGER version 1.0",
            font=("Arial", 17, "bold"),
            text_color=COLOR_TEXT
        )
        self.version_label.place(x=20, rely=0.5, anchor="w")

        # Botones de información y configuración
        self.logo_button = customtkinter.CTkButton(
            self.info_frame, text="", image=logo,
            width=50, height=50, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            command=lambda: parent.show_frame(parent.pantalla_creadores)
        )
        self.logo_button.place(x=35, rely=0.5, anchor="center")
        
        self.config_button = customtkinter.CTkButton(
            self.config_frame, text="", image=configicon,
            width=60, height=60, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            command=lambda: parent.show_frame(parent.pantalla_configuracion)
        )
        self.config_button.pack(pady=10, padx=10)

        self.question_button = customtkinter.CTkButton(
            self.config_frame, text="", image=questionicon,
            width=60, height=60, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            command=lambda: parent.show_frame(parent.pantalla_informacion)
        )
        self.question_button.pack(pady=10, padx=10)
        
        # Botones para acceder a los scrapers
        self.static_button = customtkinter.CTkButton(
            self.buttom_frame_1, text="WIKI",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER, border_width=5, border_color=COLOR_BORDER,
            command=lambda: parent.show_frame(parent.static_scraper)
        )
        self.static_button.place(relx=0.17, rely=0.5, anchor="center")

        self.dynamic_button = customtkinter.CTkButton(
            self.buttom_frame_1, text="REAL STATE",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER, border_width=5, border_color=COLOR_BORDER,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.dynamic_button.place(relx=0.5, rely=0.5, anchor="center")

        self.reports_button = customtkinter.CTkButton(
            self.buttom_frame_1, text="REPORTS",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            border_width=5, border_color=COLOR_BORDER,
            hover_color=COLOR_HOVER,
            command=lambda: parent.show_frame(parent.reports)
        )
        self.reports_button.place(relx=0.83, rely=0.5, anchor="center")

        self.coming_button = customtkinter.CTkButton(
            self.buttom_frame_2, text="SOON...",
            text_color=COLOR_TEXT,
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            border_width=5, border_color=COLOR_BORDER,
            hover_color="#227f7f"
        )
        self.coming_button.place(relx=0.5, rely=0.5, anchor="center")

class Pantalla_Configuracion(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color=COLOR_BG)

        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=COLOR_BG, hover_color=COLOR_HOVER,
            width=60, height=60, command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

        self.title_label = customtkinter.CTkLabel(
            self, text="CONFIGURACION", font=("Segoe UI Black", 40, "bold"), text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        self.config_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=400, width=400)
        self.config_frame.place(relx=0.5, y=260, anchor="center")
        
        
        themes = ["Green", "Blue", "Red"]
        self.theme_picker = customtkinter.CTkComboBox(self.config_frame, values=themes, height=40, width=100)
        self.theme_picker.place(x=90, y=60, anchor="center")
        
        
        config = load_config()
        current_theme = config.get("theme", "blue").capitalize()
        self.theme_picker.set(current_theme)
        
        self.theme_button = customtkinter.CTkButton(
            self.config_frame, text="Select", fg_color=COLOR_BUTTON, hover_color=COLOR_HOVER,
            width=80, height=40, command=self.change_theme
        )
        self.theme_button.place(x=190, y=60, anchor="center")

        
        default_directory = config.get("reports_directory", os.path.join(os.path.expanduser("~"), "Downloads", "reports"))
        self.directory_entry = customtkinter.CTkEntry(
            self.config_frame,
            placeholder_text=default_directory,
            width=320,
            height=40,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.directory_entry.place(x=200, y=140, anchor="center")

        self.directory_button = customtkinter.CTkButton(
            self.config_frame,
            text="Select Directory",
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            width=140,
            height=40,
            command=self.change_directory
        )
        self.directory_button.place(relx=0.5, y=200, anchor="center")
        
        
        self.directory = default_directory

    def change_directory(self):
        
        path_text = self.directory_entry.get().strip()
        if path_text:
            if os.path.isdir(path_text):
                self.directory = path_text
                update_config(reports_directory=self.directory)
                self.directory_entry.configure(placeholder_text=self.directory)
                mbox.showinfo("Actualizado", "Directorio actualizado correctamente.")
            else:
                mbox.showerror("Error", "INGRESE UNA RUTA VALIDA")
        else:
            default_dir = self.directory_entry.cget("placeholder_text")
            selected_dir = filedialog.askdirectory(initialdir=default_dir, 
                                                   title="Seleccione la carpeta de destino para los reports")
            if selected_dir:
                self.directory = selected_dir
                update_config(reports_directory=self.directory)
                self.directory_entry.configure(placeholder_text=self.directory)
                mbox.showinfo("Actualizado", "Directorio actualizado correctamente.")

    def change_theme(self):
        new_theme = self.theme_picker.get().lower()
        update_config(theme=new_theme)
        mbox.showinfo("Actualizado", "Tema actualizado, porfavor vuelva a abrir el programa para visualizar los cambios")
        

# Pantalla de creadores
class Pantalla_Creadores(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

        self.title_label = customtkinter.CTkLabel(
            self, text="CREATORS",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        self.creators_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG, height=300, width=400
        )
        self.creators_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.creators_label = customtkinter.CTkLabel(
            self.creators_frame,
            text=("Jhon Sebastian Rodriguez Ramirez\n"
                  "Sebastian Alejandro Alarcon Cespedes\n"
                  "Yadieth Stefany Guevara Manrique"),
            justify="center",
            font=("Arial", 20, "bold"),
            text_color=COLOR_TEXT,
            width=360, height=460
        )
        self.creators_label.place(relx=0.5, rely=0.5, anchor="center")

        self.gif_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG,width=272, height=168)
        self.gif_frame.place(x = 156, rely=0.9, anchor="center")

        
        self.gif_image = Image.open('assets/dogs.gif')
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((272,168),Image.LANCZOS)) for frame in ImageSequence.Iterator(self.gif_image)]
        self.frame_count = len(self.frames)

        
        self.gif_label = tkinter.Label(self.gif_frame, bg=COLOR_BG)
        self.gif_label.place(relx=0.5, rely=0.5, anchor="center", relheight=1, relwidth=1)

        self.animate_gif()

    def animate_gif(self):
        def update_gif(index):
            self.gif_label.config(image=self.frames[index])
            next_index = (index + 1) % self.frame_count  # Cicla de forma indefinida
            self.after(100, update_gif, next_index)  # Actualiza cada 100 ms
        update_gif(0)

# Scraper estático (WIKI)
class Static_Scraper(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

        self.config_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=190, width=100)
        self.config_frame.place(relx=0.98, y=20, anchor="ne")

        self.title_label = customtkinter.CTkLabel(
            self, text="WIKI",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        self.status_label = customtkinter.CTkLabel(
            self, text="",
            height=30, width=400,
            text_color=COLOR_TEXT
        )
        self.status_label.place(relx=0.5, y=95, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            command=self.start_scraping
        )
        self.search_button.place(x=950, y=25, anchor="center")

    def start_scraping(self):
        # Limpieza de widgets previos
        for widget in ["sections_frame", "wiki_frame", "related_frame", "sections_label", "related_label"]:
            self.clear_widget(widget)
        
        self.search_url()
        self.show_related_frame()
        self.show_sections_frame()

    def search_url(self):
        self.url = self.url_entry.get().strip()
        if not self.url:
            self.status_label.configure(text="Por favor, ingresa una URL válida.", text_color=COLOR_ERROR_TEXT)
            return
        try:
            self.scraper = WIKISCRAPER(self.url)
            self.title = self.scraper.title_extractor()
            self.sections = self.scraper.general_content_extractor()
            self.related_words = self.scraper.related_words_extractor()
            self.status_label.configure(text="URL cargada correctamente", text_color=COLOR_TITLE)
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color=COLOR_ERROR_TEXT)

    def show_related_frame(self):
        for widget in ["related_frame", "related_label"]:
            self.clear_widget(widget)

        self.related_label = customtkinter.CTkLabel(
            self, text="Palabras relacionadas",
            font=("Segoe UI Black", 20, "bold"),
            text_color=COLOR_TITLE
        )
        self.related_label.place(relx=0.3333, y=230, anchor="center")

        self.related_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_HIGHLIGHT_FRAME,
            width=300, height=400
        )
        self.related_frame.place(relx=0.3333, y=460, anchor="center")

        for key, value in self.related_words.items():
            def open_wiki(v=value):
                webbrowser.open("https://es.wikipedia.org/" + v)
            customtkinter.CTkButton(
                self.related_frame,
                text=key,
                text_color="white",
                width=200,
                height=20,
                fg_color=COLOR_BUTTON,
                hover_color=COLOR_HOVER,
                border_color=COLOR_BORDER,
                command=open_wiki
            ).pack(pady=10)

    def show_sections_frame(self):
        self.sections_label = customtkinter.CTkLabel(
            self, text="Secciones",
            font=("Segoe UI Black", 20, "bold"),
            text_color=COLOR_TITLE
        )
        self.sections_label.place(relx=0.6667, y=230, anchor="center")

        self.sections_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_HIGHLIGHT_FRAME,
            width=300, height=400
        )
        self.sections_frame.place(relx=0.6667, y=460, anchor="center")

        self.section_vars = {}
        for section in self.sections:
            var = customtkinter.StringVar(value="on")
            self.section_vars[section] = var
            customtkinter.CTkSwitch(
                self.sections_frame,
                text=section,
                text_color=COLOR_BG,
                variable=var,
                onvalue="on",
                offvalue="off",
                fg_color=COLOR_BUTTON,
                progress_color=COLOR_HOVER,
                border_color=COLOR_BORDER,
                width=200,
                height=20
            ).pack(pady=10)

        self.continue_button = customtkinter.CTkButton(
            self.sections_frame,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text="Continue",
            text_color=COLOR_TEXT,
            width=60,
            height=40,
            command=self.show_wiki_frame
        )
        self.continue_button.pack(pady=20)

    def show_wiki_frame(self):
        for widget in ["related_frame", "related_label", "sections_label"]:
            self.clear_widget(widget)

        if not hasattr(self, "scraper"):
            self.status_label.configure(text="Por favor, ingresa una URL y presiona search.", text_color=COLOR_ERROR_TEXT)
            return

        selected_sections = [sec for sec, var in self.section_vars.items() if var.get() == "on"]
        if not selected_sections:
            selected_sections = self.sections

        self.paragraphs = self.scraper.paragraphs_extractor(selected_sections)
        self.clear_widget("sections_frame")

        self.wiki_frame = customtkinter.CTkScrollableFrame(
            self, fg_color="white",
            width=1000, height=400
        )
        self.wiki_frame.place(relx=0.5, y=450, anchor="center")

        self.wiki_title_label = customtkinter.CTkLabel(
            self.wiki_frame,
            text=self.title,
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_BG,
            width=300,
            height=60
        )
        self.wiki_title_label.pack(pady=20)

        paragraphs_text = ""
        for section, paras in self.paragraphs.items():
            paragraphs_text += f"{section}\n" + "\n".join(paras) + "\n\n"

        self.paragraphs_label = customtkinter.CTkLabel(
            self.wiki_frame,
            text=paragraphs_text,
            justify="left",
            font=("Arial", 20, "bold"),
            text_color=COLOR_BG,
            width=960
        )
        self.paragraphs_label.configure(wraplength=960)
        self.paragraphs_label.pack(pady=20)

        self.report_gen_button = customtkinter.CTkButton(
            self, text="Generate",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            command=self.global_atributes
        )
        self.report_gen_button.place(relx=0.5, y=215, anchor="center")

    

    def global_atributes(self):
        shared_state.set_titulo(self.title)
        shared_state.set_parrafos(self.paragraphs)
        from reports.static_report import Generator_report
        Generator_report().generar()

# Scraper dinámico
class Dynamic_Scraper(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

        self.title_label = customtkinter.CTkLabel(
            self, text="REAL STATE",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        self.config_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=190, width=100)
        self.config_frame.place(relx=0.98, y=20, anchor="ne")

        self.buttom_frame = customtkinter.CTkFrame(self, fg_color=COLOR_BG, height=200, width=700)
        self.buttom_frame.place(relx=0.5, y=220, anchor="center")

        self.metro_button = customtkinter.CTkButton(
            self.buttom_frame, text="METRO \n CUADRADO",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER, border_width=5, border_color=COLOR_BORDER,
            command=lambda: parent.show_frame(parent.pantalla_metro_cuadrado)
        )
        self.metro_button.place(relx=0.17, rely=0.5, anchor="center")

        self.finca_button = customtkinter.CTkButton(
            self.buttom_frame, text="FINCA RAIZ",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER, border_width=5, border_color=COLOR_BORDER,
            command=lambda: parent.show_frame(parent.pantalla_finca_raiz)
        )
        self.finca_button.place(relx=0.5, rely=0.5, anchor="center")

        self.proper_button = customtkinter.CTkButton(
            self.buttom_frame, text="PROPERATI",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220, height=180, fg_color=COLOR_BUTTON,
            border_width=5, border_color=COLOR_BORDER,
            hover_color=COLOR_HOVER,
            command=lambda: parent.show_frame(parent.pantalla_properati)
        )
        self.proper_button.place(relx=0.83, rely=0.5, anchor="center")


class Pantalla_Properati(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.return_button_dynamic = customtkinter.CTkButton(
            self, text="", image=returnicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.return_button_dynamic.place(x=50, y=50, anchor="center")

        self.info_label = customtkinter.CTkLabel(
            self, text="PROPERATI",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.info_label.place(relx=0.5, y=60, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            
        )
        self.search_button.place(x=950, y=25, anchor="center")


        self.city_frame = customtkinter.CTkFrame(
            self, fg_color="white",
            height=150, width=485
        )
        self.city_frame.place(relx=0.49, y=275, anchor="e")

        self.list_frame = customtkinter.CTkFrame(
            self, fg_color="white",
            height=50, width=485
        )
        self.list_frame.place(relx=0.51, y=225, anchor="w")

        self.city_label = customtkinter.CTkLabel(self.city_frame,text="hola", text_color= "black")
        self.city_label.place(x = 20, rely = 0.5, anchor=("w"))
        
class Pantalla_Metro_Cuadrado(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.return_button_dynamic = customtkinter.CTkButton(
            self, text="", image=returnicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.return_button_dynamic.place(x=50, y=50, anchor="center")

        self.info_label = customtkinter.CTkLabel(
            self, text="METRO CUADRADO",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.info_label.place(relx=0.5, y=60, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            
        )
        self.search_button.place(x=950, y=25, anchor="center")

        self.city_frame = customtkinter.CTkFrame(
            self, fg_color="white",
            height=150, width=485
        )
        self.city_frame.place(relx=0.49, y=275, anchor="e")

        self.list_frame = customtkinter.CTkFrame(
            self, fg_color="white",
            height=50, width=485
        )
        self.list_frame.place(relx=0.51, y=225, anchor="w")

        self.city_label = customtkinter.CTkLabel(self.city_frame,text="hola", text_color= "black")
        self.city_label.place(x = 20, rely = 0.5, anchor=("w"))

class Pantalla_Properati(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.city_list = [
            "Bogota","Cucuta","Medellin","Barranquilla","Cali",
            "Bucaramanga","Yopal","Cartagena","Santa Marta",
            "Villavicencio","Tunja","Leticia","Manizales","Ibague"
        ]

        self.return_button_dynamic = customtkinter.CTkButton(
            self, text="", image=returnicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.return_button_dynamic.place(x=50, y=50, anchor="center")

        self.info_label = customtkinter.CTkLabel(
            self, text="PROPERATI",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.info_label.place(relx=0.5, y=60, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")

        self.url_entry.bind("<KeyRelease>", self.update_city_suggestions)
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            command = self.export_filters
        )
        self.search_button.place(x=950, y=25, anchor="center")

        
        self.city_scroll_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_BG,
            width=485, height=150
        )
        self.city_scroll_frame.place(relx=0.49, y=285, anchor="e")

        self.list_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=485
        )
        self.list_frame.place(relx=0.51, y=225, anchor="w")

        self.list_box_1 = customtkinter.CTkComboBox(self.list_frame, values=Properati.Types, width=318, height=30)
        self.list_box_1.place(x=147, rely=0.5, anchor="w")

        self.list_box_2 = customtkinter.CTkComboBox(self.list_frame, values=Properati.operationTypes, width=137, height=30)
        self.list_box_2.place(x=10, rely=0.5, anchor="w")

    def update_city_suggestions(self, event):
        typed = self.url_entry.get().strip()
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()

        if typed:
            for city in self.city_list:
                if typed.lower() in city.lower():
                    label = customtkinter.CTkLabel(
                        self.city_scroll_frame,
                        text=city,
                        text_color=COLOR_TITLE,
                        fg_color=COLOR_BUTTON,
                        corner_radius=50,
                        anchor="w",
                        justify="left"
                    )
                    label.pack(side="top", fill="x", padx=10, pady=2)
                    label.bind("<Button-1>", lambda e, c=city: self.select_city(c))

    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()


    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_frame.winfo_children():
            widget.destroy()


    def export_filters(self):
        filters.operation_type = self.list_box_2.get()
        filters.property_type = self.list_box_1.get()
        filters.city = self.url_entry.get()

        
class Pantalla_Metro_Cuadrado(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.city_list = [
            "Bogota","Cucuta","Medellin","Barranquilla","Cali",
            "Bucaramanga","Yopal","Cartagena","Santa Marta",
            "Villavicencio","Tunja","Leticia","Manizales","Ibague"
        ]

        self.return_button_dynamic = customtkinter.CTkButton(
            self, text="", image=returnicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.return_button_dynamic.place(x=50, y=50, anchor="center")

        self.info_label = customtkinter.CTkLabel(
            self, text="METRO CUADRADO",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.info_label.place(relx=0.5, y=60, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")

        self.url_entry.bind("<KeyRelease>", self.update_city_suggestions)
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            command = self.export_filters
        )
        self.search_button.place(x=950, y=25, anchor="center")

        
        self.city_scroll_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_BG,
            width=485, height=150
        )
        self.city_scroll_frame.place(relx=0.49, y=285, anchor="e")

        self.list_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=485
        )
        self.list_frame.place(relx=0.51, y=225, anchor="w")

        self.list_box_1 = customtkinter.CTkComboBox(self.list_frame, values=MetroCuadrado.Types, width=318, height=30)
        self.list_box_1.place(x=147, rely=0.5, anchor="w")

        self.list_box_2 = customtkinter.CTkComboBox(self.list_frame, values=MetroCuadrado.operationTypes, width=137, height=30)
        self.list_box_2.place(x=10, rely=0.5, anchor="w")

    def update_city_suggestions(self, event):
        typed = self.url_entry.get().strip()
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()

        if typed:
            for city in self.city_list:
                if typed.lower() in city.lower():
                    label = customtkinter.CTkLabel(
                        self.city_scroll_frame,
                        text=city,
                        text_color=COLOR_TITLE,
                        fg_color=COLOR_BUTTON,
                        corner_radius=50,
                        anchor="w",
                        justify="left"
                    )
                    label.pack(side="top", fill="x", padx=10, pady=2)
                    label.bind("<Button-1>", lambda e, c=city: self.select_city(c))

    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()


    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_frame.winfo_children():
            widget.destroy()

    def export_filters(self):
        filters.operation_type = self.list_box_2.get()
        filters.property_type = self.list_box_1.get()
        filters.city = self.url_entry.get()

class Pantalla_Finca_Raiz(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)

        self.city_list = [
            "Bogota","Cucuta","Medellin","Barranquilla","Cali",
            "Bucaramanga","Yopal","Cartagena","Santa Marta",
            "Villavicencio","Tunja","Leticia","Manizales","Ibague"
        ]

        self.return_button_dynamic = customtkinter.CTkButton(
            self, text="", image=returnicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.return_button_dynamic.place(x=50, y=50, anchor="center")

        self.info_label = customtkinter.CTkLabel(
            self, text="FINCA RAIZ",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.info_label.place(relx=0.5, y=60, anchor="center")

        self.url_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=990
        )
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame,
            placeholder_text="URL",
            width=900,
            height=30,
            fg_color=COLOR_FRAME,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.url_entry.place(x=460, y=25, anchor="center")

        self.url_entry.bind("<KeyRelease>", self.update_city_suggestions)
        
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search",
            width=60, height=30,
            fg_color=COLOR_BUTTON,
            hover_color=COLOR_HOVER,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            command = self.export_filters
        )
        self.search_button.place(x=950, y=25, anchor="center")

        
        self.city_scroll_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_BG,
            width=485, height=150
        )
        self.city_scroll_frame.place(relx=0.49, y=285, anchor="e")

        self.list_frame = customtkinter.CTkFrame(
            self, fg_color=COLOR_BG,
            height=50, width=485
        )
        self.list_frame.place(relx=0.51, y=225, anchor="w")

        self.list_box_1 = customtkinter.CTkComboBox(self.list_frame, values=FincaRaiz.Types, width=318, height=30)
        self.list_box_1.place(x=147, rely=0.5, anchor="w")

        self.list_box_2 = customtkinter.CTkComboBox(self.list_frame, values=FincaRaiz.operationTypes, width=137, height=30)
        self.list_box_2.place(x=10, rely=0.5, anchor="w")

    def update_city_suggestions(self, event):
        typed = self.url_entry.get().strip()
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()

        if typed:
            for city in self.city_list:
                if typed.lower() in city.lower():
                    label = customtkinter.CTkLabel(
                        self.city_scroll_frame,
                        text=city,
                        text_color=COLOR_TITLE,
                        fg_color=COLOR_BUTTON,
                        corner_radius=50,
                        anchor="w",
                        justify="left"
                    )
                    label.pack(side="top", fill="x", padx=10, pady=2)
                    label.bind("<Button-1>", lambda e, c=city: self.select_city(c))

    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_scroll_frame.winfo_children():
            widget.destroy()


    def select_city(self, city):
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, city)
        for widget in self.city_frame.winfo_children():
            widget.destroy()

    def export_filters(self):
        filters.operation_type = self.list_box_2.get()
        filters.property_type = self.list_box_1.get()
        filters.city = self.url_entry.get()



class Reports(BaseScreen):
    def __init__(self, parent):
        super().__init__(parent)
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=COLOR_BG,
            hover_color=COLOR_HOVER,
            width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")
        self.title_label = customtkinter.CTkLabel(
            self, text="REPORTS",
            font=("Segoe UI Black", 40, "bold"),
            text_color=COLOR_TITLE
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")
        self.files_frame = customtkinter.CTkScrollableFrame(
            self, fg_color=COLOR_BG, width=800, height=400
        )
        self.files_frame.place(relx=0.5, y=280, anchor="center")

    def refresh_files(self):
        config = load_config()
        reports_dir = config.get("reports_directory", os.path.join(os.path.expanduser("~"), "Downloads", "reports"))
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        allowed_exts = ('.pdf', '.xlsx', '.xls')
        for filename in os.listdir(reports_dir):
            if filename.lower().endswith(allowed_exts):
                filepath = os.path.join(reports_dir, filename)
                btn = customtkinter.CTkButton(
                    self.files_frame,
                    text=f"{os.path.splitext(filename)[0]}\nFile Type : {os.path.splitext(filename)[1].upper()}",
                    width=120,
                    height=80,
                    corner_radius=15,
                    fg_color=COLOR_BUTTON,
                    text_color="white",
                    font=("Segoe UI Black", 16, "bold"),
                    border_width=3,
                    border_color=COLOR_BORDER,
                    hover_color=COLOR_HOVER,
                    command=lambda path=filepath: os.startfile(path)
                )
                btn.pack(pady=5)

    def tkraise(self, aboveThis=None):
        self.refresh_files()
        super().tkraise(aboveThis)



if __name__ == "__main__":
    app = APPGUIGREEN()
    app.mainloop()
