#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:34:11 2023

@author: Justin
"""

import RPi.GPIO as GPIO
import sys
import time
import json
import threading

from datetime import datetime as dt
from datetime import timedelta as td
from tinydb import TinyDB, Query
from utilities import Settings

class DataLogger:
    def __init__(self, settings):
        self.settings = Settings.retrieve_settings()
        self.GPIO_LIST = [22, 23, 24, 25]
        self.GPIO = GPIO  # Initialize GPIO module
        self.GPIO.setmode(GPIO.BCM)  # Use GPIO Numbering Mode

        # Defines the GPIO type (Input or Output)
        for io in self.GPIO_LIST:
            self.GPIO.setup(io, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def logging(self):
            curr_hour = dt.now().hour
            curr_min = dt.now().minute
            settings = Settings.retrieve_settings()

            # Get settings values
            pulse_per_unit = settings['k_factor']
            standard_unit = settings['standard_unit']
            desired_units = settings['desired_unit']
            countPulse = ''

            GPIO.add_event_detect(
                self.GPIO_LIST[0], GPIO.FALLING, callback=countPulse)

            if self.settings['output'] == 'local':
                self.save_data = self.write_log_to_db()
            else:
                self.save_data = self.write_log_to_file()
            
            
            log_data = {'site_name': self.settings['site_name'], 
            'sensor': self.settings['sensor_name'],
            'log_timestamp': dt.now()}
            
            

        def stop_logging(self):
            self.GPIO.cleanup()
            sys.exit()

        def write_log_to_file(self):
            curr_day = dt.strftime(dt.today(), '%y-%m-%d')
            yesterday = dt.strftime(dt.today() - td (days = 1), '%y-%m-%d')
            
            self.log_file = '/home/ect-one-user/Desktop/One_Water_Pulse_Logger/gui_app/logger_data'
            with open(self.log_file, 'a') as lf :
                lf.write('{}\t{}\t{}\t')
                
            lf.close()
            
        def write_log_to_db(self):
            Query.insert(self.log_data)
