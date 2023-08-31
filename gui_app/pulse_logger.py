#!/usr/bin/python
# -*- coding: utf-8 -*-
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
    curr_day = dt.strftime(dt.today(), "%y-%m-%d")
    yesterday = dt.strftime(dt.today() - td(days=1), "%y-%m-%d")

    if dt.now().hour == 00 and dt.now().minute == 00:
        file_for_load = (
            "/home/ect-one-user/Desktop/Logger_Data/" + yesterday + "_data.csv"
        )
    elif dt.now().hour >= 00 and dt.now().hour <= 23 and dt.now().minute > 00:
        file_for_load = (
            "/home/ect-one-user/Desktop/Logger_Data/" + curr_day + "_data.csv"
        )

    settings = LoggerSettings.retrieve_settings()
    GPIO_LIST = [22, 23, 24, 25]
    pulse_per_unit = settings["K Factor"]
    standard_unit = settings["Standard Unit"]
    desired_units = settings["Desired Unit"]
    logger_run = False
    curr_hour = 0
    write_min_hr = 3
    write_min_day = 58
    hour_total = 0.0
    day_total = 0.0
    hour_save = 0.0
    day_save = 0.0
    log_data = {
        "site_name": settings["Site Name"],
        "sensor": settings["Sensor"]["Name"],
        "log_timestamp": dt.now(),
    }
    pi = pigpio.pi()  # Initialize pigpio module
    pi.set_mode(GPIO_LIST[0], pigpio.INPUT)
    cb = pi.callback(GPIO_LIST[0], pigpio.RISING_EDGE)
    lock = threading.Lock()  # Add a lock for thread synchronization

    @classmethod
    def logging(cls):
        while cls.logger_run:
            flow = cls.cb.count / cls.pulse_per_unit
            cls.hour_total += flow
            cls.day_total += cls.hour_total

    @classmethod
    def save_logging(cls):
        if cls.settings["Data Output"]["Location"] == "local":
            data_save = DataLogger.write_log_to_db()
        else:
            data_save = DataLogger.write_log_to_file()

        if cls.curr_hour == dt.now().hour and dt.now().minute == cls.write_min_hr:
            if cls.standard_unit == cls.desired_units and cls.standard_unit == "gpm":
                cls.hour_save = cls.hour_total
                cls.day_save = cls.day_total
            elif cls.standard_unit != cls.desired_units and cls.standard_unit == "lpm":
                cls.hour_save = cls.hour_total * 0.2642
                cls.day_save = cls.day_total * 0.2642

            logs_to_save = DataLogger.update_logdata(
                {"hourly_flow": cls.hour_save, "daily_flow": cls.day_save}
            )
            data_save(logs_to_save)
            cls.hour_count = 0

        elif cls.curr_hour == 23 and dt.now().minute == cls.write_min_day:
            logs_to_save = DataLogger.update_logdata(
                {"hourly_flow": cls.hour_save, "daily_flow": cls.day_save}
            )
            data_save(logs_to_save)
            cls.data_export()
            cls.hour_count = 0
            cls.day_count = 0

    @staticmethod
    def update_logdata(d):
        bdict(DataLogger.log_data).merge(d, overwrite=True)

    def start_logging(cls):
        cls.logger_run = True
        cls.curr_hour = dt.now().hour
        cls.pi.start()

    def stop_logging(cls):
        cls.logger_run = False
        cls.pi.stop()

    def data_export():
        where_to = LoggerSettings.settings_json["Data Output"]["Location"]

        if where_to in ["s3", "ftp"]:
            if where_to == "s3":
                StorageHandler.upload_to_s3(DataLogger.file_for_load)
            else:
                StorageHandler.upload_to_ftp(DataLogger.file_for_load)

    @staticmethod
    def write_log_to_file(file_for_load, log_data):
        with open(DataLogger.log_file, "a") as lf:
            lf.write("{}\t{}\t{}\t{}\t{}\n").format(
                DataLogger.log_data["site_name"],
                DataLogger.log_data["sensor"],
                DataLogger.log_data["log_timestamp"],
                DataLogger.log_data["hourly_flow"],
                DataLogger.log_data["daily_flow"],
            )

        lf.close()

    @staticmethod
    def write_log_to_db(dict_to_write):
        Query.insert(dict_to_write)
