from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class CreateTableOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, redshift_conn_id = "", *args, **kwargs):
        
        super(CreateTableOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        
    def execute(self, context):
        self.log.info('Creating Postgres SQL Hook')
        redshift = PostgresHook(postgres_conn_id = self.redshift_conn_id)

        self.log.info('Executing creating tables in Redshift.')
        queries =  open('/home/workspace/airflow/create_tables.sql', 'r').read()
        redshift.run(queries)
        
        self.log.info("Tables created ")
        





