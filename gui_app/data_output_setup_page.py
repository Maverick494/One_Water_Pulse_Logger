#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 20:33:42 2023
@author: Justin

"""

from base64 import b64encode as be
from base64 import b64decode as bd
from datetime import datetime as dt
from guizero import Box, Combo, info, Picture, ListBox, PushButton, Text, TextBox, Window
from utilities import Settings

class LoggerSetupPage:

    def __init__(self, parent, main_app):

        self.parent = parent
        self.main_app = main_app
        self.current_row = 0       
        self.settings_dict = {}
        self.widgets_to_destroy = []
        
        # Top Box for header
        self.top_box = Box(self.parent, layout='grid')

        # Display the brand logo in the top left corner of the main window.
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

        self.config_selection = Combo(
            self.mid_box,
            options=[ 'Data Output Config', 'Sensor Config'],
            command=self.check_selection,
            grid=[0, 0]
        )
        self.config_selection.text_color = 'white'
        self.config_selection.text_size = 16

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

    def create_input_list(self):
        
            if self.config_selection.value == 'Data Output Config':
                    
                self.data_output_choice_label = Text(self.mid_box, text='Data Output:',
                grid=[0, 0])
                self.data_output_choice_label.text_color = 'white'

                self.data_output_choice = Combo(self.mid_box,
                options=['local', 's3', 'ftp'], command=self.check_sub_selection,
                grid=[1, 0])
                self.data_output_choice.text_color = 'white'

                self.current_row += 1

                self.widgets_to_destroy.extend([
                    self.data_output_choice_label,
                    self.data_output_choice
                    ])

    def create_inputs(self):

        if self.config_selection.value == 'Sensor Config':

            self.sn_label = Text(self.mid_box, text='Sensor Name:',
                align='right', grid=[0, 1])
            self.sn_label.text_color = 'white'
            self.sn_input = TextBox(self.mid_box, grid=[1, 1], width=30)
            self.sn_input.text_color = 'white'

            self.current_row += 1
            
            self.kf_label = Text(self.mid_box, text='K Factor:',
                align='right', grid=[0, 2])
            self.kf_label.text_color = 'white'
            self.kf_input = TextBox(self.mid_box, grid=[1, 2], width=10)
            self.kf_input.text_color = 'white'

            self.current_row += 1
            
            self.su_label = Text(self.mid_box, text='Sensor Units:',
                        align='right', grid=[0, 3])
            self.su_label.text_color = 'white'
            self.su_input = TextBox(self.mid_box, grid=[1, 3], width=10)
            self.su_input.text_color = 'white'

            self.current_row += 1
            
            self.du_label = Text(self.mid_box, text='Desired Units:', grid=[0, 4])
            self.du_label.text_color = 'white'
            self.du_input = TextBox(self.mid_box, grid=[1, 4], width=10)
            self.du_input.text_color = 'white'

            self.current_row += 1

            self.widgets_to_destroy.extend([
                self.sn_label,
                self.sn_input,
                self.kf_label,
                self.kf_input,
                self.su_label,
                self.su_input,
                self.du_label,
                self.du_input
                ])
                      
        elif self.data_output_choice.value == 's3':

            self.l_spacer = Text(self.mid_box, text='', grid=[0, 1], width = 'fill')

            self.current_row += 1             

            self.s3_bucket_label = Text(self.mid_box, text='S3 Bucket:',
            grid=[0, 2], align='left')
            self.s3_bucket_label.text_color = 'white'

            self.s3_bucket_input = TextBox(self.mid_box, grid=[1, 2], width=30,
            align='left')
            self.s3_bucket_input.text_color = 'white'

            self.current_row += 1

            self.s3_prefix_label = Text(self.mid_box, text='S3 Folder:',
            grid=[0, 3], align='left')
            self.s3_prefix_label.text_color = 'white'

            self.s3_prefix_input = TextBox(self.mid_box, grid=[1, 3], width=30,
            align='left')
            self.s3_prefix_input.text_color = 'white'

            self.current_row += 1

            self.s3_key_label = Text(self.mid_box, text='S3 Filename:', 
            grid=[0, 4], align='left')
            self.s3_key_label.text_color = 'white'

            self.s3_key_input = TextBox(self.mid_box, grid=[1, 4], width=30,
            align='left')
            self.s3_key_input.text_color = 'white'

            self.current_row += 1

            self.s3_ak_label = Text(self.mid_box, text='User Access Key:',
            grid=[0, 5], align='left')
            self.s3_ak_label.text_color = 'white'

            self.s3_ak_input = TextBox(self.mid_box, grid=[1, 5], width=30,
            align='left')
            self.s3_ak_input.text_color = 'white'

            self.current_row += 1

            self.s3_sk_label = Text(self.mid_box, text='User Secret Key:',
            grid=[0, 6], align='left')
            self.s3_sk_label.text_color = 'white'

            self.s3_sk_input = TextBox(self.mid_box, grid=[1, 6], width=30,
            align='left')
            self.s3_sk_input.text_color = 'white'

            self.current_row += 1

            self.s3_role_label = Text(self.mid_box, text='Role to Assume:',
            grid=[0, 7], align='left')
            self.s3_role_label.text_color = 'white'

            self.s3_role_input = TextBox(self.mid_box, grid=[1, 7], width=30,
            align='left')
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
                self.l_spacer
                ])

        elif self.data_output_choice.value == 'ftp':
            
            self.l_spacer = Text(self.mid_box, text='', grid=[0, 1], width = 'fill')

            self.ftp_host_label = Text(self.mid_box, text='FTP Host:',
            grid=[0, 2], align='left')
            self.ftp_host_label.text_color = 'white'

            self.ftp_host_input = TextBox(self.mid_box, grid=[1, 2], width=30,
            align='left')
            self.ftp_host_input.text_color = 'white'

            self.current_row += 1

            self.ftp_port_label = Text(self.mid_box, text='FTP Port:',
            grid=[0, 3], align='left')
            self.ftp_port_label.text_color = 'white'

            self.ftp_port_input = TextBox(self.mid_box, grid=[1, 3], width=30,
            align='left')
            self.ftp_port_input.text_color = 'white'

            self.current_row += 1

            self.ftp_un_label = Text(self.mid_box, text='FTP Username:',
            grid=[0, 4], align='left')
            self.ftp_un_label.text_color = 'white'

            self.ftp_un_input = TextBox(self.mid_box, grid=[1, 4], width=30,
            align='left')
            self.ftp_un_input.text_color = 'white'

            self.current_row += 1

            self.ftp_pwd_label = Text(self.mid_box, text='FTP Password:',
            grid=[0, 5], align='left')
            self.ftp_pwd_label.text_color = 'white'

            self.ftp_pwd_input = TextBox(self.mid_box, grid=[1, 5], width=30,
            align='left')
            self.ftp_pwd_input.text_color = 'white'

            self.current_row += 1

            self.ftp_dir_label = Text(self.mid_box, text='Save Location:',
            grid=[0, 6], align='left')
            self.ftp_dir_label.text_color='white'

            self.ftp_dir_input = TextBox(self.mid_box, grid=[1, 6], width=30,
            align='left')
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
                self.l_spacer
                ])

        elif self.data_output_choice.value == 'local':
            
            self.l_spacer = Text(self.mid_box, text='', grid=[0, 1], width = 'fill')

            self.email_address_label = Text(self.mid_box, text='Email Address:',
            grid=[0, 2], align='left')
            self.email_address_label.text_color = 'white'

            self.email_address_input = TextBox(self.mid_box, grid=[1, 2], width=40,
            align='left')
            self.email_address_input.text_color = 'white'

            self.current_row += 1

            self.widgets_to_destroy.extend([
                self.email_address_label,
                self.email_address_input,
                self.l_spacer
                ])
                         
        # Create a button to return the ListBox to visible
        self.show_list_btn = PushButton(self.bottom_box, text='Back to List',
        command=self.show_config, grid=[0, self.current_row+1],
        align='bottom')
        self.show_list_btn.text_color = 'white'

        self.save_settings_btn = PushButton(self.bottom_box, text='Save Settings',
        command=self.save_settings, grid=[1, self.current_row+1], align='bottom')
        self.save_settings_btn.text_color = 'white'
        
        self.widgets_to_destroy.extend([
            self.show_list_btn,
            self.save_settings_btn
            ])
                
    def import_settings(self, kwargs):
        if kwargs['Location'] == 's3':
            self.data_output_choice.value = 's3'
            self.s3_bucket_input.value = kwargs['Bucket']
            self.s3_prefix_input.value = kwargs['Prefix']
            self.s3_key_input.value = kwargs['Key']
            self.s3_ak_input.value = bd(kwargs['Access Key']).decode('utf-8')
            self.s3_sk_input.value = bd(kwargs['Secret Key']).decode('utf-8')
            self.s3_role_input.value = kwargs['Role']
        elif kwargs['Location'] == 'ftp':
            self.data_output_choice.value = 'ftp'
            self.ftp_host_input.value = kwargs['Host']
            self.ftp_port_input.value = kwargs['Port']
            self.ftp_un_input.value = bd(kwargs['Username']).decode('utf-8')
            self.ftp_pwd_input.value = bd(kwargs['Password']).decode('utf-8')
            self.ftp_dir_input.value = kwargs['Directory']
        else:
            self.data_output_choice.value = 'local'
            self.email_input.value = kwargs['Email Address']
        
        self.sn_input.value = kwargs['Name']
        self.kf_input.value = kwargs['K Factor']
        self.su_input.value = kwargs['Standard Unit']
        self.du_input.value = kwargs['Desired Unit']
    
    def save_settings(self):

        if self.config_selection.value == 'Data Output Config':
            if self.data_output_choice.value == 's3':
                self.settings_dict.update(
                    {'Location': self.data_output_choice.value,
                    'Bucket': self.s3_bucket_input.value,
                    'Prefeix': self.s3_prefix_input.value,
                    'Key': self.s3_key_input.value,
                    'Access Key': be(self.s3_ak_input.value.encode('utf-8')),
                    'Secret Key': be(self.s3_sk_input.value.encode('utf-8')),
                    'Role': self.s3_role_input.value})

            elif self.data_output_choice.value == 'ftp':
                self.settings_dict.update(
                    {'Location': self.data_output_choice.value,
                    'Host': self.ftp_host_input.value, 
                    'Port': self.ftp_port_input.value,
                    'Username': be(self.ftp_un_input.value.encode('utf-8')),
                    'Password': be(self.ftp_pwd_input.value.encode('utf-8')),
                    'Directory': self.ftp_dir_input.value})
            else:
                self.settings_dict.update(
                {'Location': self.data_output_choice.value,
                'Email Address': self.email_input.value})

        elif self.config_selection.value == 'Sensor Config':
            self.settings_dict.update(
                {'Name': self.sn_input.value,
                'K Factor': self.kf_input.value,
                'Standard Unit': self.su_input.value,
                'Desired Unit': self.du_input.value})
            
        Settings.update_settings(self.settings_dict)
        info('success', 'settings staged.')
        self.return_to_main()

    def check_selection(self):

        if self.config_selection.value == 'Data Output Config':          
            # Hide the ListBox
            self.config_selection.hide()
            self.return_button.hide()
            
            # Create input widgets
            self.create_input_list()
            self.create_inputs()

        elif self.config_selection.value == 'Sensor Config':
            # Hide the ListBox
            self.config_selection.hide()
            self.return_button.hide()
            
            # Create input widgets
            self.create_inputs()

    def check_sub_selection(self):

        if self.data_output_choice.value in ['ftp', 's3'] \
            and self.config_selection.visible == False:
            # Destroy input widgets and the "Show List" button
            self.destroy_widgets()

            # Create input widgets
            self.create_inputs()

    def destroy_widgets(self):

        # Destroy existing input widgets if there are any
        for widget in self.widgets_to_destroy:
            widget.destroy()

        self.widgets_to_destroy = []  # Clear the list

    def show_config(self):

        # Destroy input widgets and the "Show List" button
        self.destroy_widgets()

        # Show the ListBox
        self.config_selection.show()
        self.return_button.show()