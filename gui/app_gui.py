import tkinter
import customtkinter
from PIL import Image, ImageTk
from scraper.static_scraper import WIKISCRAPER


# Configuración de apariencia
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

class APPGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DataDigger")
        self.configure(bg_color="#111612")
        
        # Crear los tres Frames (pantallas) y mostrarlas/ocultarlas
        self.pantalla_principal = Pantalla_Principal(self)
        self.static_scraper = Static_Scraper(self)
        self.dynamic_scraper = Dynamic_Scraper(self)

    

        # Mostrar Pantalla_Principal al inicio
        self.show_frame(self.pantalla_principal)

    def show_frame(self, frame):
        """Muestra el frame seleccionado y oculta los demás."""
        frame.tkraise()  # Llevar el frame seleccionado al frente

class Pantalla_Principal(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#111612")

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Creación de los Frames
        self.buttom_frame = customtkinter.CTkFrame(self, fg_color="#111612", height=200, width=700)
        self.buttom_frame.place(relx=0.5, y=220, anchor="center")

        self.info_frame = customtkinter.CTkFrame(self, fg_color="#111612", height=60, width=60)
        self.info_frame.place(x=50, rely=1, anchor="s")

        self.config_frame = customtkinter.CTkFrame(self, fg_color="#111612", height=190, width=100)
        self.config_frame.place(relx=0.98, y=20, anchor="ne")

        self.version_frame = customtkinter.CTkFrame(self, fg_color="#111612", height=30, width=240)
        self.version_frame.place(relx=0.9, rely=1, anchor="s")

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="DATA DIGGER", font=("Segoe UI Black", 80, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=60, anchor="center")
        
        # Versión
        self.version_label = customtkinter.CTkLabel(
            self.version_frame, text="DATA DIGGER version 1.0", font=("Arial", 17, "bold"), text_color="#626262"
        )
        self.version_label.place(x=20, rely=0.5, anchor="w")

        # Botones
        self.logo_button = customtkinter.CTkButton(
            self.info_frame,
            text="",
            image=logo,
            width=50,
            height=50,
            fg_color="#111612"
        )
        self.logo_button.place(x=35, rely=0.5, anchor="center")
        
        self.config_button = customtkinter.CTkButton(
            self.config_frame,
            text="",
            image=configicon,
            width=60,
            height=60,
            fg_color="#111612"
        )
        self.config_button.pack(pady=10, padx=10)

        self.question_button = customtkinter.CTkButton(
            self.config_frame,
            text="",
            image=questionicon,
            width=60,
            height=60,
            fg_color="#111612"
        )
        self.question_button.pack(pady=10, padx=10)
        
        self.static_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="WIKI",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color="#0f0f0f",
            hover_color="#27ba58",
            border_width=5,
            border_color="#383838",
            command=lambda: parent.show_frame(parent.static_scraper)
        )
        self.static_button.place(relx=0.17, rely=0.5, anchor="center")

        self.dynamic_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="REAL STATE",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color="#0f0f0f",
            hover_color="#27ba58",
            border_width=5,
            border_color="#383838",
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.dynamic_button.place(relx=0.5, rely=0.5, anchor="center")

        self.coming_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="SOON...",
            text_color="#626262",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color="#0f0f0f",
            border_width=5,
            border_color="#383838"
        )
        self.coming_button.place(relx=0.83, rely=0.5, anchor="center")

