FROM airflow-base

# do not use proxy for airflow-worker IP
RUN echo "export {NO_PROXY,no_proxy}=\$NO_PROXY,\$(getent hosts worker  | awk '{ print \$1 }')" >> ~/.bashrc

COPY alembic.ini /
COPY airflow.cfg ${AIRFLOW_HOME}/

COPY docker/airflow/start.sh /
CMD ["/start.sh"]

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt