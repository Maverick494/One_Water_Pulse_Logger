#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:33:42 2023
@author: Justin

"""

from base64 import b64encode as be
from datetime import datetime as dt
from guizero import Box, Combo, info, Picture, ListBox, PushButton, Text, TextBox, Window
from utilities import Settings

class DataOutputSetupPage:

    def __init__(self, parent, main_app):

        self.parent = parent
        self.main_app = main_app
        self.current_row = 0       
        self.settings_dict = {}
        self.widgets_to_destroy = []
        
        # Top Box for header
        self.top_box = Box(self.parent, layout='grid')

        self.brand = Picture(self.top_box,
                             image='/home/ect-one-user/Desktop/One_Water_Pulse_Logger/assets/Epic_Clean_Tec_Brand.png'
                             , align='left', grid=[0, 0])

        self.header = Text(self.top_box,
                           text=dt.now().strftime('%Y-%m-%d %H:%M:%S'),
                           align='right', grid=[1, 0])
        self.header.width = 90
        self.header.text_color = 'white'

        # Middle box
        self.mid_box = Box(self.parent, layout='grid')

        self.data_output = Combo(
            self.mid_box,
            options=[ 'local', 'ftp', 's3'],
            command=self.check_selection,
            grid=[0, 0]
        )
        self.data_output.text_color = 'white'
        self.data_output.text_size = 16

        # Bottom box for buttons
        self.bottom_box = Box(self.parent, layout='grid', align='bottom')

        self.return_button = PushButton(self.bottom_box,
                text='Return to Main Page',
                command=self.return_to_main, align='bottom', grid=[0, 2])
        self.return_button.text_color = 'white'

    def return_to_main(self):

        self.main_app.app.show()
        self.main_app.get_settings()
        self.parent.destroy()

    def create_widgets(self):

        self.t_spacer = Text(self.mid_box, text='', grid=[0, 0], width = 'fill')

        if self.data_output.value == 's3':

            self.s3_bucket_label = Text(self.mid_box, text='S3 Bucket:',
            grid=[0, 1], align='left')
            self.s3_bucket_label.text_color = 'white'

            self.s3_bucket_input = TextBox(self.mid_box, grid=[1, 1], width=40)
            self.s3_bucket_input.text_color = 'white'

            self.current_row += 1

            self.s3_prefix_label = Text(self.mid_box, text='S3 Folder:',
            grid=[0, 2], align='left')
            self.s3_prefix_label.text_color = 'white'

            self.s3_prefix_input = TextBox(self.mid_box, grid=[1, 2], width=40)
            self.s3_prefix_input.text_color = 'white'

            self.current_row += 1

            self.s3_key_label = Text(self.mid_box, text='S3 Filename:', 
            grid=[0, 3], align='left')
            self.s3_key_label.text_color = 'white'

            self.s3_key_input = TextBox(self.mid_box, grid=[1, 3], width=40)
            self.s3_key_input.text_color = 'white'

            self.current_row += 1

            self.s3_ak_label = Text(self.mid_box, text='User Access Key:',
            grid=[0, 4], align='left')
            self.s3_ak_label.text_color = 'white'

            self.s3_ak_input = TextBox(self.mid_box, grid=[1, 4], width=40)
            self.s3_ak_input.text_color = 'white'

            self.current_row += 1

            self.s3_sk_label = Text(self.mid_box, text='User Secret Key:',
            grid=[0, 5], align='left')
            self.s3_sk_label.text_color = 'white'

            self.s3_sk_input = TextBox(self.mid_box, grid=[1, 5], width=40)
            self.s3_sk_input.text_color = 'white'

            self.current_row += 1

            self.s3_role_label = Text(self.mid_box, text='Role to Assume:',
            grid=[0, 6], align='left')
            self.s3_role_label.text_color = 'white'

            self.s3_role_input = TextBox(self.mid_box, grid=[1, 6], width=40)
            self.s3_role_input.text_color = 'white'

            self.current_row += 1

            self.widgets_to_destroy.extend([
                self.s3_bucket_label,
                self.s3_bucket_input,
                self.s3_prefix_label,
                self.s3_prefix_input,
                self.s3_key_label,
                self.s3_key_input,
                self.s3_ak_label,
                self.s3_ak_input,
                self.s3_sk_label,
                self.s3_sk_input,
                self.s3_role_label,
                self.s3_role_input,
                ])

        if self.data_output.value == 'ftp':
            
            self.ftp_host_label = Text(self.mid_box, text='FTP Host:',
            grid=[0, 1], align='left')
            self.ftp_host_label.text_color = 'white'

            self.ftp_host_input = TextBox(self.mid_box, grid=[1, 1], width=40)
            self.ftp_host_input.text_color = 'white'

            self.current_row += 1

            self.ftp_port_label = Text(self.mid_box, text='FTP Port:',
            grid=[0, 2], align='left')
            self.ftp_port_label.text_color = 'white'

            self.ftp_port_input = TextBox(self.mid_box, grid=[1, 2], width=40)
            self.ftp_port_input.text_color = 'white'

            self.current_row += 1

            self.ftp_un_label = Text(self.mid_box, text='FTP Username:',
            grid=[0, 3], align='left')
            self.ftp_un_label.text_color = 'white'

            self.ftp_un_input = TextBox(self.mid_box, grid=[1, 3], width=40)
            self.ftp_un_input.text_color = 'white'

            self.current_row += 1

            self.ftp_pwd_label = Text(self.mid_box, text='FTP Password:',
            grid=[0, 4], align='left')
            self.ftp_pwd_label.text_color = 'white'

            self.ftp_pwd_input = TextBox(self.mid_box, grid=[1, 4], width=40)
            self.ftp_pwd_input.text_color = 'white'

            self.current_row += 1

            self.ftp_dir_label = Text(self.mid_box, text='Save Location:',
            grid=[0, 5], align='left')
            self.ftp_dir_label.text_color='white'

            self.ftp_dir_input = TextBox(self.mid_box, grid=[1, 5], width=40)
            self.ftp_dir_input.text_color='white'

            self.current_row += 1

            self.widgets_to_destroy.extend([
                self.ftp_host_label,
                self.ftp_host_input,
                self.ftp_port_label,
                self.ftp_port_input,
                self.ftp_un_label,
                self.ftp_un_input,
                self.ftp_pwd_label,
                self.ftp_pwd_input,
                self.ftp_dir_label,
                self.ftp_dir_input,
                ])
                                   
        # Create a button to return the ListBox to visible
        self.show_list_btn = PushButton(self.bottom_box, text='Back to List',
        command=self.show_list, grid=[0, self.current_row+1],
        align='bottom')
        self.show_list_btn.text_color = 'white'

        self.save_settings_btn = PushButton(self.bottom_box, text='Save Settings',
        command=self.save_settings, grid=[1, self.current_row+1], align='bottom')
        self.save_settings_btn.text_color = 'white'
        
        self.widgets_to_destroy.extend([
            self.t_spacer,
            self.show_list_btn,
            self.save_settings_btn
            ])
            
    def save_settings(self):
        if self.data_output_choice.value == 's3':
            self.settings_dict.update(
                {'data_output_choice': self.data_output_choice.value,
                 's3_bucket': self.s3_bucket_input.value,
                 's3_prefix': self.s3_prefix_input.value,
                 's3_key': self.s3_key_input.value,
                 'access_key': be(self.s3_ak_input.value.encode('utf-8')),
                 'secret_key': be(self.s3_sk_input.value.encode('utf-8')),
                 'role_arn': self.s3_role_input.value})

        elif self.data_output_choice.value == 'ftp':
            self.settings_dict.update(
               {'data_output_choice': self.data_output_choice.value,
                'host': self.ftp_host_input.value, 
                'port': self.ftp_port_input.value,
                'username': be(self.ftp_un_input.value.encode('utf-8')),
                'password': be(self.ftp_pwd_input.value.encode('utf-8')),
                'directory': self.ftp_dir_input.value})
        else:
            self.settings_dict.update(
            {'data_output_choice': self.data_output_choice.value})
            
        Settings.update_settings(self.settings_dict)
        info('success', 'settings staged.')
        self.return_to_main()

    def check_selection(self):
        if self.data_output.value in ['ftp','s3']:
            # Hide the ListBox
            self.data_output.hide()
            self.return_button.hide()
            
            # Create input widgets
            self.create_widgets()
        else:
            self.local_choice = info('local storage', r'local storage stores to'
            r' the local datbase. No Config Required.')
            self.return_to_main()

    def destroy_widgets(self):

        # Destroy existing input widgets if there are any
        for widget in self.widgets_to_destroy:
            widget.destroy()

        self.widgets_to_destroy = []  # Clear the list

    def show_list(self):

        # Destroy input widgets and the "Show List" button
        self.destroy_widgets()

        # Show the ListBox
        self.data_output.show()
        self.return_button.show()
