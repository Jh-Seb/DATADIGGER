import tkinter
import customtkinter
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

# Definir Imágenes
logo = customtkinter.CTkImage(light_image=Image.open('assets/logo2.png'), dark_image=Image.open('assets/logo2.png'), size=(50, 50))
bgimage = customtkinter.CTkImage(light_image=Image.open(r'assets/bgimage.png'), dark_image=Image.open(r'assets/bgimage.png'), size=(1381.25, 1056))
questionicon = customtkinter.CTkImage(light_image=Image.open(r'assets\Questionicon.png'), dark_image=Image.open(r'assets\Questionicon.png'), size=(60, 60))
configicon = customtkinter.CTkImage(light_image=Image.open(r'assets\configicon.png'), dark_image=Image.open(r'assets\configicon.png'), size=(60, 60))
homeicon = customtkinter.CTkImage(light_image=Image.open(r'assets\homeicon.png'), dark_image=Image.open(r'assets\homeicon.png'), size=(60, 60))

# Clases de Temas
class Theme:
    def __init__(self):
        self.bg_color = "#111612"
        self.text_color = "#32ff7e"
        self.button_fg_color = "#0f0f0f"
        self.button_hover_color = "#27ba58"
        self.button_border_color = "#383838"
        self.secondary_text_color = "#626262"
        self.frame_fg_color = "#111612"
        self.icon_size = (60, 60)
        self.logo_size = (50, 50)
        self.bg_image_path = 'assets/bgimage.png'
        self.logo_path = 'assets/logo2.png'
        self.question_icon_path = 'assets/Questionicon.png'
        self.config_icon_path = 'assets/configicon.png'
        self.home_icon_path = 'assets/homeicon.png'

class Green_Theme(Theme):
    def __init__(self):
        super().__init__()
        pass

class Pink_Theme(Theme):
    def __init__(self):
        super().__init__()
        self.bg_color = "#1a1a1a"
        self.text_color = "#ff69b4"
        self.button_hover_color = "#ff1493"

class Arcane_Theme(Theme):
    def __init__(self):
        super().__init__()
        self.bg_color = "#1a1a1a"
        self.text_color = "#ff4500"
        self.button_hover_color = "#ff8c00"

class Blue_Theme(Theme):
    def __init__(self):
        super().__init__()
        self.bg_color = "#1a1a1a"
        self.text_color = "#1e90ff"
        self.button_hover_color = "#00bfff"

