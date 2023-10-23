from airflow.models import DagBag


def test_dags_load_with_no_errors(dag_bag, dag_files):
    """DAG/Pipeline Definition Test."""
    assert dag_bag.size() == len(dag_files)
    assert len(dag_bag.import_errors) == 0
