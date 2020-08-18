from airflow.api.common.experimental.pool import get_pool, create_pool
from airflow.exceptions import PoolNotFound
from airflow.models import BaseOperator
from airflow.utils import apply_defaults


class CreatePoolOperator(BaseOperator):
    ui_color = '#b8e9ee'

    @apply_defaults
    def __init__(
            self,
            name,
            slots,
            description='',
            *args, **kwargs):
        super(CreatePoolOperator, self).__init__(*args, **kwargs)
        self.description = description
        self.slots = slots
        self.name = name

    def execute(self, context):
        try:
            pool = get_pool(name=self.name)
            if pool:
                self.log(f'Pool exists: {pool}')
                return
        except PoolNotFound:
            pool = create_pool(name=self.name, slots=self.slots, description=self.description)
            self.log(f'Created pool: {pool}')
