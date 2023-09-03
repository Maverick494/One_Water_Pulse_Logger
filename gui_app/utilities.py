#!/usr/bin/python
"""
Created on Tue Aug  8 20:33:28 2023

@author: Justin
"""

import boto3
import ftplib
import json
import logging

from benedict import benedict as bdict
from botocore.client import Config
from datetime import datetime as dt
from guizero import (
    App,
    Box,
    error,
    info,
    Picture,
    PushButton,
    Text,
    TextBox,
    warn,
    Window,
    yesno,
)
from os.path import exists


class PopupHandler:
    def popup_create(event):
        popup_type = event["Type"]
        popup_title = event["Title"]
        popup_message = event["Message"]
        valid_types = ["info", "error", "warn", "yesno"]

        if popup_type in valid_types:
            if popup_type == "info":
                return info(popup_title, popup_message)
            elif popup_type == "warn":
                return warn(popup_title, popup_message)
            elif popup_type == "error":
                return error(popup_title, popup_message)
            elif popup_type == "yesno":
                return yesno(popup_title, popup_message)
        else:
            return info(popup_title, popup_message)


class LoggerSettings:
    settings_directory = "/home/ect-one-user/Desktop/One_Water_Pulse_Logger/config/"
    settings_filename = "_logger_config.json"
    settings_json = {}

    @staticmethod
    def update_settings(d):
        bdict(LoggerSettings.settings_json).merge(d, overwrite=True)
        print(LoggerSettings.settings_json)

    @classmethod
    def check_json(cls):
        keys_to_get = ["Site Name", "Sensor", "Data Output"]
        keys_exist = []

        while len(keys_exist) < len(keys_to_get):
            keys_exist.append(False)
        for i in range(len(keys_to_get)):
            if bdict.from_json(cls.settings_json).search(
                keys_to_get[i], in_keys=True, in_values=True
            ):
                keys_exist[i] = True

        return keys_exist

    @staticmethod
    def save_to_json():
        
        json_file = (
            LoggerSettings.settings_directory
            + LoggerSettings.settings_json["Site Name"]
            + LoggerSettings.settings_filename
        )

        try:
            # Use json to serialize the data and save to file
            with open(json_file, "w") as sf:
                sf.write(json.dumps(LoggerSettings.settings_json))

            sf.close()

            return {"Result": "Settings Saved to {}".format(json_file)}

        except Exception as ex:
            return {"Error": str(ex)}

    @staticmethod
    def retrieve_settings(site_name=None):

        json_file = LoggerSettings.settings_directory + site_name + LoggerSettings.settings_filename

        if exists(json_file):
            with open(json_file, "r") as json_data:
                LoggerSettings.settings_json = json.load(json_data)

            json_data.close()

            return {"File Exists" : True}, LoggerSettings.settings_json

        else:
            return {"File Exists" : False}, LoggerSettings.settings_json


class StorageHandler:
    def __init__(self):
        self.settings = LoggerSettings.retrieve_settings()

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
        conn = self.ftp_connection(
            self.settings["Data Output"]["Host"],
            self.settings["Data Output"]["Port"],
            self.settings["Data Output"]["Auth"]["Username"],
            self.settings["Data Output"]["Auth"]["Password"],
        )

        with open(data_file, "rb") as df:
            conn.storbinary("STOR", df)

        df.close()
        conn.close()
        return {"status": "success"}

    def set_creds(access_key, secret_key, role_arn=None, session_name="AssumedSession"):
        if role_arn is not None:
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
            sts_client = boto3.client(
                "sts",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="us-west-1",
            )

            # Assume the role
            assumed_role = sts_client.assume_role(
                RoleArn=role_arn, RoleSessionName=session_name
            )

            # Create a new session with the assumed role credentials
            assumed_credentials = assumed_role["Credentials"]
            session = boto3.Session(
                aws_access_key_id=assumed_credentials["AccessKeyId"],
                aws_secret_access_key=assumed_credentials["SecretAccessKey"],
                aws_session_token=assumed_credentials["SessionToken"],
            )

            return session

        else:
            s3 = boto3.client(
                "s3", aws_access_key_id=access_key, secret_access_key=secret_key
            )

            return s3

    def save_to_s3(self, data_file):
        settings = LoggerSettings.retrieve_settings()

        if self.settings["Data Output"]["Auth"]["Role"] is not None:
            aws_session = self.set_creds(
                settings["Data Output"]["Auth"]["Access Key"],
                settings["Data Output"]["Auth"]["Secret Key"],
                settings["Data Output"]["Auth"]["Role"],
            )

            s3 = aws_session.client(
                "s3", config=boto3.session.Config(signature_version="s3v4")
            )

        else:
            aws_session.upload_file(
                data_file,
                Bucket=settings["Data Output"]["Bucket"],
                Key=settings["Data Output"]["Prefix"]
                + "dt={}/".format(dt.strftime(dt.today(), "%y%m%d"))
                + data_file.split("/")[-1],
                config=Config(signature_version="s3v4"),
            )

        return {"status": "success"}

    def save_to_local(self, data_file):
        pass
