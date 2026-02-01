from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_science_team',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'tensorflow_model_training',
    default_args=default_args,
    description='A simple DAG to train a TensorFlow model',
    schedule=timedelta(days=1),
    catchup=False
)

train_task = BashOperator(
    task_id='train_tensorflow_model',
    bash_command='python3 src/train.py',
    dag=dag,
)

train_task
if __name__ == "__main__":
    print("DAG loaded successfully")
