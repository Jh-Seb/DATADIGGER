import tkinter
import customtkinter
import shared_state
from PIL import Image, ImageTk, ImageSequence
from scraper.static_scraper import WIKISCRAPER

# Configuración de apariencia
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.deactivate_automatic_dpi_awareness()

spin = customtkinter.CTkImage(
    light_image=Image.open(r'assets/spin.gif'),
    dark_image=Image.open(r'assets/spin.gif')
)

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