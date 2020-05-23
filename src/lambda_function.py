#########################################################################################################
# Criador: Vinicius Aquino do Vale - Data: 18/05/2020
# Contém funções que ajudam na conversão para csv
# Cria o profiling de qualidade dos dados
# Traduz de English para Português
#########################################################################################################

import boto3
import start 
import urllib.parse as unquote_plus


s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket, key, download_path = download_file(event, context)
    upload_path = start.convert_type_to_csv(download_path)
    upload_file(bucket, key, upload_path)

def download_file(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        download_path = '/tmp/{}'.format(key.replace('/',''))
        s3_client.download_file(bucket, key, download_path)
        return bucket, key, download_path 


def upload_file(bucket, key, upload_path):
    s3_client.upload_file(upload_path, '{}-raw'.format(bucket), key)
