from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from pipelines.steps import ingestion, clean, silver, gold
from db.init.schema import get_db, ensure_db_schema

def run_init_schema():
  with get_db() as conn:
    ensure_db_schema(conn)

def run_injestion():
    with get_db() as conn:
        ingestion.run(conn)

def run_clean():
    with get_db() as conn:
        clean.run(conn)

def run_silver():
    with get_db() as conn:
        silver.run(conn)

def run_gold():
    with get_db() as conn:
        gold.run(conn)

with DAG(
    dag_id='etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    t0 = PythonOperator(task_id="init_schema", python_callable=run_init_schema)
    t1 = PythonOperator(task_id="ingestion", python_callable=run_injestion)
    t2 = PythonOperator(task_id="clean", python_callable=run_clean)
    t3 = PythonOperator(task_id="silver", python_callable=run_silver)
    t4 = PythonOperator(task_id="gold", python_callable=run_gold)

    t0 >> t1 >> t2 >> t3 >> t4