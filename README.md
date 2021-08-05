# Loading GCS data to Bigquery using Cloud Functions
This is one of the part of **Intro to Cloud Functions** Repository. Here we will try to learn basics of Cloud Functions to create **Batch** jobs. Here We will learn step by step how to create a batch job using [German Credit Risk](https://www.kaggle.com/uciml/german-credit). The complete process is divided into 5 parts:

1. **Creating a Google Cloud Bucket**
2. **Creating a Google Cloud Bigquery Table**
3. **Creating a Google Cloud functions**
4. **Reading the data from GCS**
5. **Storing the Records in Bigquery**


## Motivation
For the last two years, I have been part of a great learning curve wherein I have upskilled myself to move into a Machine Learning and Cloud Computing. This project was practice project for all the learnings I have had. This is first of the many more to come. 
 

## Libraries/frameworks used

<b>Built with</b>
- [Anaconda](https://www.anaconda.com/)
- [Python](https://www.python.org/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Google Bigquery](https://cloud.google.com/bigquery)
- [Google Cloud Functions](https://cloud.google.com/functions)

## Cloning Repository

```bash
    # clone this repo:
    git clone https://github.com/adityasolanki205/Load-Cloud-Storage-data-into-Bigquery-using-Cloud-Functions.git
```

## Job Construction

Below are the steps to setup the enviroment and run the codes:

1. **Setup**: First we will have to setup free google cloud account which can be done [here](https://cloud.google.com/free). Then we need to Download the data from [German Credit Risk](https://www.kaggle.com/uciml/german-credit). We have included it in the data folder in the repository 

2. **Cloning the Repository to Cloud SDK**: We will have to copy the repository on Cloud SDK using below command:

```bash
    # clone this repo:
    git clone https://github.com/adityasolanki205/Load-Cloud-Storage-data-into-Bigquery-using-Cloud-Functions.git
```

4. **Creating a Google Cloud Bucket**: Here we will create a GCS bucket that will act as a Bigquery source. Name the Bucket as 'functions-testing-bq'


5. **Creating a Bigquery Dataset**: Here we will create a dataset and a table to act as destination. Create a dataset by the name 
'GermanCredit' and table with the name 'GermanCreditTable'. Use the schema below to create the table.

```python
    Schema:
        Existing_account:STRING
        Duration_month:INTEGER
        Credit_history:STRING
        Purpose:STRING
        Credit_amount:STRING
        Saving:STRING
        Employment_duration:STRING
        Installment_rate:INTEGER
        Personal_status:STRING
        Debtors:STRING
        Residential_Duration:INTEGER
        Property:STRING
        Age:INTEGER
        Installment_plans:STRING
        Housing:STRING
        Number_of_credits:INTEGER
        Job:STRING
        Liable_People:INTEGER
        Telephone:STRING
        Foreign_worker:STRING
        Classification:INTEGER
``` 

6. **Creating a Cloud Functions**: Now we will create a cloud functions. Follow the steps given in test section of this document.

7. **Read data from GCS and load into Bigquery**: Here we will read the data from GCS and load into Bigquery. Here we will read the data from Google cloud Bucket(present in the variable 'uri'). Then load data in Bigquery using client.load_table_from_uri. Here Write Desposition can be changed from 'WRITE_APPEND' to 'WRITE_TRUNCATE' depending on the requirement.  

```python
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
        uri = 'gs://functions-testing-bq/german_data.csv'

        # load the data into BQ
        load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(os.environ['TABLE']),
                job_config=job_config)

        load_job.result()  # wait for table load to complete.
        print('Job finished.')

```

The output will be in tht Bigquery dataset created. 


## Tests
To test the code we need to do the following:

    1. Copy the repository in Cloud SDK using below command:
        git clone https://github.com/adityasolanki205/Load-Cloud-Storage-data-into-Bigquery-using-Cloud-Functions.git
    
    2. Create a US Multiregional Storage Bucket by the name functions-testing-bq.
        
    3. Create a Biquery dataset with the name GermanCredit and a table named GermanCreditTable in US region. 
       This should be an empty table with schema as given below:
       
        Existing_account:STRING,
        Duration_month:INTEGER,
        Credit_history:STRING,
        Purpose:STRING,
        Credit_amount:STRING,
        Saving:STRING,
        Employment_duration:STRING,
        Installment_rate:INTEGER,
        Personal_status:STRING,
        Debtors:STRING,
        Residential_Duration:INTEGER,
        Property:STRING,
        Age:INTEGER,
        Installment_plans:STRING,
        Housing:STRING,
        Number_of_credits:INTEGER,
        Job:STRING,
        Liable_People:INTEGER,
        Telephone:STRING,
        Foreign_worker:STRING,
        Classification:INTEGER
    
    6. Create the Cloud functions as mentioned below: 
        a. Functions-name: CSV to Bigquery
        b. Regions: us-central1
        c. Trigger type: Cloud Storage
        d. Event Type: Finalize/Create
        e. Bucket: <Give your complete Bucket name>
        f. Runtime environment variables

            i. DATASET : GermanCredit
            ii. TABLE : GermanCreditTable

        g. Runtime: Python 3.7
        h. Source Code: Inline Editor
        i. main.py: Copy the code provided in the repository by the name main.py
        j. requirements.txt: Copy the code provided in the repository by the name requirements.txt
        k. Entry Point: load_csv_to_bq
     
    7. Click in Deploy Button
        
    8. Copy the data file in the cloud Bucket using the below command
        cd Load-Cloud-Storage-data-into-Bigquery-using-Cloud-Functions/data
        gsutil cp german_data.csv gs://functions-testing-bq/
        cd ..
    9. Now verify if the data is loaded in Bigquery


## Credits
1. Akash Nimare's [README.md](https://gist.github.com/akashnimare/7b065c12d9750578de8e705fb4771d2f#file-readme-md)
2. [Ternary Data](https://www.ternarydata.com/news/use-python-and-google-cloud-to-schedule-a-file-download-and-load-into-bigquery-3p3aw)
