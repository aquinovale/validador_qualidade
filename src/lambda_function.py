#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam na conversão para csv
# Cria o profiling de qualidade dos dados
# Traduz de English para Português
#########################################################################################################

import os'
import boto3
import start 
import urllib.parse as unquote_plus


s3_client = boto3.client('s3')

landing_bucket = 'landing'

def lambda_handler(event, context):
    location = '/tmp/validador/'
    bucket, key, download_path = download_file(event, context, location)
    start.convert_type_to_csv(download_path)
    upload_file(landing_bucket, key, location)

def download_file(event, context, location):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        os.makedirs(location, exist_ok=True)
        download_path = location + key.replace('/','')
        s3_client.download_file(bucket, key, download_path)
        return bucket, key, download_path 


def upload_file(bucket, key, upload_path):
    for r, _, files in os.walk(upload_path, topdown=False):
        for f in files:
            if ('.csv' in f or '.schema' in f or '_warns' in f):
                s3_client.upload_file(os.path.join(upload_path, f), bucket, f)
