#!/usr/bin/python
"""
Created on Tue Aug  8 20:33:16 2023

@author: Justin
"""

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
from datetime import datetime as dt
import subprocess
import sys
from data_output_setup_page import LoggerSetupPage
from logging_data_display import DataDisplayPage
import logging as log
from utilities import LoggerSettings, PopupHandler


class MainApp:
    def __init__(self):
        self.submit_site_text = "Submit"
        self.app = App(
            "Epic One Water Pulse Logging", width=800, height=480, bg="#050f2b"
        )
        # Maximize the app window
        # self.app.tk.attributes('-fullscreen', True)

        # Top Box for header
        self.top_box = Box(self.app, layout="grid")
        self.brand = Picture(
            self.top_box,
            image=r"/home/ect-one-user"
            r"/Desktop/One_Water_Pulse_Logger"
            r"/assets/Epic_Clean_Tec_Brand.png",
            align="left",
            grid=[0, 0],
        )
        self.header = Text(
            self.top_box,
            text=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
            align="right",
            grid=[1, 0],
            width="fill",
        )
        self.header.text_color = "white"
        self.header.width = 90

        self.welcome_box = Box(self.app, layout="grid", align="top")
        self.welcome_text = Text(
            self.welcome_box,
            text="Welcome to the Epic CleanTec Pulse Logger Prototype.",
            size=14,
            grid=[0, 0],
        )
        self.welcome_text.text_color = "white"
        self.welcome_text.width = 90

        self.welcome_text_l2 = Text(
            self.welcome_box,
            text="Please send any feedback to JPulley4396@Gmail.com",
            size=14,
            grid=[0, 1],
        )
        self.welcome_text_l2.text_color = "white"
        self.welcome_text_l2.width = 90

        # Middle of Screen box
        self.box = Box(self.app, layout="grid", align="top")
        self.spacer = Text(self.box, text="", grid=[0, 1], width="fill")

        self.site_name_label = Text(self.box, text="Site Name:", grid=[0, 2])
        self.site_name_label.text_color = "white"

        self.l_spacer = Text(self.box, text="", grid=[1, 2])

        self.site_name = TextBox(self.box, grid=[2, 2])
        self.site_name.width = 20
        self.site_name.bg = "white"

        self.r_spacer = Text(self.box, text="", grid=[3, 2])

        self.submit_site = PushButton(
            self.box, text=self.submit_site_text, command=self.site_lock, grid=[4, 2]
        )
        self.submit_site.text_color = "white"

        self.spacer = Text(self.box, text="", grid=[0, 3], width="fill")

        self.sv_box = Box(self.app, layout="auto", align="top")
        self.sv_stg_to_file = PushButton(
            self.sv_box, text="Save Settings File", command=self.save_settings
        )
        self.sv_stg_to_file.text_color = "white"
        self.sv_stg_to_file.width = 50
        self.sv_stg_to_file.hide()

        # Create a button holder at bottom of screen
        self.bottom_box = Box(self.app, layout="grid", align="bottom")
        self.open_ds_button = PushButton(
            self.bottom_box,
            text="Logger Setup",
            command=lambda: self.open_window(LoggerSetupPage, "Logger Setup"),
            align="left",
            grid=[0, 0],
        )
        self.open_ds_button.text_color = "white"
        self.open_ds_button.hide()

        self.open_db_button = PushButton(
            self.bottom_box,
            text="Open Logging",
            command=lambda: self.open_window(DataDisplayPage, "Logging"),
            align="left",
            grid=[1, 0],
        )
        self.open_db_button.text_color = "white"
        self.open_db_button.hide()

        self.close_button = PushButton(
            self.bottom_box,
            text="Shutdown Logger",
            command=self.exit_pgm,
            align="left",
            grid=[2, 0],
        )
        self.close_button.text_color = "white"

    def run(self):
        self.app.display()

    def get_settings(self):
        LoggerSettings.site_name = self.site_name.value
        self.settings = LoggerSettings.retrieve_settings()

        if self.settings[0]["File Exists"]:
            load_settings = PopupHandler.popup_create(
                {
                    "Type": "yesno",
                    "Title": "Load Settings",
                    "Message": "Settings file found. Load settings?",
                }
            )
            if load_settings:
                self.open_window(DataDisplayPage, "Logging")
        else:
            PopupHandler.popup_create(
                {
                    "Type": "info",
                    "Title": "Config",
                    "Message": "No settings file found. Please configure settings.",
                }
            )

    def site_lock(self):
        if self.submit_site_text == "Submit":
            self.site_name.disable()
            self.submit_site_text = "Alter Site Name"
            LoggerSettings.update_settings({"Site Name": self.site_name.value})
            self.get_settings()
            self.open_ds_button.show()

            # Add a log statement
            log.info(f"Site name updated to {self.site_name.value}")

        else:
            self.site_name.enable()
            self.submit_site_text = "Submit"
            self.open_ds_button.hide()
            self.open_db_button.hide()

            # Add a log statement
            log.info(f"Site name updated to {self.site_name.value}")

        self.submit_site.text = self.submit_site_text

    def verify_json(self):
        self.local_settings = LoggerSettings.check_json()

        if all(self.local_settings):
            PopupHandler.popup_create(
                {
                    "Type": "info",
                    "Title": "Config",
                    "Message": "Settings ready for save.",
                }
            )
            self.sv_stg_to_file.show()

    def save_settings(self):
        LoggerSettings.save_to_json()
        PopupHandler.popup_create(
                {
                    "Type": "info",
                    "Title": "Config",
                    "Message": "Settings saved to file.",
                }
            )
        self.sv_stg_to_file.hide()
        self.open_ds_button.disable()
        self.open_db_button.show()

    def open_window(self, module, wdw_name):
        self.app.hide()
        new_window = Window(
            self.app, title=wdw_name, width=800, height=480, bg="#050f2b"
        )
        # new_window.tk.attributes('-fullscreen', True)

        # Create an instance of DataDisplayPage
        open_page = module(new_window, self)
        new_window.show()

    def exit_pgm(self):
        self.app.destroy()
        # subprocess.Popen(['shutdown','-h','now'])
        sys.exit()


if __name__ == "__main__":
    app = MainApp()
    app.run()