class Static_Scraper(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#111612")
        self.parent = parent

        # Botón para regresar a Pantalla_Principal
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color="#111612", width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="WIKI", font=("Segoe UI Black", 40, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Crear Frame para la URL
        self.url_frame = customtkinter.CTkFrame(self, fg_color="light gray", height=50, width=990)
        self.url_frame.place(relx=0.5, y=150, anchor="center")
        
        # Entrada de la URL
        self.url_entry = customtkinter.CTkEntry(
            self.url_frame, 
            placeholder_text="URL",
            width=900,
            height=30,
        )
        self.url_entry.place(x=460, y=25, anchor="center")

        # Botón de búsqueda 
        self.search_button = customtkinter.CTkButton(
            self.url_frame, text="search", width=60, height=30, command = self.show_sections_frame
        )
        self.search_button.place(x=950, y=25, anchor="center")

        # Label para mostrar mensajes de estado o error
        self.status_label = customtkinter.CTkLabel(self, text="", height=30, width=400)
        self.status_label.place(relx=0.5, y=95, anchor="center")
    
    
         



    def show_sections_frame(self):
        #Crear Sections Frame
        self.sections_frame = customtkinter.CTkScrollableFrame(self,fg_color="light gray",width=300,height=400)
        self.sections_frame.place(relx=0.5,y=420,anchor="center")
        
        self.continue_button = customtkinter.CTkButton(self.sections_frame,fg_color="light gray",text="Continue",width=60,height=40,command=self.show_wiki_frame)
        self.continue_button.pack(pady=20)

        
        # Obtiene la URL ingresada en el entry
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="Por favor, ingresa una URL.", text_color="red")
            return

        sections = []
        try:
            wiki = WIKISCRAPER(url)
            title = wiki.title_extractor()
            sections = wiki.general_content_extractor()
            paragraphs = wiki.paragraphs_extractor(sections)
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")
            return  # O finalizar el método aquí para que no se ejecute el resto
        for i in sections:
            customtkinter.CTkSwitch(self.sections_frame, text=i, width=200, height=20).pack(pady=10)
        
    def show_wiki_frame(self):

        #Crear Frame del Wiki

        self.wiki_frame = customtkinter.CTkScrollableFrame(self,fg_color="light gray",width=1000,height=400)
        self.wiki_frame.place(relx=0.5,y=420,anchor="center")

        self.wiki_title_label = customtkinter.CTkLabel(self.wiki_frame,text="BOGOTAZO",font=("Segoe UI Black", 40, "bold"), text_color="black",width= 300,height= 60)
        self.wiki_title_label.pack(pady=20)
        
        self.paragraphs_label = customtkinter.CTkLabel(self.wiki_frame,
        text="Se conoce como el Bogotazo a una serie de disturbios ocurridos en Bogotá, la capital de Colombia, como consecuencia del magnicidio del líder del Partido Liberal, Jorge Eliécer Gaitán, ocurrido el 9 de abril de 1948.El presunto autor material del magnicidio, Juan Roa Sierra, fue perseguido y linchado por una multitud que, posteriormente, arrastró su cadáver hasta la Casa de Nariño.1La ola de protestas, que también se expandió a otras ciudades y regiones del país, desencadenó el recrudecimiento de la época conocida en el país como «La Violencia», que terminó aparentemente diez años después, en 1958. Las consecuencias, sin embargo, duraron más de lo imaginado por cuenta del conflicto armado interno que ha tenido como protagonistas a la Fuerza Pública, a grupos guerrilleros y paramilitares, bandas criminales y narcotráfico en Colombia.En el primer gobierno de Alberto Lleras Camargo (quien asume por renuncia del titular Alfonso López Pumarejo), el Partido Liberal se dividió en torno a dos candidatos para las elecciones del 5 de mayo de 1946: Gabriel Turbay, el candidato oficial, y Jorge Eliécer Gaitán, el candidato disidente. Esta división facilitó que el Partido Conservador acabara con 16 años de presidencias liberales al ganar las elecciones con su candidato único, Mariano Ospina Pérez.2En las elecciones, Ospina Pérez alcanzó aproximadamente 565 000 votos; Gabriel Turbay 441 000 y Gaitán 100 000. Al asumir el mandato, Ospina Pérez planteó un gobierno de Unidad nacional con la participación de ambos partidos, que nunca se concretó.3",
        justify ="left",
        font=("Arial", 20, "bold"), 
        text_color="black",
        width= 960
        )
        self.paragraphs_label.configure(wraplength=960)
        self.paragraphs_label.pack(pady =20)
        
        
    

    
        
        
        


class Dynamic_Scraper(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#111612")

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="REAL STATE", font=("Segoe UI Black", 40, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Botón para regresar a Pantalla_Principal
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color="#111612", width=60, height=60,
            command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

# Definir Imágenes
logo = customtkinter.CTkImage(light_image=Image.open('assets/logo2.png'),dark_image=Image.open('assets/logo2.png'),size=(50, 50)) 
bgimage = customtkinter.CTkImage(light_image=Image.open(r'assets/bgimage.png'),dark_image=Image.open(r'assets/bgimage.png'),size=(1381.25, 1056))
questionicon = customtkinter.CTkImage(light_image=Image.open(r'assets\Questionicon.png'),dark_image=Image.open(r'assets\Questionicon.png'),size=(60,60))
configicon = customtkinter.CTkImage(light_image=Image.open(r'assets\configicon.png'),dark_image=Image.open(r'assets\configicon.png'),size=(60,60))
homeicon = customtkinter.CTkImage(light_image=Image.open(r'assets\homeicon.png'),dark_image=Image.open(r'assets\homeicon.png'),size=(60,60))

if __name__ == "__main__":
    app = APPGUI()
    app.mainloop()
