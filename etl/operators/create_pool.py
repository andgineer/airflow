from typing import Any

from airflow.api.common.experimental.pool import create_pool, get_pool
from airflow.exceptions import PoolNotFound
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class CreatePoolOperator(BaseOperator):  # type: ignore
    """Create a pool if it does not exist."""

    ui_color = "#b8e9ee"

    @apply_defaults  # type: ignore
    def __init__(
        self, *args: Any, name: str, slots: int, description: str = "", **kwargs: Any
    ) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        self.description = description
        self.slots = slots
        self.name = name

    def execute(self, context: Any) -> None:  # pylint: disable=unused-argument
        """Execute."""
        assert self._log
        try:
            pool = get_pool(name=self.name)
            if pool:
                self._log.info(f"Pool exists: {pool}")
                return
        except PoolNotFound:
            pool = create_pool(name=self.name, slots=self.slots, description=self.description)
            self._log.info(f"Created pool: {pool}")
