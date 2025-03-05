import tkinter
import customtkinter
import shared_state
from PIL import Image, ImageTk, ImageSequence
from scraper.static_scraper import WIKISCRAPER

# Configuración de la apariencia y DPI
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

# Carga de la imagen de spinner para temas claro y oscuro
spin = customtkinter.CTkImage(
    light_image=Image.open(r'assets/spin.gif'),
    dark_image=Image.open(r'assets/spin.gif')
)

# Clase principal de la aplicación
class DKDE(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.title("DKDE")
        self.configure(bg_color="#000000")

        # Frame para mostrar el GIF animado
        self.gif_frame = customtkinter.CTkFrame(self, fg_color="#000000")
        self.gif_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        # Carga del GIF y preparación de sus frames
        self.gif_image = Image.open('assets/spin.gif')
        self.frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(self.gif_image)]
        self.frame_count = len(self.frames)

        # Label para mostrar la animación
        self.gif_label = tkinter.Label(self.gif_frame, bg="#000000")
        self.gif_label.place(relx=0.5, rely=0.5, anchor="center")

        # Inicia la animación del GIF
        self.animate_gif()

    # Método para animar el GIF en el label
    def animate_gif(self):
        def update_gif(index):
            self.gif_label.config(image=self.frames[index])
            next_index = (index + 1) % self.frame_count  # Ciclo continuo
            self.after(100, update_gif, next_index)  # Actualiza cada 100 ms
        update_gif(0)
