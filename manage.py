import os

def create_scaffold(base_dir):
    # Define the folder structure
    folders = [
        "data/raw",
        "data/processed",
        "data/outputs",
        "logs",
        "src/etl",
        "src/utils",
        "src/tests",
        "diagrams"
    ]

    # Create folders
    for folder in folders:
        os.makedirs(os.path.join(".", folder), exist_ok=True)
    
    # Create files with placeholders
    files = {
        "README.md": "# Proyecto de Ingeniería de Datos\n\nDescripción del proyecto.",
        "requirements.txt": "# Dependencias del proyecto\n\npandas\nnumpy\nsqlalchemy\nboto3\npytest",
        ".gitignore": "*.pyc\n__pycache__/\nlogs/\ndata/outputs/\n.env",
        "src/etl/extract.py": "# Código para la extracción de datos\ndef extract_data():\n    pass",
        "src/etl/transform.py": "# Código para la transformación de datos\ndef transform_data(data):\n    pass",
        "src/etl/load.py": "# Código para la carga de datos\ndef load_data(data):\n    pass",
        "src/etl/pipeline.py": (
            "# Script principal del pipeline ETL\n"
            "from extract import extract_data\n"
            "from transform import transform_data\n"
            "from load import load_data\n"
            "def run_pipeline():\n"
            "    raw_data = extract_data()\n"
            "    processed_data = transform_data(raw_data)\n"
            "    load_data(processed_data)\n"
            "if __name__ == '__main__':\n"
            "    run_pipeline()"
        ),
        "src/utils/logging_config.py": (
            "# Configuración de logs\n"
            "import logging\n"
            "def setup_logging():\n"
            "    logging.basicConfig(\n"
            "        filename='../logs/pipeline.log',\n"
            "        level=logging.INFO,\n"
            "        format='%(asctime)s - %(levelname)s - %(message)s'\n"
            "    )"
        ),
        "src/utils/exceptions.py": "# Definición de excepciones personalizadas\nclass PipelineError(Exception):\n    pass",
        "src/tests/test_extract.py": "# Pruebas para la extracción\ndef test_extract():\n    assert True",
        "src/tests/test_transform.py": "# Pruebas para la transformación\ndef test_transform():\n    assert True",
        "src/tests/test_load.py": "# Pruebas para la carga\ndef test_load():\n    assert True",
        "src/tests/test_pipeline.py": "# Pruebas para el pipeline completo\ndef test_pipeline():\n    assert True",
    }

    # Create files
    for file, content in files.items():
        with open(os.path.join(base_dir, file), "w") as f:
            f.write(content)

    print(f"Scaffold creado en: {os.path.abspath(base_dir)}")

# Ejecutar el script
if __name__ == "__main__":
    create_scaffold("my-data-engineering-project")
