from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'mlops_admin',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='iomt_e2e_mlops_pipeline',
    default_args=default_args,
    description='Automated pipeline for IoMT data ingestion and validation',
    schedule=timedelta( days = 1 ),# Runs daily
    start_date=datetime(2026, 3, 9),
    catchup=False,
    tags=['ingestion', 'validation', 'iomt', 'cyber_attacks'],
) as dag:

    # Define the absolute path to your project workspace
    PROJECT_PATH = '/home/murtuza/Desktop/Mlops_training/E2E_Projects/iomt_cyber_attacks'
    
    # Adjust this path if your venv is named something else (e.g., .venv or env)
    PYTHON_EXEC = f'{PROJECT_PATH}/venv/bin/python'

    # Task 1: Run the ingestion script
    ingest_data_task = BashOperator(
        task_id='ingest_landing_data',
        bash_command=f"""
        export PYTHONPATH={PROJECT_PATH} &&
        {PYTHON_EXEC} {PROJECT_PATH}/src/data_preprocessing/ingest.py""",
    )

    # Task 2: Run the validation script
    validate_data_task = BashOperator(
        task_id='validate_and_deduplicate_data',
        bash_command=f"""
        export PYTHONPATH={PROJECT_PATH} &&
        {PYTHON_EXEC} {PROJECT_PATH}/src/data_preprocessing/validate.py""",
    )

    # Define the execution sequence (Task dependencies)
    ingest_data_task >> validate_data_task