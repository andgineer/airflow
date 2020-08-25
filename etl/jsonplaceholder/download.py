"""
jsonplaceholder download
"""
import requests
from urllib.parse import urljoin
from datetime import timezone, datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from json import JSONDecodeError
from airflow.exceptions import AirflowSkipException
import logging

log = logging.getLogger()

engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()


class Posts(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    title = Column(String)
    body = Column(String)


def download(download_date: datetime):
    host = 'https://jsonplaceholder.typicode.com/'
    print(f'Downloading posts from {host} for {download_date}')

    post_id = 1
    url = f"{urljoin(host, 'posts')}/{post_id}"

    response = requests.get(
        url,
        # auth=config().proxy_cred,
        timeout=600,
        # proxies=config().proxies
    )
    try:
        return response.json()
    except JSONDecodeError:
        log.exception(f'Bad JSON:\n{response.text}')
        raise AirflowSkipException('Bad response')  # fail without retrying


if __name__ == '__main__':
    print(download(
        datetime.now(
            tz=timezone.utc
        ).replace(
            hour=0, minute=0, second=0, microsecond=0)
    ))
