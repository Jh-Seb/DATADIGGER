import pandas as pd
import os

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

if __name__ == "__main__":
    print('Seleccione una página:')
    try:
        numero = int(input(""" 1. Properati
 2. Fincaraiz
"""))

        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        
        if numero == 1:
            input_csv = os.path.join(os.getcwd(), "data_properati.csv")  # Buscar en la carpeta del script
            output_excel = os.path.join(downloads_folder, "data_properati.xlsx")
        elif numero == 2:
            input_csv = os.path.join(os.getcwd(), "data_fincaraiz.csv")
            output_excel = os.path.join(downloads_folder, "data_fincaraiz.xlsx")
        else:
            print("Opción inválida. Debe ser 1 o 2.")
            exit()

        # Convierte CSV a Excel
        convert_csv_to_excel(input_csv, output_excel)

    except ValueError:
        print("Error: Debe ingresar un número válido (1 o 2).")