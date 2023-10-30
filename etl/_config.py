import os
from typing import Dict, Optional


class EnvVar:
    """Environment variables."""

    proxy_login = "PROXY_LOGIN"
    proxy_password = "PROXY_PASSWORD"
    xchng_folder = "WORKERS_XCHNG_FOLDER"


class Config:
    """Configuration."""

    proxy_login = os.getenv(EnvVar.proxy_login)
    proxy_password = os.getenv(EnvVar.proxy_password)
    xchng_folder = os.getenv(EnvVar.xchng_folder)  # we need it on workers only so it's ok if
    # this is empty for Airflow scheduler

    proxies: Optional[Dict[str, str]] = (
        {"HTTPS_PROXY": os.environ["HTTPS_PROXY"]}
        if os.getenv("HTTPS_PROXY") is not None
        else None
    )

    proxy_cred = (proxy_login, proxy_password)


_config: Optional[Config] = None


def config() -> Config:
    """Get config."""
    global _config  # pylint: disable=global-statement
    if _config is None:
        _config = Config()
    return _config
