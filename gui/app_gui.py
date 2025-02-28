import tkinter
import customtkinter
import shared_state
from PIL import Image, ImageTk, ImageSequence
from scraper.static_scraper import WIKISCRAPER

# Configuración de apariencia
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

class DKDE(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DKDE")
        self.configure(bg_color="#000000")

        
        self.gif_frame = customtkinter.CTkFrame(self, fg_color="#000000")
        self.gif_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        
        self.gif_image = Image.open('assets/spin.gif')
        self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.gif_image)]
        self.frame_count = len(self.frames)

        
        self.gif_label = tkinter.Label(self.gif_frame, bg="#000000")
        self.gif_label.place(relx=0.5, rely=0.5, anchor="center")

        
        self.animate_gif()

    def animate_gif(self):
        def update_gif(index):
            self.gif_label.config(image=self.frames[index])
            next_index = (index + 1) % self.frame_count  # Cicla de forma indefinida
            self.after(100, update_gif, next_index)  # Actualiza cada 100 ms
        update_gif(0)

class APPGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DataDigger")
        self.configure(bg_color="#111612")
        
        # Pantallas
       
        self.pantalla_principal = Pantalla_Principal(self)
        self.static_scraper = Static_Scraper(self)
        self.dynamic_scraper = Dynamic_Scraper(self)
        self.pantalla_informacion = Pantalla_Informacion(self)
        self.pantalla_creadores = Pantalla_Creadores(self)

        
        self.show_frame(self.pantalla_principal)

    def show_frame(self, frame):
        """Muestra el frame seleccionado y oculta los demás."""
        frame.tkraise()

