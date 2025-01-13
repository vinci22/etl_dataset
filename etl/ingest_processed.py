import os
import logging
import pandas as pd
from datetime import datetime
from etl.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

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

def transform_data(df):
    """
    Transforma los datos RAW a datos procesados.
    """
    try:
        # Transformaciones basadas en la lógica proporcionada
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        df['transaction_hour'] = df['trans_date_trans_time'].dt.hour
        df['transaction_day'] = df['trans_date_trans_time'].dt.day
        df['transaction_month'] = df['trans_date_trans_time'].dt.month
        df['transaction_year'] = df['trans_date_trans_time'].dt.year

        # Imputación y transformación de variables
        df['merch_zipcode'] = df['merch_zipcode'].fillna(0).astype(int)
        df['merchant_category'] = df['merchant'].str.replace(r'^fraud_', '', regex=True)
        df['is_fraud_target'] = df['is_fraud'].astype(int)

        # Codificación de variables categóricas
        df['category_encoded'] = pd.factorize(df['category'])[0]
        df['gender_encoded'] = pd.factorize(df['gender'])[0]

        # Eliminar columnas innecesarias
        columns_to_drop = ['Unnamed: 0.1', 'Unnamed: 0', 'cc_num', 'merchant', 'trans_num', 'is_fraud']
        df = df.drop(columns=columns_to_drop, errors='ignore')
        return df
    except Exception as e:
        logging.error(f"Error durante la transformación de datos: {e}")
        raise

def process_raw_data():
    """
    Procesa los datos RAW y los guarda en la carpeta PROCESSED.
    """
    try:
        # Obtener carpeta RAW y PROCESSED para hoy
        raw_folder = get_today_subfolder(RAW_DATA_PATH)
        processed_folder = get_today_subfolder(PROCESSED_DATA_PATH)

        # Procesar cada archivo en la carpeta RAW
        for filename in os.listdir(raw_folder):
            raw_file_path = os.path.join(raw_folder, filename)

            # Procesar solo archivos CSV
            if filename.endswith(".csv"):
                logging.info(f"Procesando archivo RAW: {raw_file_path}")

                # Leer datos
                df_raw = pd.read_csv(raw_file_path)

                # Transformar datos
                df_transformed = transform_data(df_raw)

                # Guardar datos transformados
                processed_file_path = os.path.join(processed_folder, f"{filename.split('.')[0]}.parquet")
                df_transformed.to_parquet(processed_file_path, index=False)
                logging.info(f"Archivo procesado guardado en: {processed_file_path}")
    except Exception as e:
        logging.error(f"Error durante el procesamiento de datos RAW: {e}")
        raise

if __name__ == "__main__":
    try:
        logging.info("Iniciando la etapa de transformación de datos.")

        # Procesar los datos desde la carpeta RAW
        process_raw_data()

        logging.info("Transformación de datos completada exitosamente.")
    except Exception as e:
        logging.error(f"Error en la etapa de transformación: {e}")
