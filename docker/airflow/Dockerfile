FROM airflow-base

# do not use proxy for airflow-worker IP
RUN echo "export {NO_PROXY,no_proxy}=\$NO_PROXY,\$(getent hosts worker  | awk '{ print \$1 }')" >> ~/.bashrc

COPY start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]
