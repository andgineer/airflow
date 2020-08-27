FROM airflow-base

COPY airflow.cfg ${AIRFLOW_HOME}/

COPY docker/airflow-worker/start.sh /
CMD ["/start.sh"]

COPY requirements.txt /
RUN pip install --user -r /requirements.txt