class Pantalla_Principal(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#111612")

        # Imagen de fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Creacion de los Frames
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

        # Botones de información y configuración
        self.logo_button = customtkinter.CTkButton(
            self.info_frame,
            text="",
            image=logo,
            width=50,
            height=50,
            fg_color="#111612",
            command = lambda: parent.show_frame(parent.pantalla_creadores)
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
            fg_color="#111612",
            command=lambda: parent.show_frame(parent.pantalla_informacion)
        )
        self.question_button.pack(pady=10, padx=10)
        
        # Botones para acceder a los scrapers
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


class Pantalla_Creadores(customtkinter.CTkFrame):
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

        # Título de la pantalla
        self.title_label = customtkinter.CTkLabel(
            self, text="CREATORS", font=("Segoe UI Black", 40, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Nombre de los creadores
        self.creators_frame = customtkinter.CTkFrame(self, fg_color="light gray", height=500, width=400)
        self.creators_frame.place(relx = 0.5, y = 330, anchor = "center")
        self.creators_label = customtkinter.CTkLabel(
            self.creators_frame, 
            text=f"Jhon Sebastian Rodriguez Ramirez \n Sebastian Alejandro Alarcon Cespedes \n Yadieth Stefany Guevara Manrique",
            justify="center",
            font=("Arial", 20, "bold"),
            text_color="black", width=360, height=460
        )
        self.creators_label.place(relx = 0.5,rely = 0.5, anchor = "center")

class Pantalla_Informacion(customtkinter.CTkFrame):
    pass

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

        # Título de la pantalla
        self.title_label = customtkinter.CTkLabel(
            self, text="WIKI", font=("Segoe UI Black", 40, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Label de estado para mostrar mensajes al usuario
        self.status_label = customtkinter.CTkLabel(self, text="", height=30, width=400)
        self.status_label.place(relx=0.5, y=95, anchor="center")

        # Frame para ingresar la URL
        self.url_frame = customtkinter.CTkFrame(self, fg_color="#111612", height=50, width=990)
        self.url_frame.place(relx=0.5, y=155, anchor="center")
        
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
            self.url_frame, text="search", width=60, height=30,
            command=self.start_scraping
        )
        self.search_button.place(x=950, y=25, anchor="center")

    def start_scraping(self):
        # Limpieza de frames existentes
        if hasattr(self, "sections_frame") and self.sections_frame is not None:
            self.sections_frame.place_forget()
            self.sections_frame.destroy()
            self.sections_frame = None
        if hasattr(self, "wiki_frame") and self.wiki_frame is not None:
            self.wiki_frame.place_forget()
            self.wiki_frame.destroy()
            self.wiki_frame = None
        if hasattr(self, "related_frame") and self.related_frame is not None:
            self.related_frame.place_forget()
            self.related_frame.destroy()
            self.related_frame = None
        if hasattr(self, "sections_label"):
            self.sections_label.place_forget()
            self.sections_label.destroy()
            self.sections_label = None
        if hasattr(self, "related_label") and self.related_label is not None:
            self.related_label.place_forget()
            self.related_label.destroy()
            self.related_label = None


        

        
        self.search_url()
        
        self.show_related_frame()
        self.show_sections_frame()





    def search_url(self):
        self.url = self.url_entry.get().strip()
        if not self.url:
            self.status_label.configure(text="Por favor, ingresa una URL válida.", text_color="red")
            return
        
        try:
            self.scraper = WIKISCRAPER(self.url)
            self.title = self.scraper.title_extractor()
            self.sections = self.scraper.general_content_extractor()
            self.related_words = self.scraper.related_words_extractor()
            self.status_label.configure(text="URL cargada correctamente", text_color="#32ff7e")


            
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")

    # Muestra los temas relacionados
    
    def show_related_frame(self):
        if hasattr(self, "related_frame") and self.related_frame is not None:
            self.related_frame.destroy()
            self.related_frame = None
        elif hasattr(self, "related_label"):
            self.related_label.destroy()
            self.related_label = None

        self.related_label = customtkinter.CTkLabel(self,text = "Temas relacionados",font=("Segoe UI Black", 20, "bold"), text_color="#32ff7e")
        self.related_label.place(relx=0.3333333333, y=230, anchor = "center")  
        self.related_frame = customtkinter.CTkScrollableFrame(self, fg_color="#32ff7e", width=300, height=400)
        self.related_frame.place(relx=0.3333333333, y=460, anchor="center")

        
        for i, j in self.related_words.items():
            customtkinter.CTkButton(
                self.related_frame,
                text=i,
                text_color="#111612",
                width=200,
                height=20,
                command=lambda j=j: self.status_label.configure(text=j, text_color="red")
            ).pack(pady=10)

    # Muestra las secciones

    def show_sections_frame(self):
        if hasattr(self, "sections_frame") and self.sections_frame is not None:
            self.sections_frame.destroy()
            self.sections_frame = None
        
        elif hasattr(self, "sections_label"):
            self.sections_label.destroy()
            self.sections_label = None

        self.sections_label = customtkinter.CTkLabel(self,text = "Secciones",font=("Segoe UI Black", 20, "bold"), text_color="#32ff7e")
        self.sections_label.place(relx=0.6666666666, y=230, anchor = "center")
        self.sections_frame = customtkinter.CTkScrollableFrame(self, fg_color="#32ff7e", width=300, height=400)
        self.sections_frame.place(relx=0.6666666666, y=460, anchor="center")
      
        self.section_vars = {}
        
        for section in self.sections:
            var = customtkinter.StringVar(value="on")
            self.section_vars[section] = var
            customtkinter.CTkSwitch(self.sections_frame, text=section, text_color="#111612",
                                      variable=var, onvalue="on", offvalue="off",
                                      width=200, height=20).pack(pady=10)
        
        self.continue_button = customtkinter.CTkButton(self.sections_frame, fg_color="#111612",
                                                       text="Continue", width=60, height=40,
                                                       command=self.show_wiki_frame)
        self.continue_button.pack(pady=20)

    # Muestra una previsualización de la información

    def show_wiki_frame(self):
       
        if hasattr(self, "related_frame") and self.related_frame is not None:
            self.related_frame.place_forget()
            self.related_frame.destroy()
            self.related_frame = None
        if hasattr(self, "related_label") and self.related_label is not None:
            self.related_label.place_forget()
            self.related_label.destroy()
            self.related_label = None
        if hasattr(self, "sections_label"):
            self.sections_label.place_forget()
            self.sections_label.destroy()
            self.sections_label = None
        if hasattr(self, "related_label") and self.related_label is not None:
            self.related_label.place_forget()
            self.related_label.destroy()
            self.related_label = None

        
        if not hasattr(self, "scraper"):
            self.status_label.configure(text="Por favor, ingresa una URL y presiona search.", text_color="red")
            return

        selected_sections = [section for section, var in self.section_vars.items() if var.get() == "on"]
        if not selected_sections:
            selected_sections = self.sections

       
        self.paragraphs = self.scraper.paragraphs_extractor(selected_sections)
        
        
        if hasattr(self, "sections_frame") and self.sections_frame is not None:
            self.sections_frame.place_forget()
            self.sections_frame.destroy()
            self.sections_frame = None

        
        self.wiki_frame = customtkinter.CTkScrollableFrame(self, fg_color="light gray", width=1000, height=400)
        self.wiki_frame.place(relx=0.5, y=450, anchor="center")

        self.wiki_title_label = customtkinter.CTkLabel(
            self.wiki_frame, text=self.title,
            font=("Segoe UI Black", 40, "bold"),
            text_color="black", width=300, height=60
        )
        self.wiki_title_label.pack(pady=20)
        
        
        self.paragraphs_text = ""
        for section, paras in self.paragraphs.items():
            self.paragraphs_text += f"{section}\n"
            self.paragraphs_text += "\n".join(paras) + "\n\n"
            
        self.paragraphs_label = customtkinter.CTkLabel(
            self.wiki_frame,
            text=self.paragraphs_text,
            justify="left",
            font=("Arial", 20, "bold"),
            text_color="black", width=960
        )
        self.paragraphs_label.configure(wraplength=960)
        self.paragraphs_label.pack(pady=20)

        self.report_gen_button = customtkinter.CTkButton(
            self, text="Generate", width=60, height=30,
            command=self.global_atributes
        )
        self.report_gen_button.place(relx = 0.5, y = 215, anchor = "center")
    def global_atributes(self):
        shared_state.titulo = self.title
        shared_state.secciones = self.sections
        shared_state.parrafos = self.paragraphs_text



class Dynamic_Scraper(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.configure(fg_color="#111612")

        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        self.title_label = customtkinter.CTkLabel(
            self, text="REAL STATE", font=("Segoe UI Black", 40, "bold"), text_color="#32ff7e"
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

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
spin = customtkinter.CTkImage(light_image=Image.open(r'assets\spin.gif'),dark_image=Image.open(r'assets\spin.gif'))
if __name__ == "__main__":
    app = APPGUI()
    app.mainloop()
