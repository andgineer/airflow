from airflow.models import DagBag


def test_dags_load_with_no_errors(dag_files):
    dag_bag = DagBag(include_examples=False)
    for file_name in dag_files:
        print(f'Loading DAG {file_name}')
        dags = dag_bag.process_file(file_name)
        assert len(dags) > 0
        assert len(dag_bag.import_errors) == 0
