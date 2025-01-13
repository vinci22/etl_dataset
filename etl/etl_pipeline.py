import logging
from etl.ingest_staging import extract_to_staging
from etl.ingest_raw import process_staging_to_raw
from etl.ingest_processed import process_raw_data

# Configuración de logging
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def run_pipeline():
    """
    Ejecuta secuencialmente las etapas del pipeline ETL.
    """
    try:
        logging.info("Iniciando el pipeline ETL.")

        # Etapa 1: Ingestión a Staging
        logging.info("Ejecutando la etapa de extracción a Staging.")
        extract_to_staging()
        logging.info("Etapa de extracción a Staging completada exitosamente.")

        # Etapa 2: Transformación y movimiento a Raw
        logging.info("Ejecutando la etapa de transformación a Raw.")
        process_staging_to_raw()
        logging.info("Etapa de transformación a Raw completada exitosamente.")

        # Etapa 3: Procesamiento y movimiento a Processed
        logging.info("Ejecutando la etapa de procesamiento a Processed.")
        process_raw_data()
        logging.info("Etapa de procesamiento a Processed completada exitosamente.")

        logging.info("Pipeline ETL completado exitosamente.")
    except Exception as e:
        logging.error(f"Error durante la ejecución del pipeline ETL: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()
