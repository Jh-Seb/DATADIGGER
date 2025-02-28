import os
import sys

# Agrega el directorio raíz del proyecto al sys.path para que se encuentren todos los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from gui.app_gui import APPGUI, DKDE
from reports.report_generator import generar_reporte

def main():
    if os.path.exists(r"coco.jpeg"):
        app = APPGUI()
    else:
        app = DKDE()
    
    app.mainloop()

    # Una vez que se cierra la GUI, se puede generar el reporte usando la variable compartida
    generar_reporte()

if __name__ == "__main__":
    main()
