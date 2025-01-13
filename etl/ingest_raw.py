import os
import shutil
import logging
import pandas as pd
from datetime import datetime
from etl.config import STAGING_DATA_PATH, RAW_DATA_PATH

# Configuración de logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def get_today_subfolder(base_path):
    """
    Crea y retorna la ruta con subcarpetas organizadas por año/mes/día dentro de la carpeta base.
    """
    today = datetime.now()
    folder_path = os.path.join(
        base_path,
        f"{today.year}",
        f"{today.month:02d}",
        f"{today.day:02d}"
    )
    # Crear la carpeta si no existe
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def format_file(file_path, destination_folder):
    """
    Lee el archivo desde staging, le da formato consistente y lo guarda en la carpeta RAW.
    """
    try:
        # Leer el archivo original
        df = pd.read_csv(file_path)

        # Renombrar columnas para asegurar consistencia (opcional)
        df.columns = df.columns.str.lower().str.replace(" ", "_")

        # Asegurarse de que las fechas estén en el formato correcto (opcional)
        if 'trans_date_trans_time' in df.columns:
            df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])

        # Ruta del archivo formateado
        formatted_file_name = os.path.basename(file_path).replace(".csv", "_formatted.csv")
        formatted_file_path = os.path.join(destination_folder, formatted_file_name)

        # Guardar el archivo en formato CSV
        df.to_csv(formatted_file_path, index=False)
        logging.info(f"Archivo formateado y movido a RAW: {formatted_file_path}")
    except Exception as e:
        logging.error(f"Error al dar formato al archivo {file_path}: {e}")
        raise

def process_staging_to_raw():
    """
    Mueve los archivos desde la carpeta STAGING a RAW, dándoles formato consistente.
    """
    try:
        # Obtener las carpetas particionadas por fecha
        staging_folder = get_today_subfolder(STAGING_DATA_PATH)
        raw_folder = get_today_subfolder(RAW_DATA_PATH)

        # Procesar cada archivo en la carpeta STAGING
        for filename in os.listdir(staging_folder):
            staging_file_path = os.path.join(staging_folder, filename)

            # Procesar solo archivos CSV
            if filename.endswith(".csv"):
                logging.info(f"Procesando archivo desde Staging: {staging_file_path}")

                # Formatear y mover el archivo a RAW
                format_file(staging_file_path, raw_folder)

                # Eliminar el archivo original de Staging
                os.remove(staging_file_path)
                logging.info(f"Archivo original eliminado de Staging: {staging_file_path}")
            else:
                logging.warning(f"Elemento no procesado porque no es un archivo CSV: {staging_file_path}")
    except Exception as e:
        logging.error(f"Error durante el procesamiento de datos de Staging a RAW: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Iniciando la transferencia de datos de Staging a RAW.")
        
        # Procesar datos desde Staging a RAW
        process_staging_to_raw()
        
        logging.info("Transferencia de datos completada exitosamente.")
    except Exception as e:
        logging.error(f"Error en la transferencia de datos de Staging a RAW: {e}")
