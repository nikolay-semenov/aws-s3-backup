import os
import json
import boto3
import shutil
import configparser
from datetime import datetime
from botocore import exceptions


def config_get():
    config_parse = configparser.ConfigParser()
    config_parse.read('config.ini')
    return config_parse


def client_create():
    session = boto3.session.Session()
    client = session.client(
        service_name=config_get()["aws"]['service_name'],
        aws_access_key_id=config_get()["aws"]["access_key"],
        aws_secret_access_key=config_get()["aws"]["secret_key"],
        region_name=config_get()["aws"]["region_name"]
    )
    return client


def client_upload_data(path, bucket):
    config = config_get()
    date_time_now = datetime.now()
    timestamp = date_time_now.strftime("%d-%b-%y")
    shutil.copy(config["data"]["dump_path"],
                config["data"]["dump_source"] +
                config["data"]["dump_name"] +
                '-' +
                timestamp)
    for root, dirs, files in os.walk(path):
        for file in files:
            client_create().upload_file(os.path.join(root, file),
                                        bucket,
                                        file)
            os.remove(os.path.join(config["data"]["dump_source"],
                                   file))


def client_get_bucket(bucket):
    client = client_create()
    config = config_get()
    with open(config["data"]["file_name"], 'w') as result:
        data = client.list_buckets()
        json.dump(data, result, indent=4, sort_keys=True, default=str)
        for keys in data['Buckets']:
            if keys['Name'] == bucket:
                return keys


def main():
    client = client_create()
    config = config_get()
    key_list = client_get_bucket(bucket=config["aws"]["bucket_name"])
    try:
        if config["aws"]["bucket_name"] in key_list['Name']:
            client_upload_data(path=config["data"]["dump_source"],
                               bucket=config["aws"]["bucket_name"])
    except (TypeError, AttributeError, exceptions.ClientError):
        client.create_bucket(Bucket=config["aws"]["bucket_name"],
                             CreateBucketConfiguration={'LocationConstraint': config["aws"]["region_name"]})


main()
