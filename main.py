import os

from google.cloud import bigquery

def load_csv_to_bq(data, context):
        client = bigquery.Client()
        
        dataset_ref = client.dataset(os.environ['DATASET'])
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = 'WRITE_APPEND'
        job_config.schema = [
                    bigquery.SchemaField('Existing_account', 'STRING'),
                    bigquery.SchemaField('Duration_month', 'INTEGER'),
                    bigquery.SchemaField('Credit_history', 'STRING'),
                    bigquery.SchemaField('Purpose', 'STRING'),
                    bigquery.SchemaField('Credit_amount', 'STRING'),
                    bigquery.SchemaField('Saving', 'STRING'),
                    bigquery.SchemaField('Employment_duration', 'STRING'),
                    bigquery.SchemaField('Installment_rate', 'INTEGER'),
                    bigquery.SchemaField('Personal_status', 'STRING'),
                    bigquery.SchemaField('Debtors', 'STRING'),
                    bigquery.SchemaField('Residential_Duration', 'INTEGER'),
                    bigquery.SchemaField('Property', 'STRING'),
                    bigquery.SchemaField('Age', 'INTEGER'),
                    bigquery.SchemaField('Installment_plans', 'STRING'),
                    bigquery.SchemaField('Housing', 'STRING'),
                    bigquery.SchemaField('Number_of_credits', 'INTEGER'),
                    bigquery.SchemaField('Job', 'STRING'),
                    bigquery.SchemaField('Liable_People', 'INTEGER'),
                    bigquery.SchemaField('Telephone', 'STRING'),
                    bigquery.SchemaField('Foreign_worker', 'STRING'),
                    bigquery.SchemaField('Classification', 'INTEGER'),
                ]
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV

        # get the URI for uploaded CSV in GCS from 'data'
        uri = 'gs://' + os.environ['BUCKET'] + '/' + os.environ['FILE']

        # load the data into BQ
        load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(os.environ['TABLE']),
                job_config=job_config)

        load_job.result()  # wait for table load to complete.
        print('Job finished.')

