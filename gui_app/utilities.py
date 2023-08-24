#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:33:28 2023

@author: Justin
"""

import boto3
import ftplib
import json

from base64 import b64decode as bd
from datetime import datetime as dt


class Settings:
    
    def __init__(self, **kwargs):
        print(kwargs.site_name, kwargs.data_output_choice, kwargs.sensor_name)
      
        if kwargs.email_address is not None:
            self.email_address = kwargs.email_address
        else:
            self.email_address = 'ryan@epiccleantec.com'
        
        self.json_data = {}
                    
    def update_settings(**kwargs):

        # Create a dictionary to represent the JSON structure
        json_data = {
            'Settings': {
                'Site Name': kwargs.site_name,
                'Sensor': {
                    'Name': kwargs.sensor_name,
                    'K Factor': kwargs.k_factor,
                    'Standard Unit': kwargs.standard_unit,
                    'Desired Unit': kwargs.desired_unit
                },
                'Data Output': {
                    'Location': kwargs.data_output_choice.lower()
                }
            }
        }
        
        # Add data based on data_output_choice
        if kwargs.data_output_choice.lower() == 's3':
            json_data['Settings']['Location']['s3_bucket'] = kwargs.s3_bucket
            json_data['Settings']['Location']['s3_key'] = kwargs.s3_key
            json_data['Settings']['Location']['auth'] = {
                'Access Key': kwargs.access_key,
                'Secret Key': kwargs.secret_key
            }
            if kwargs.role_arn is not None:
                json_data['settings']['data_output']['auth']['role'] = kwargs.role_arn
        elif kwargs.data_output_choice.lower() == 'ftp':
            json_data['Settings']['Location']['host'] = kwargs.host
            json_data['Settings']['Location']['port'] = kwargs.port
            json_data['Settings']['Location']['directory'] = kwargs.directory
            json_data['Settings']['Location']['auth'] = {
                'Username': kwargs.username,
                'Password': kwargs.password
            }

        return json_data

    def save_to_json(self):

        json_to_write = self.json_data

        # Serialize the JSON data to a file
        with open(self.settings_directory + self.settings_filename, 'w') as sf:
            json.dump(json_to_write, sf, indent=4)  # Use json.dump() to serialize the data

        sf.close()
        return {'Settings' : 'Saved to file'}

    def retrieve_settings(cls):

        try:
            with open(cls.settings_directory+cls.settings_filename, 'r') as json:
                settings = json.load(json)
            
            json.close()
            
            return settings

        except (FileNotFoundError, IsADirectoryError) as e:
            return None


class StorageHandler:
    def __init__(self):
        self.settings = Settings.retrieve_settings()

    def ftp_connection(HOST, PORT, USER, PASS):

        try:
            ftp = ftplib.FTP(source_address=())
            ftp.connect(HOST, PORT)
            ftp.login(USER, PASS)
            ftp.set_pasv(False)
            ftp.set_debuglevel(3)

        except ftplib.all_errors as ex:
            print(str(ex))
            raise
         
        return ftp      
    
    def save_to_ftp(self, data_file):
        conn = self.ftp_connection(self.settings['output']['host'],
                              self.settings['output']['port'],
                              self.settings['output']['auth']['username'],
                              self.settings['output']['auth']['password'])
        
        with open(data_file, 'rb') as df :                      
            conn.storbinary('STOR', df)
        
        df.close()
        conn.close()
        pass
        
    def set_creds(access_key, secret_key, role_arn = None,
                                  session_name='AssumedSession'):
        
        if role_arn is not None :
            """
            Assumes an IAM role using IAM User's access and secret keys.

            Parameters:
                access_key (str): IAM User's access key.
                secret_key (str): IAM User's secret key.
                role_arn (str): ARN of the IAM role you want to assume.
                session_name (str): Name of the assumed role session (optional).

            Returns:
                boto3.Session: A session with the assumed role credentials.
            """
            sts_client = boto3.client('sts',
                                      aws_access_key_id=bd(access_key).decode('utf-8'),
                                      aws_secret_access_key=bd(secret_key).decode('utf-8'),
                                      region_name='us-west-1')

            # Assume the role
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name
            )

            # Create a new session with the assumed role credentials
            assumed_credentials = assumed_role['Credentials']
            session = boto3.Session(
                aws_access_key_id=assumed_credentials['AccessKeyId'],
                aws_secret_access_key=assumed_credentials['SecretAccessKey'],
                aws_session_token=assumed_credentials['SessionToken']
            )
            
            return session
            
        else :
            s3 = boto3.client('s3', aws_access_key_id=bd(access_key).decode('utf-8'),
            secret_access_key=bd(secret_key).decode('utf-8'))
                                  
            return s3
        

    def save_to_s3(self, data_file):
        settings = Settings.retrieve_settings()
        if self.settings['output']['auth']['role'] is not None :
            aws_session = self.set_creds(settings['output']['auth']['access_key'],
                                    settings['output']['auth']['access_key'],
                                    settings['output']['auth']['role'])
                                    
            s3 = aws_session.client('s3', config = boto3.session
                                    .Config(signature_version='s3v4'))
                                    
        else :
           aws_session.upload_file(data_file,
                                   Bucket = settings['output']['s3_bucket'],
                                   Key = settings['output']['s3_prefix']
                                   + 'dt={}/'.format(dt.strftime(dt.today(),
                                                    '%y%m%d'))
                                   + data_file.split('/')[-1],
                                   config = Config(signature_version='s3v4'))
                                   
    def save_to_local(self, data_file):
        pass
