import os
import re
import shared_state
from fpdf import FPDF  
from pathlib import Path
from config_manager import load_config


# Función para limpiar el texto y evitar caracteres no compatibles 
def limpiar_texto(texto):
                texto = re.sub(r'[\u200b\u202a\u202c]', '', texto)  
                return texto.encode('latin-1', 'ignore').decode('latin-1')

# Clase personalizada para generar reportes en PDF
class ReportPDF(FPDF):
        def header(self):
                self.set_font("Times",'', 10)
                self.cell(0, 10,"Extracto de Wikipedia", 0, 1, 'C')
        
        def footer(self):
                self.set_y(-15)
                self.set_font("Times", 'B', 8)
                self.cell(0, 10, f'{self.page_no()}', 0, 0, 'R')
        
        def nickname(self, title): 
                self.set_font("Times", 'B', 16)
                self.cell(0,10, limpiar_texto(title), 0, 1, 'C')
                self.ln(10)
        
        def indice(self, secciones, parrafos):
                self.set_font("Times", 'B', 14)
                self.cell(0,10, limpiar_texto(secciones), 0, 1, 'L')
                self.ln(3)

                for parrafo in parrafos:
                      self.set_font("Times", '', 12)
                      self.multi_cell(0,10,limpiar_texto(parrafo), align='L')
                      self.ln(3)

# Clase para generar el PDF con los datos obtenidos             
class Generator_report(ReportPDF):
        def __init__(self):
                super().__init__()
                self.set_auto_page_break(auto = True, margin = 15)

        def generar(self):
                self.add_page()
                titulo = shared_state.get_titulo()
                self.nickname(titulo)
                parrafos = shared_state.get_parrafos()
                palabras = shared_state.get_palabras_relacionadas()
                for seccion, parrafos in parrafos.items():
                        self.indice(seccion, parrafos)
                  
                filename = f'{titulo}.pdf'
                config = load_config()
                directory = config.get("reports_directory", "C:\\Users\\JHON\\Downloads\\reports").lower()
                file_path = os.path.join(directory, filename)
                self.output(file_path)
                os.startfile(file_path)
                print('Reporte generado exitosamente')


if __name__ == '__main__':
    reporte = Generator_report()
    reporte.generar()
