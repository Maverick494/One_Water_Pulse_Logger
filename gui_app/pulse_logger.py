#!/usr/bin/python
"""
Created on Tue Aug  8 20:34:11 2023

@author: Justin
"""

import pigpio
import threading

from benedict import benedict as bdict
from datetime import datetime as dt
from datetime import timedelta as td
from tinydb import TinyDB, Query
from utilities import LoggerSettings, StorageHandler


class DataLogger:

    flow = 0.0
    hour_total = 0.0
    day_total = 0.0

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

    settings = LoggerSettings.settings_json
    GPIO_LIST = [22, 23, 24, 25]
    logger_run = False
    curr_hour = 0
    write_min_hr = 3
    write_min_day = 58
    hour_save = 0.0
    day_save = 0.0
    log_data = {}
    pi = pigpio.pi()  # Initialize pigpio module
    pi.set_mode(GPIO_LIST[0], pigpio.INPUT)
    cb = pi.callback(GPIO_LIST[0], pigpio.RISING_EDGE)
    lock = threading.Lock()  # Add a lock for thread synchronization

    def logging():
        dl = DataLogger
        while dl.logger_run:
            flow = dl.cb.count / dl.settings["K Factor"]
        dl.hour_total += flow
        dl.day_total += dl.hour_total

    def save_logging():
        dl = DataLogger
        if dl.settings["Data Output"]["Location"] == "local":
            data_save = dl.write_log_to_db
        else:
            data_save = dl.write_log_to_file

        if dl.curr_hour == dt.now().hour and dt.now().minute == dl.write_min_hr:
            if dl.settings["Data Output"]["Sensor"]["Standard Unit"] == dl.settings["Data Output"]["Sensor"]["Desired Unit"] \
               and dl.settings["Data Output"]["Sensor"]["Standard Unit"] == "gpm":
                dl.hour_save = dl.hour_total
                dl.day_save = dl.day_total
            elif dl.settings["Data Output"]["Sensor"]["Standard Unit"] != dl.settings["Data Output"]["Sensor"]["Desired Unit"]\
                and dl.settings["Data Output"]["Sensor"]["Standard Unit"] == "lpm":
                dl.hour_save = dl.hour_total * 0.2642
                dl.day_save = dl.day_total * 0.2642

            logs_to_save = dl.update_logdata(
                {"hourly_flow": dl.hour_save, "daily_flow": dl.day_save}
            )
            data_save(logs_to_save)
            dl.hour_total = 0.0

        elif dl.curr_hour == 23 and dt.now().minute == dl.write_min_day:
            logs_to_save = dl.update_logdata(
                {"hourly_flow": dl.hour_save, "daily_flow": dl.day_save}
            )
            data_save(logs_to_save)
            dl.data_export()
            dl.hour_total = 0.0
            dl.day_total = 0.0

    def update_logdata(d):
        dl = DataLogger
        dl.log_data = {
            "site_name": dl.settings["Site Name"],
            "sensor": dl.settings["Sensor"]["Name"],
            "log_timestamp": dt.now()
        }
        bdict(dl.log_data).merge(d, overwrite=True)

    def start_logging():
        dl = DataLogger
        print(dl.settings)
        dl.logger_run = True
        dl.curr_hour = dt.now().hour

    def stop_logging():
        dl = DataLogger
        dl.logger_run = False
        dl.pi.stop()

    def data_export():
        where_to = DataLogger.settings["Data Output"]["Location"]

        if where_to in ["s3", "ftp"]:
            if where_to == "s3":
                StorageHandler.upload_to_s3(DataLogger.file_for_load)
            else:
                StorageHandler.upload_to_ftp(DataLogger.file_for_load)

    def write_log_to_file(dict_to_write):
        with open(DataLogger.file_for_load, "a") as lf:
            lf.write("{}\t{}\t{}\t{}\t{}\n").format(dict_to_write)

        lf.close()

    def write_log_to_db(dict_to_write):
        Query.insert(dict_to_write)
