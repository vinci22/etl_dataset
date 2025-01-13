import os
import shutil
import pandas as pd
from datetime import datetime
from ingest_raw import get_today_subfolder, format_file, process_staging_to_raw

# Configuración de pruebas
TEST_BASE_DIR = "test_data"
TEST_STAGING_PATH = os.path.join(TEST_BASE_DIR, "staging")
TEST_RAW_PATH = os.path.join(TEST_BASE_DIR, "raw")

# Fixtures para configurar y limpiar el entorno de pruebas
import pytest

@pytest.fixture(scope="module")
def setup_test_environment():
    """
    Crea el entorno de prueba antes de que se ejecuten las pruebas.
    """
    os.makedirs(TEST_STAGING_PATH, exist_ok=True)
    os.makedirs(TEST_RAW_PATH, exist_ok=True)
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

def test_format_file(setup_test_environment):
    """
    Verifica que el archivo se formatee y guarde correctamente en RAW.
    """
    # Crear archivo de prueba en Staging
    test_file_path = os.path.join(TEST_STAGING_PATH, "test_file.csv")
    df = pd.DataFrame({
        "Trans Date Trans Time": ["2025-01-12 10:00:00", "2025-01-12 11:00:00"],
        "CC Num": [1234567890, 9876543210]
    })
    df.to_csv(test_file_path, index=False)

    # Llamar a la función de formato
    raw_folder = get_today_subfolder(TEST_RAW_PATH)
    format_file(test_file_path, raw_folder)

    # Verificar si el archivo formateado existe en RAW
    formatted_file_name = "test_file_formatted.csv"
    formatted_file_path = os.path.join(raw_folder, formatted_file_name)
    assert os.path.exists(formatted_file_path)

    # Verificar contenido del archivo formateado
    df_formatted = pd.read_csv(formatted_file_path)
    assert "trans_date_trans_time" in df_formatted.columns
    assert "cc_num" in df_formatted.columns

def test_process_staging_to_raw(setup_test_environment):
    """
    Verifica el procesamiento completo de Staging a Raw.
    """
    # Crear archivo de prueba en Staging
    test_file_path = os.path.join(TEST_STAGING_PATH, "test_file.csv")
    df = pd.DataFrame({
        "Trans Date Trans Time": ["2025-01-12 10:00:00", "2025-01-12 11:00:00"],
        "CC Num": [1234567890, 9876543210]
    })
    df.to_csv(test_file_path, index=False)

    # Llamar al proceso completo
    process_staging_to_raw()

    # Verificar que el archivo original fue eliminado de Staging
    assert not os.path.exists(test_file_path)

    # Verificar si el archivo formateado existe en RAW
    raw_folder = get_today_subfolder(TEST_RAW_PATH)
    formatted_file_name = "test_file_formatted.csv"
    formatted_file_path = os.path.join(raw_folder, formatted_file_name)
    assert os.path.exists(formatted_file_path)

    # Verificar contenido del archivo formateado
    df_formatted = pd.read_csv(formatted_file_path)
    assert "trans_date_trans_time" in df_formatted.columns
    assert "cc_num" in df_formatted.columns