# Ventana de Configuración
class Config_Window(customtkinter.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.geometry("400x300")
        self.title("Configuración")
        self.configure(bg_color="#111612")

        self.theme_label = customtkinter.CTkLabel(self, text="Selecciona un tema:", font=("Arial", 20, "bold"))
        self.theme_label.pack(pady=10)

        self.theme_var = customtkinter.StringVar(value="Green")

        self.green_theme_radio = customtkinter.CTkRadioButton(
            self, text="Green Theme", variable=self.theme_var, value="Green", command=self.change_theme
        )
        self.green_theme_radio.pack(pady=5)

        self.pink_theme_radio = customtkinter.CTkRadioButton(
            self, text="Pink Theme", variable=self.theme_var, value="Pink", command=self.change_theme
        )
        self.pink_theme_radio.pack(pady=5)

        self.arcane_theme_radio = customtkinter.CTkRadioButton(
            self, text="Arcane Theme", variable=self.theme_var, value="Arcane", command=self.change_theme
        )
        self.arcane_theme_radio.pack(pady=5)

        self.blue_theme_radio = customtkinter.CTkRadioButton(
            self, text="Blue Theme", variable=self.theme_var, value="Blue", command=self.change_theme
        )
        self.blue_theme_radio.pack(pady=5)

    def change_theme(self):
        selected_theme = self.theme_var.get()
        if selected_theme == "Green":
            self.parent.current_theme = Green_Theme()
        elif selected_theme == "Pink":
            self.parent.current_theme = Pink_Theme()
        elif selected_theme == "Arcane":
            self.parent.current_theme = Arcane_Theme()
        elif selected_theme == "Blue":
            self.parent.current_theme = Blue_Theme()

        self.parent.apply_theme()

# Clase Principal de la Aplicación
class APPGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DataDigger")
        
        # Tema inicial
        self.current_theme = Green_Theme()

        # Crear los tres Frames (pantallas) y mostrarlas/ocultarlas
        self.pantalla_principal = Pantalla_Principal(self)
        self.static_scraper = Static_Scraper(self)
        self.dynamic_scraper = Dynamic_Scraper(self)

        # Aplicar el tema después de crear los frames
        self.apply_theme()

        # Mostrar Pantalla_Principal al inicio
        self.show_frame(self.pantalla_principal)

    def apply_theme(self):
        """ Aplica el tema actual a toda la aplicación """
        self.configure(bg_color=self.current_theme.bg_color)
        self.pantalla_principal.configure(fg_color=self.current_theme.bg_color)
        self.static_scraper.configure(fg_color=self.current_theme.bg_color)
        self.dynamic_scraper.configure(fg_color=self.current_theme.bg_color)

        # Aplicar el tema a los botones
        self.pantalla_principal.static_button.configure(fg_color=self.current_theme.button_fg_color, hover_color=self.current_theme.button_hover_color, border_color=self.current_theme.button_border_color)
        self.pantalla_principal.dynamic_button.configure(fg_color=self.current_theme.button_fg_color, hover_color=self.current_theme.button_hover_color, border_color=self.current_theme.button_border_color)
        self.pantalla_principal.coming_button.configure(fg_color=self.current_theme.button_fg_color, border_color=self.current_theme.button_border_color)

        # Aplicar el tema a las etiquetas
        self.pantalla_principal.title_label.configure(text_color=self.current_theme.text_color)
        self.pantalla_principal.version_label.configure(text_color=self.current_theme.secondary_text_color)

    def show_frame(self, frame):
        """ Muestra el frame seleccionado, y oculta los demás """
        frame.tkraise()  # Llevar el frame seleccionado al frente

    def open_config_window(self):
        """ Abre la ventana de configuración """
        config_window = Config_Window(self)
        config_window.grab_set()  # Hace que la ventana de configuración sea modal

# Pantalla Principal
class Pantalla_Principal(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)  # Expande el frame para llenar toda la ventana
        self.configure(fg_color=parent.current_theme.bg_color)

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Creación de los Frames
        self.buttom_frame = customtkinter.CTkFrame(self, fg_color=parent.current_theme.bg_color, height=200, width=700)
        self.buttom_frame.place(relx=0.5, y=220, anchor="center")

        self.info_frame = customtkinter.CTkFrame(self, fg_color=parent.current_theme.bg_color, height=60, width=60)
        self.info_frame.place(x=50, rely=1, anchor="s")

        self.config_frame = customtkinter.CTkFrame(self, fg_color=parent.current_theme.bg_color, height=190, width=100)
        self.config_frame.place(relx=0.98, y=20, anchor="ne")

        self.version_frame = customtkinter.CTkFrame(self, fg_color=parent.current_theme.bg_color, height=30, width=240)
        self.version_frame.place(relx=0.9, rely=1, anchor="s")

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="DATA DIGGER", font=("Segoe UI Black", 80, "bold"), text_color=parent.current_theme.text_color
        )
        self.title_label.place(relx=0.5, y=60, anchor="center")
        
        # Versión
        self.version_label = customtkinter.CTkLabel(
            self.version_frame, text="DATA DIGGER version 1.0", font=("Arial", 17, "bold"), text_color=parent.current_theme.secondary_text_color
        )
        self.version_label.place(x=20, rely=0.5, anchor="w")

        # Botones
        self.logo_button = customtkinter.CTkButton(
            self.info_frame,
            text="",
            image=logo,
            width=50,
            height=50,
            fg_color=parent.current_theme.bg_color
        )
        self.logo_button.place(x=35, rely=0.5, anchor="center")
        
        self.config_button = customtkinter.CTkButton(
            self.config_frame,
            text="",
            image=configicon,
            width=60,
            height=60,
            fg_color=parent.current_theme.bg_color,
            command=parent.open_config_window
        )
        self.config_button.pack(pady=10, padx=10)

        self.question_button = customtkinter.CTkButton(
            self.config_frame,
            text="",
            image=questionicon,
            width=60,
            height=60,
            fg_color=parent.current_theme.bg_color
        )
        self.question_button.pack(pady=10, padx=10)
        
        self.static_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="WIKI",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color=parent.current_theme.button_fg_color,
            hover_color=parent.current_theme.button_hover_color,
            border_width=5,
            border_color=parent.current_theme.button_border_color,
            command=lambda: parent.show_frame(parent.static_scraper)
        )
        self.static_button.place(relx=0.17, rely=0.5, anchor="center")

        self.dynamic_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="REAL STATE",
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color=parent.current_theme.button_fg_color,
            hover_color=parent.current_theme.button_hover_color,
            border_width=5,
            border_color=parent.current_theme.button_border_color,
            command=lambda: parent.show_frame(parent.dynamic_scraper)
        )
        self.dynamic_button.place(relx=0.5, rely=0.5, anchor="center")

        self.coming_button = customtkinter.CTkButton(
            self.buttom_frame,
            text="SOON...",
            text_color=parent.current_theme.secondary_text_color,
            font=("Tw Cen MT Condensed Extra Bold", 40, "bold"),
            width=220,
            height=180,
            fg_color=parent.current_theme.button_fg_color,
            border_width=5,
            border_color=parent.current_theme.button_border_color
        )
        self.coming_button.place(relx=0.83, rely=0.5, anchor="center")

# Pantalla Static Scraper
class Static_Scraper(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)  # Expande el frame para llenar toda la ventana
        self.configure(fg_color=parent.current_theme.bg_color)

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="WIKI", font=("Segoe UI Black", 40, "bold"), text_color=parent.current_theme.text_color
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Crear Frames
        self.url_frame = customtkinter.CTkFrame(
            self, fg_color="light gray", height=30, width=900
        )
        self.url_frame.place(relx=0.5, y=100, anchor="center")
        
        # Botón para regresar a Pantalla_Principal
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=parent.current_theme.bg_color, width=60, height=60, command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50, anchor="center")

# Pantalla Dynamic Scraper
class Dynamic_Scraper(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)  # Expande el frame para llenar toda la ventana
        self.configure(fg_color=parent.current_theme.bg_color)

        # Fondo
        self.bg_image = customtkinter.CTkLabel(self, text="", image=bgimage)
        self.bg_image.place(relx=0.7, rely=0.9, anchor="center", relwidth=1, relheight=1)

        # Título principal
        self.title_label = customtkinter.CTkLabel(
            self, text="REAL STATE", font=("Segoe UI Black", 40, "bold"), text_color=parent.current_theme.text_color
        )
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # Botón para regresar a Pantalla_Principal
        self.house_button = customtkinter.CTkButton(
            self, text="", image=homeicon, fg_color=parent.current_theme.bg_color, width=60, height=60, command=lambda: parent.show_frame(parent.pantalla_principal)
        )
        self.house_button.place(x=50, y=50)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = APPGUI()
    app.mainloop()