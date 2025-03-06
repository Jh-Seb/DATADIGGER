import pandas as pd
import os
from config_manager import load_config

def convert_csv_to_excel(csv_path, excel_path):
    """
    Lee un archivo CSV usando coma como delimitador y lo guarda como archivo Excel.
    :param csv_path: Ruta del archivo CSV de entrada.
    :param excel_path: Ruta del archivo Excel de salida.
    """
    try:
        if not os.path.exists(csv_path):
            print(f"Error: El archivo {csv_path} no existe.")
            return
        
        # Lee el CSV, forzando la coma como delimitador
        df = pd.read_csv(csv_path, sep=',', encoding='utf-8')

        # Guarda el DataFrame como archivo Excel
        df.to_excel(excel_path, index=False)
        print(f"Archivo Excel generado correctamente en: {excel_path}")
    
    except Exception as e:
        print(f"Error al convertir el archivo: {e}")
def generar():
    print('Seleccione una página:')
    try:
        numero = int(input(""" 1. Properati
 2. Fincaraiz
"""))
        config = load_config()
        directory = config.get("reports_directory", "C:\\Users\\JHON\\Downloads\\reports").lower()
        downloads_folder = os.path.join(directory)
        
        
        input_csv = os.path.join(os.getcwd(), "data_properati.csv")  # Buscar en la carpeta del script
        output_excel = os.path.join(downloads_folder, "data_properati.xlsx")
        

        # Convierte CSV a Excel
        convert_csv_to_excel(input_csv, output_excel)

    except ValueError:
        print("Error: Debe ingresar un número válido (1 o 2).")

if __name__ == '__main__':
    generar()
