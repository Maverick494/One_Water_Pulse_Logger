#!/usr/bin/python
"""
Created on Tue Aug  8 20:34:11 2023

@author: Justin
"""

import pigpio
import sys
import time
import json
import threading

from benedict import benedict as bdict
from datetime import datetime as dt
from datetime import timedelta as td
from tinydb import TinyDB, Query
from utilities import LoggerSettings, PopupHandler, StorageHandler


class DataLogger:

    def __init__(self):
        self.curr_day = dt.strftime(dt.today(), "%y-%m-%d")
        self.yesterday = dt.strftime(dt.today() - td(days=1), "%y-%m-%d")

        if dt.now().hour == 00 and dt.now().minute == 00:
            self.file_for_load = (
                "/home/ect-one-user/Desktop/Logger_Data/" + self.yesterday + "_data.csv"
            )
        elif dt.now().hour >= 00 and dt.now().hour <= 23 and dt.now().minute > 00:
            self.file_for_load = (
                "/home/ect-one-user/Desktop/Logger_Data/" + self.curr_day + "_data.csv"
            )

        self.settings = LoggerSettings.retrieve_settings()
        self.GPIO_LIST = [22, 23, 24, 25]
        self.logger_run = False
        self.curr_hour = 0
        self.write_min_hr = 3
        self.write_min_day = 58
        self.hour_total = 0.0
        self.day_total = 0.0
        self.hour_save = 0.0
        self.day_save = 0.0
        self.log_data = {
            "site_name": self.settings["Site Name"],
            "sensor": self.settings["Sensor"]["Name"],
            "log_timestamp": dt.now(),
        }
        self.pi = pigpio.pi()  # Initialize pigpio module
        self.pi.set_mode(self.GPIO_LIST[0], pigpio.INPUT)
        self.cb = self.pi.callback(self.GPIO_LIST[0], pigpio.RISING_EDGE)
        self.lock = threading.Lock()  # Add a lock for thread synchronization

    def logging(self):
        while self.logger_run:
            flow = self.cb.count / self.settings["K Factor"]
            self.hour_total += flow
            self.day_total += self.hour_total

    def save_logging(self):
        if self.settings["Data Output"]["Location"] == "local":
            data_save = self.write_log_to_db
        else:
            data_save = self.write_log_to_file

        if self.curr_hour == dt.now().hour and dt.now().minute == self.write_min_hr:
            if self.standard_unit == self.desired_units and self.standard_unit == "gpm":
                self.hour_save = self.hour_total
                self.day_save = self.day_total
            elif self.standard_unit != self.desired_units and self.standard_unit == "lpm":
                self.hour_save = self.hour_total * 0.2642
                self.day_save = self.day_total * 0.2642

            logs_to_save = self.update_logdata(
                {"hourly_flow": self.hour_save, "daily_flow": self.day_save}
            )
            data_save(logs_to_save)
            self.hour_count = 0

        elif self.curr_hour == 23 and dt.now().minute == self.write_min_day:
            logs_to_save = self.update_logdata(
                {"hourly_flow": self.hour_save, "daily_flow": self.day_save}
            )
            data_save(logs_to_save)
            self.data_export()
            self.hour_count = 0
            self.day_count = 0

    def update_logdata(self, d):
        bdict(self.log_data).merge(d, overwrite=True)

    @staticmethod
    def start_logging():
        dl = DataLogger()
        dl.logger_run = True
        dl.curr_hour = dt.now().hour
        dl.pi.start()

    @staticmethod
    def stop_logging():
        dl = DataLogger()
        dl.logger_run = False
        dl.pi.stop()

    @staticmethod
    def data_export():
        where_to = DataLogger.settings["Data Output"]["Location"]

        if where_to in ["s3", "ftp"]:
            if where_to == "s3":
                StorageHandler.upload_to_s3(DataLogger.file_for_load)
            else:
                StorageHandler.upload_to_ftp(DataLogger.file_for_load)

    @staticmethod
    def write_log_to_file(self, dict_to_write):
        with open(self.file_for_load, "a") as lf:
            lf.write("{}\t{}\t{}\t{}\t{}\n").format(dict_to_write)

        lf.close()

    @staticmethod
    def write_log_to_db(dict_to_write):
        Query.insert(dict_to_write)
