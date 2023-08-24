#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:33:16 2023

@author: Justin
"""

from guizero import App, Box, info, Picture, PushButton, Text, TextBox, Window
from datetime import datetime as dt
import subprocess
import sys
from data_output_setup_page import DataOutputSetupPage
from sensor_setup_page import SensorSetupPage
from logging_data_display import DataDisplayPage
from utilities import Settings


class MainApp:
    def __init__(self):

        self.submit_site_text = 'Submit'
        self.app = App('Epic One Water Pulse Logging',
                       width=800, height=480, bg='#050f2b')
        # Maximize the app window
        #self.app.tk.attributes('-fullscreen', True)

        # Top Box for header
        self.top_box = Box(self.app, layout="grid")
        self.brand = Picture(self.top_box, image=r'/home/ect-one-user'
                                                 r'/Desktop/One_Water_Pulse_Logger'
                                                 r'/assets/Epic_Clean_Tec_Brand.png',
                             align='left', grid=[0, 0])
        self.header = Text(self.top_box, text=dt.now().strftime('%Y-%m-%d %H:%M:%S'),
                           align='right', grid=[1, 0])
        self.header.width = 90
        self.header.text_color = 'white'

        # Middle of Screen box
        self.box = Box(self.app, layout='grid', align='top')
        self.welcome_text = Text(self.box, text="Welcome to the Epic CleanTec Pulse Logger Prototype.",
                                 size=14, align='top', grid=[0, 0, 2, 1])
        self.welcome_text.text_color = 'white'

        self.welcome_text_l2 = Text(self.box, text="Please send any feedback to JPulley4396@Gmail.com",
                                    size=14, align='top', grid=[0, 1, 2, 1])
        self.welcome_text_l2.text_color = 'white'

        self.spacer = Text(self.box, text='', grid=[0, 2])

        self.site_name_label = Text(self.box, text='Site Name:', grid=[0, 3])
        self.site_name_label.text_color = 'white'

        self.site_name = TextBox(self.box, grid=[1, 3])
        self.site_name.width = 30
        self.site_name.bg = 'white'
        
        self.submit_site =  PushButton(self.box, text=self.submit_site_text,
        command=self.save_settings, grid = [2, 3])
        self.submit_site.text_color = 'white'
        
        self.spacer = Text(self.box, text='', grid=[0, 4], width='fill')
        
        self.sv_stg_to_file = PushButton(self.box, text='Save Settings File',
        command=Settings.save_to_json, grid=[0, 5], align='top')
        self.sv_stg_to_file.text_color = 'white'
        

        # Create a button holder at bottom of screen
        self.bottom_box = Box(self.app, layout='grid', align='bottom')
        self.open_ds_button = PushButton(self.bottom_box, text='Open Data Output Setup',
                                         command=lambda: self.open_window(
                                             DataOutputSetupPage, 'Data Output Setup'),
                                         align='left', grid=[0, 0])
        self.open_ds_button.text_color = 'white'
        self.open_ss_button = PushButton(self.bottom_box, text='Open Sensor Setup',
                                         command=lambda: self.open_window(
                                             SensorSetupPage, 'Sensor Setup'),
                                         align='left', grid=[1, 0])
        self.open_ss_button.text_color = 'white'
        self.open_db_button = PushButton(self.bottom_box, text='Open Logging',
                                         command=lambda: self.open_window(
                                             DataDisplayPage, 'Logging'),
                                         align='left', grid=[2, 0])
        self.open_db_button.text_color = 'white'
        self.close_button = PushButton(self.bottom_box, text='Shutdown Logger',
                                       command=self.exit_pgm,
                                       align='left', grid=[3, 0])
        self.close_button.text_color = 'white'

    def run(self):

        self.app.display()
        
    def get_settings(self):

        self.settings = Settings.retrieve_settings()
        self.sv_stg_to_file.hide()
        print(self.settings)
        if not self.settings is None and not Settings.site_name is None \
        and not Settings.sensor_name is None \
        and not Settings.data_output_choice is None:
            info('Status', 'Settings ready for save.')
            self.sv_stg_to_file.show()
                
    def save_settings(self):

        if self.submit_site_text == 'Submit' :
            Settings.update_settings({'site_name': self.site_name.value})
            self.site_name.disable()
            self.submit_site_text = 'Alter Site Name'
        else:
            self.site_name.enable()
            self.submit_site_text = 'Submit'
            
        self.submit_site.text = self.submit_site_text

    def open_window(self, module, wdw_name):

        self.app.hide()
        new_window = Window(
            self.app, title=wdw_name, width=800, height=480, bg='#050f2b')
        #new_window.tk.attributes('-fullscreen', True)
        
        # Create an instance of DataDisplayPage
        open_page = module(new_window, self)
        new_window.show()

    def exit_pgm(self):

        self.app.destroy()
        # subprocess.Popen(['shutdown','-h','now'])
        sys.exit()


if __name__ == "__main__":
    app = MainApp()
    app.get_settings()
    app.run()
