#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 10:24:48 2023

@author: Justin
"""

from guizero import Box, Combo, info, Picture, ListBox, PushButton, Text, TextBox, Window
from datetime import datetime as dt
from utilities import Settings

class SensorSetupPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        self.settings_dict = {}

        # Top Box for header
        self.top_box = Box(self.parent, layout="grid")
        self.brand = Picture(self.top_box, image=r'/home/ect-one-user'
                                                 r'/Desktop/One_Water_Pulse_Logger'
                                                 r'/assets/Epic_Clean_Tec_Brand.png',
                             align='left', grid=[0, 0])
        self.header = Text(self.top_box, text=dt.now().strftime('%Y-%m-%d %H:%M:%S'),
                           align='right', grid=[1, 0])
        self.header.width = 90
        self.header.text_color = 'white'

        # Middle box
        self.mid_box = Box(self.parent, layout='grid')
        
        self.t_spacer = Text(self.mid_box, text='', grid=[0, 0], width = 'fill')
        
        self.sn_label = Text(self.mid_box, text='Sensor Name:',
                    align='right', grid=[0, 1])
        self.sn_label.text_color = 'white'
        self.sn_input = TextBox(self.mid_box, grid=[1, 1], width=50)
        self.sn_input.text_color = 'white'
        
        self.kf_label = Text(self.mid_box, text='K Factor:',
            align='right', grid=[0, 2])
        self.kf_label.text_color = 'white'
        self.kf_input = TextBox(self.mid_box, grid=[1, 2], width=50)
        self.kf_input.text_color = 'white'
        
        self.su_label = Text(self.mid_box, text='Sensor Units:',
                    align='right', grid=[0, 3])
        self.su_label.text_color = 'white'
        self.su_input = TextBox(self.mid_box, grid=[1, 3], width=50)
        self.su_input.text_color = 'white'
        
        self.du_label = Text(self.mid_box, text='Desired Units:', grid=[0, 4])
        self.du_label.text_color = 'white'
        self.du_input = TextBox(self.mid_box, grid=[1, 4], width=50)
        self.du_input.text_color = 'white'
               
        # Bottom box for buttons
        self.bottom_box = Box(self.parent, layout="grid", align="bottom")
        
        self.save_settings_btn = PushButton(self.bottom_box, text='Save Settings',
        command=self.save_settings, grid=[0, 0], align='bottom')
        self.save_settings_btn.text_color = 'white'
        
        self.return_button = PushButton(self.bottom_box, text='Return to Main Page',
                                        command=self.return_to_main,
                                        align='bottom', grid=[1, 0])
        self.return_button.text_color = 'white'

    def return_to_main(self):
        self.main_app.app.show()
        self.parent.destroy()
        
    def save_settings(self):
            
        self.settings_dict.update({
                'sensor_name': self.sn_input.value,
                'k_factor': self.kf_input.value,
                'sensor_unit': self.su_input.value,
                'desired_unit': self.du_input.value})

        Settings.update_settings(self.settings_dict)
        info('success', 'settings staged.')
        self.return_to_main()
