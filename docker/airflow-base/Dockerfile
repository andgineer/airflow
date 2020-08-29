FROM andgineer/airflow-conda

COPY airflow.cfg ${AIRFLOW_HOME}/
COPY alembic.ini /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

CMD ["bash", "-c", "airflow info"]
