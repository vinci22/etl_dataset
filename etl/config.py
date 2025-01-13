import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

# Rutas de subcarpetas
STAGING_DATA_PATH = os.path.join(DATA_DIR, "staging")  # Sin barra inclinada al comienzo
PRERAW_DATA_PATH = os.path.join(DATA_DIR, "preraw")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed")


# Configuración de Kaggle
KAGGLE_DATASET = "priyamchoksi/credit-card-transactions-dataset"  # Cambiar según el dataset que uses
