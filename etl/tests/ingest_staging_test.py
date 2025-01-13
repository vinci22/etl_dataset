import os
import pandas as pd
import pytest

from ingest_staging import validate_quality

# Rutas a los archivos de prueba
TEST_DATA_DIR = "tests/data/test_data"
VALID_FILE = os.path.join(TEST_DATA_DIR, "valid_data.csv")
NULL_FILE = os.path.join(TEST_DATA_DIR, "data_with_nulls.csv")
DUPLICATE_FILE = os.path.join(TEST_DATA_DIR, "data_with_duplicates.csv")

@pytest.fixture
def setup_test_files():
    """Crea archivos de prueba para los tests."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Archivo válido
    pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": [4, 5, 6]
    }).to_csv(VALID_FILE, index=False)

    # Archivo con valores nulos
    pd.DataFrame({
        "col1": [1, None, 3],
        "col2": [4, 5, None]
    }).to_csv(NULL_FILE, index=False)

    # Archivo con duplicados
    pd.DataFrame({
        "col1": [1, 2, 2],
        "col2": [4, 5, 5]
    }).to_csv(DUPLICATE_FILE, index=False)

    yield

    # Limpieza: Elimina los archivos de prueba después de ejecutar los tests
    for file in [VALID_FILE, NULL_FILE, DUPLICATE_FILE]:
        if os.path.exists(file):
            os.remove(file)
    os.rmdir(TEST_DATA_DIR)

def test_validate_quality_valid_data(setup_test_files):
    """Test: Archivo válido debe pasar las validaciones."""
    assert validate_quality(VALID_FILE) == True, "El archivo válido no pasó las validaciones."

def test_validate_quality_with_nulls(setup_test_files):
    """Test: Archivo con valores nulos debe fallar la validación."""
    assert validate_quality(NULL_FILE) == False, "El archivo con valores nulos pasó las validaciones."

def test_validate_quality_with_duplicates(setup_test_files):
    """Test: Archivo con duplicados debe fallar la validación."""
    assert validate_quality(DUPLICATE_FILE) == False, "El archivo con duplicados pasó las validaciones."
