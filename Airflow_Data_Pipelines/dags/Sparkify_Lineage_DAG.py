from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import ( CreateTableOperator, StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

#AWS_KEY = os.environ.get('AWS_KEY')
#AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval=None,    #'0 * * * *',
          max_active_runs = 1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_in_redshift = CreateTableOperator(
    task_id = 'create_tables_in_redshift',
    redshift_conn_id = 'redshift',
    dag = dag
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    table_name="staging_events",
    s3_bucket = "udacity-dend-warehouse",
    s3_key = "log-data",
    file_format="JSON",
    log_json_file = "log_json_path.json",
    redshift_conn_id = "redshift",
    aws_credential_id="aws_credentials",
    dag=dag,
    provide_context=True
)



stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    table_name="staging_songs",
    s3_bucket = "udacity-dend-warehouse",
    s3_key = "song_data",
    file_format="JSON",
    redshift_conn_id = "redshift",
    aws_credential_id="aws_credentials",
    dag=dag,
    provide_context=True
)


load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id = 'redshift',
    sql_query = SqlQueries.songplay_table_insert, 
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_query = SqlQueries.user_table_insert,
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_query = SqlQueries.song_table_insert,
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_query = SqlQueries.artist_table_insert,
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    sql_query = SqlQueries.time_table_insert,
)



run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id = "redshift",
    tables = ["artists", "songplays", "songs", "time", "users"]
    
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> create_tables_in_redshift
create_tables_in_redshift >> stage_songs_to_redshift
create_tables_in_redshift >> stage_events_to_redshift
stage_songs_to_redshift >> load_songplays_table
stage_events_to_redshift >> load_songplays_table

load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_time_dimension_table

load_artist_dimension_table >> run_quality_checks 
load_user_dimension_table >> run_quality_checks 
load_song_dimension_table >> run_quality_checks 
load_time_dimension_table >>  run_quality_checks

run_quality_checks >> end_operator

