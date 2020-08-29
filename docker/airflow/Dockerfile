FROM andgineer/airflow-conda

COPY airflow.cfg ${AIRFLOW_HOME}/
COPY alembic.ini /

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# do not use proxy for airflow-worker IP
RUN echo "export {NO_PROXY,no_proxy}=\$NO_PROXY,\$(getent hosts worker  | awk '{ print \$1 }')" >> ~/.bashrc

COPY start.sh /
CMD /start.sh
