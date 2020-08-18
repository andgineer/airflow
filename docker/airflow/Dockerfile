FROM apache/airflow:1.10.10-python3.7

# do not use proxy for worker IP
RUN echo "export {NO_PROXY,no_proxy}=\$NO_PROXY,\$(getent hosts worker  | awk '{ print \$1 }')" >> ~/.bashrc

ENTRYPOINT ["/bin/bash"]
