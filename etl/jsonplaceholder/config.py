import os
from typing import Optional


class EnvVar:
    proxy_login = 'PROXY_LOGIN'
    proxy_password = 'PROXY_PASSWORD'
    xchng_folder = 'WORKERS_XCHNG_FOLDER'


class Config:
    proxy_login = os.environ[EnvVar.proxy_login]
    proxy_password = os.environ[EnvVar.proxy_password]
    xchng_folder = os.getenv(EnvVar.xchng_folder)  # we need it on workers only so it's ok if
    # this is empty for Airflow scheduler

    proxies: dict = {
        'HTTPS_PROXY': os.environ['HTTPS_PROXY']
    } if os.getenv('HTTPS_PROXY') is not None else None

    proxy_cred = (proxy_login, proxy_password)


_config: Optional[Config] = None


def config():
    global _config
    if _config is None:
        _config = Config()
    return _config
