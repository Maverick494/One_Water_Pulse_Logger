#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:33:28 2023

@author: Justin
"""

from botocore.client import Config
import boto3
import ftplib
import json

from base64 import b64decode as bd
from datetime import datetime as dt


class Settings:
    settings_directory = '/home/ect-one-user/Desktop/One_Water_Pulse_Logger/config/'
    json_data = {}
    settings_filename = ''

    @staticmethod    
    def update_settings(kwargs):

        settings_filename = '{}_settings.json'.format(kwargs['Site Name'])

        # Create a dictionary to represent the JSON structure
        json_data = {
            'Settings': {
                'Site Name': kwargs['Site Name'],
                'Sensor': {
                    'Name': kwargs['Name'],
                    'K Factor': kwargs['K Factor'],
                    'Standard Unit': kwargs['standard_unit'],
                    'Desired Unit': kwargs['Desired Unit'],
                },
                'Data Output': {
                    'Location': kwargs['Location'].lower()
                }
            }
        }
        
        # Add data based on data_output_choice
        if kwargs.data_output_choice.lower() == 's3':
            json_data['Settings']['Location']['Bucket'] = kwargs['Bucket']
            json_data['Settings']['Location']['Prefix'] = kwargs['Prefix']
            json_data['Settings']['Location']['Key'] = kwargs['Key']
            json_data['Settings']['Location']['Auth'] = {
                'Access Key': kwargs['Access Key'],
                'Secret Key': kwargs['Secret Key']
            }
            if kwargs.role_arn is not None:
                json_data['Settings']['Data Output']['Auth']['Role'] = kwargs['Role']

        elif kwargs.data_output_choice.lower() == 'ftp':
            json_data['Settings']['Location']['Host'] = kwargs['Host']
            json_data['Settings']['Location']['Port'] = kwargs['Port']
            json_data['Settings']['Location']['Directory'] = kwargs['Directory']
            json_data['Settings']['Location']['Auth'] = {
                'Username': kwargs['Username'],
                'Password': kwargs['Password']
            }

        elif kwargs.data_output_choice.lower() == 'local':

            if kwargs.email_address is not None:
                json_data['Settings']['Email Address'] = kwargs['Email Address']
            else:
                json_data['Settings']['Email Address'] = 'ryan@epiccleantec.com'

        return json_data, settings_filename

    @staticmethod
    def save_to_json():

        json_to_write = json_data

        # Serialize the JSON data to a file
        with open(settings_directory + settings_filename, 'w') as sf:
            json.dump(json_to_write, sf, indent=4)  # Use json.dump() to serialize the data

        sf.close()
        return {'Settings' : 'Saved to file'}

    @classmethod
    def retrieve_settings(cls):
        settings = None
        try:
            with open(cls.settings_directory + cls.settings_filename, 'r') as json:
                settings = json.load(json)
            
            json.close()
        
            return settings
        except (IsADirectoryError, FileNotFoundError):
            return settings

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
