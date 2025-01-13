import os
import shutil
import pandas as pd
import pytest
from datetime import datetime
from main import get_today_subfolder, transform_data, process_raw_data

# Configuración de pruebas
TEST_BASE_DIR = "test_data"
TEST_RAW_PATH = os.path.join(TEST_BASE_DIR, "raw")
TEST_PROCESSED_PATH = os.path.join(TEST_BASE_DIR, "processed")

@pytest.fixture(scope="module")
def setup_test_environment():
    """
    Configura el entorno de prueba antes de ejecutar las pruebas.
    """
    os.makedirs(TEST_RAW_PATH, exist_ok=True)
    os.makedirs(TEST_PROCESSED_PATH, exist_ok=True)
    yield
    shutil.rmtree(TEST_BASE_DIR)

def test_get_today_subfolder(setup_test_environment):
    """
    Verifica que la carpeta particionada por fecha se cree correctamente.
    """
    today_folder = get_today_subfolder(TEST_RAW_PATH)
    today = datetime.now()
    expected_path = os.path.join(
        TEST_RAW_PATH, f"{today.year}", f"{today.month:02d}", f"{today.day:02d}"
    )
    assert os.path.exists(expected_path)
    assert today_folder == expected_path

def test_transform_data():
    """
    Verifica que los datos RAW se transformen correctamente.
    """
    # Crear un DataFrame simulado
    raw_data = {
        "trans_date_trans_time": ["2025-01-12 10:00:00", "2025-01-12 11:00:00"],
        "cc_num": [1234567890, 9876543210],
        "merchant": ["fraud_store1", "fraud_store2"],
        "is_fraud": [1, 0],
        "category": ["electronics", "fashion"],
        "gender": ["M", "F"],
        "merch_zipcode": [None, 90210]
    }
    df_raw = pd.DataFrame(raw_data)

    # Transformar los datos
    df_transformed = transform_data(df_raw)

    # Verificar transformaciones específicas
    assert "transaction_hour" in df_transformed.columns
    assert "transaction_day" in df_transformed.columns
    assert "transaction_month" in df_transformed.columns
    assert "transaction_year" in df_transformed.columns
    assert "category_encoded" in df_transformed.columns
    assert "gender_encoded" in df_transformed.columns
    assert "cc_num" not in df_transformed.columns  # Esta columna debería ser eliminada
    assert "is_fraud" not in df_transformed.columns

def test_process_raw_data(setup_test_environment):
    """
    Verifica el proceso completo de transformación de datos desde RAW a PROCESSED.
    """
    # Crear archivo simulado en RAW
    today_folder = get_today_subfolder(TEST_RAW_PATH)
    test_file_path = os.path.join(today_folder, "test_raw.csv")
    df = pd.DataFrame({
        "trans_date_trans_time": ["2025-01-12 10:00:00", "2025-01-12 11:00:00"],
        "cc_num": [1234567890, 9876543210],
        "merchant": ["fraud_store1", "fraud_store2"],
        "is_fraud": [1, 0],
        "category": ["electronics", "fashion"],
        "gender": ["M", "F"],
        "merch_zipcode": [None, 90210]
    })
    df.to_csv(test_file_path, index=False)

    # Ejecutar el procesamiento
    process_raw_data()

    # Verificar que el archivo procesado exista en PROCESSED
    processed_folder = get_today_subfolder(TEST_PROCESSED_PATH)
    processed_file_path = os.path.join(processed_folder, "test_raw.parquet")
    assert os.path.exists(processed_file_path)

    # Verificar contenido del archivo procesado
    df_processed = pd.read_parquet(processed_file_path)
    assert "transaction_hour" in df_processed.columns
    assert "transaction_day" in df_processed.columns
    assert "transaction_month" in df_processed.columns
    assert "transaction_year" in df_processed.columns
    assert "category_encoded" in df_processed.columns
    assert "gender_encoded" in df_processed.columns
    assert "cc_num" not in df_processed.columns  # Esta columna debería ser eliminada
    assert "is_fraud" not in df_processed.columns
