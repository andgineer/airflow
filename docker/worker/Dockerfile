FROM apache/airflow:1.10.10-python3.7

# set build-time proxy settings from docker-compose.yaml#args
ARG no_proxy
ARG http_proxy
ARG https_proxy

# copy build-time proxy-settings into run-time ones
ENV NO_PROXY=$no_proxy
ENV HTTP_PROXY=$http_proxy
ENV HTTPS_PROXY=$https_proxy

COPY requirements.txt /
RUN pip install --user -r /requirements.txt

COPY docker/airflow/airflow.cfg /opt/airflow/

ENTRYPOINT ["/bin/bash"]
