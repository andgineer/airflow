from typing import Any

from airflow.utils.session import create_session
from airflow.models import BaseOperator, Pool


class CreatePoolOperator(BaseOperator):
    """Create a pool if it does not exist."""

    ui_color = "#b8e9ee"

    def __init__(
        self, *args: Any, name: str, slots: int, description: str = "", **kwargs: Any
    ) -> None:
        """Init."""
        super().__init__(*args, **kwargs)  # type: ignore[no-untyped-call]
        self.description = description
        self.slots = slots
        self.name = name

    def execute(self, context: Any) -> None:
        with create_session() as session:
            if pool := session.query(Pool).filter(Pool.pool == self.name).first():
                self.log.info("Pool exists: %s", pool)
            else:
                pool = Pool(
                    pool=self.name, slots=self.slots, description=self.description
                )
                session.add(pool)
                session.commit()
                self.log.info("Created pool: %s", pool)
