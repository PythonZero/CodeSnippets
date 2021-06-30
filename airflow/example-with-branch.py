from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

default_args = {
    "owner": "boss_man",
    "depends_on_past": False,
    "start_date": datetime(2021, 6, 26),
    "retries": 0,
    "image_pull_policy": "always",
    "namespace": "airflow",
    "startup_timeout_seconds": 7 * 60,
    "in_cluster": True,
    "get_logs": True,
    "is_delete_operator_pod": True,
    "retry_delay": timedelta(seconds=2),
    "provide_context": True,
    "tags": [
        f"owner:bob",
        f"test:true",
    ],
}


def print_1():
    print(1)


def print_2():
    print(2)


def task_that_might_fail(**kwargs):
    try_number = kwargs["task_instance"].try_number
    if try_number < 3:
        raise ValueError(f"try_number {try_number} less than 2")


dag = DAG(
    f"XXXXX_Example_DAG",
    schedule_interval="0 0 * * *",
    default_args=default_args,
    catchup=False,
)


all_op1s = []
all_op2s = []
all_branches = []

for repeat_num in range(3):
    task1_name = f"task1_run{repeat_num}"
    trigger_rule= "one_failed" if repeat_num != 0 else "all_success"
    op2_repeats = 3 if repeat_num == 1 else 1
    all_op1s.append(DummyOperator(task_id=task1_name, dag=dag, trigger_rule=trigger_rule))
    all_op2s.append(
        PythonOperator(
            dag=dag, task_id=f"task2_run{repeat_num}", python_callable=task_that_might_fail, retries=2
        )
    )
    all_branches.append(
        BranchPythonOperator(
            task_id=f"grouping_run{repeat_num}", dag=dag, python_callable=lambda **kwargs: task1_name
        )
    )

op3 = PythonOperator(
    dag=dag,
    task_id="task3",
    python_callable=print_1,
    retries=2,
)

end = PythonOperator(dag=dag, task_id="task4", python_callable=print_2, retries=2)

# See this stackoverflow question for why we need to follow this approach - https://stackoverflow.com/questions/68163296
# Creates branches
all_op1s[0] >> all_op2s[0] >> all_branches[0] >> op3 >> end  # the main branch
all_branches[0] >> all_op1s[1] >> all_op2s[1] >> all_branches[1] >> op3  # side branch with retry
all_branches[1] >> all_op1s[2] >> all_op2s[2] >> all_branches[2] >> op3  # side branch with retry
