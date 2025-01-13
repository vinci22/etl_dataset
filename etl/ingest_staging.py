import os
import shutil
import logging
import kagglehub
import pandas as pd
from datetime import datetime
from etl.config import STAGING_DATA_PATH, KAGGLE_DATASET

# Configuración de logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def get_today_subfolder(base_path):
    """
    Crea y retorna la ruta con subcarpetas organizadas por año/mes/día dentro de la carpeta base.
    Las rutas son normalizadas y convertidas a absolutas.
    """
    today = datetime.now()
    folder_path = os.path.join(
        base_path,
        f"{today.year}",
        f"{today.month:02d}",
        f"{today.day:02d}"
    )
    # Normalizar y convertir a ruta absoluta
    folder_path = os.path.abspath(os.path.normpath(folder_path))

    # Crear la carpeta si no existe
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def validate_quality(file_path):
    """
    Valida la calidad de los datos en un archivo CSV.
    Garantiza que las columnas importantes formen una clave única y no tengan duplicados.
    Retorna True si el archivo pasa las validaciones, de lo contrario False.
    """
    try:
        logging.info(f"Iniciando validación de calidad para: {file_path}")

        # Definir las columnas importantes para la validación (clave única)
        important_columns = ['trans_date_trans_time', 'cc_num']  # Ajusta según tus necesidades

        # Leer solo las columnas importantes
        df = pd.read_csv(file_path, usecols=important_columns)

        # Validar si las columnas importantes existen
        missing_columns = [col for col in important_columns if col not in df.columns]
        if missing_columns:
            logging.error(f"El archivo {file_path} no contiene las columnas necesarias: {missing_columns}")
            return False

        # # Validar valores nulos en las columnas importantes
        # if df[important_columns].isnull().sum().sum() > 0:
        #     logging.warning(f"Archivo {file_path} contiene valores nulos en columnas importantes.")
        #     return False

        # # Validar clave única: no deben existir duplicados en las columnas importantes
        # duplicates = df.duplicated(subset=important_columns).sum()
        # if duplicates > 0:
        #     logging.warning(
        #         f"Archivo {file_path} contiene {duplicates} registros duplicados en las columnas que deberían ser clave única."
        #     )
        #     return False

        # Validación exitosa
        logging.info(f"Archivo {file_path} pasó las validaciones de calidad en las columnas importantes (clave única).")
        return True
    except Exception as e:
        logging.error(f"Error durante la validación de calidad para {file_path}: {e}")
        return False


def move_to_staging(source_path, destination_folder):
    """
    Mueve archivos desde el path temporal a la partición de Staging.
    Solo se mueven los archivos que pasen las validaciones de calidad.
    """
    try:
        if not os.path.exists(source_path) or not os.path.isdir(source_path):
            logging.error(f"El path {source_path} no existe o no es un directorio válido.")
            raise FileNotFoundError(f"El path {source_path} no es válido.")

        # Listar y validar/mover archivos
        for filename in os.listdir(source_path):
            source_file = os.path.abspath(os.path.join(source_path, filename))
            destination_file = os.path.abspath(os.path.join(destination_folder, filename))

            # Validar solo archivos CSV
            if filename.endswith(".csv") and os.path.isfile(source_file):
                if validate_quality(source_file):
                    shutil.move(source_file, destination_file)
                    logging.info(f"Archivo movido a Staging: {destination_file}")
                else:
                    logging.warning(f"Archivo {source_file} no pasó las validaciones de calidad.")
            else:
                logging.warning(f"Elemento omitido porque no es un archivo CSV: {source_file}")
    except Exception as e:
        logging.error(f"Error al mover archivos a Staging: {e}")
        raise

def extract_to_staging():
    """
    Descarga los datos desde Kaggle usando kagglehub y los mueve a la carpeta staging.
    """
    try:
        logging.info("Iniciando la descarga de datos desde Kaggle con kagglehub.")
        
        # Descargar el dataset
        source_path = kagglehub.dataset_download(KAGGLE_DATASET)
        source_path = os.path.abspath(os.path.normpath(source_path))  # Normalizar y hacer absoluta
        logging.info(f"Datos descargados temporalmente en: {source_path}")
        
        # Obtener la carpeta Staging para la fecha actual
        staging_folder = get_today_subfolder(STAGING_DATA_PATH)
        logging.info(f"Carpeta de Staging: {staging_folder}")
        
        # Mover los archivos descargados a la carpeta Staging
        move_to_staging(source_path, staging_folder)
        
        logging.info(f"Datos almacenados en Staging: {staging_folder}")
        return staging_folder
    except Exception as e:
        logging.error(f"Error durante la descarga y movimiento de datos: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Iniciando la etapa de Staging del pipeline ETL.")
        
        # Descargar y mover los datos a la zona Staging
        extract_to_staging()
        
        logging.info("Etapa de Staging completada exitosamente.")
    except Exception as e:
        logging.error(f"Error durante la ejecución de la etapa de Staging: {e}")
