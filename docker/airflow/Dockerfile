FROM andgineer/airflow-conda

# we mount this as volume for live reload on changes for debugging
VOLUME /root/airflow/dags

# Flower
EXPOSE 5555

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# do not use proxy for airflow-worker IP
RUN echo "export {NO_PROXY,no_proxy}=\$NO_PROXY,\$(getent hosts worker  | awk '{ print \$1 }')" >> ~/.bashrc

COPY airflow.cfg ${AIRFLOW_HOME}/
COPY alembic.ini /
COPY start.sh /
COPY wait-for-postgres.sh /
CMD /start.sh
