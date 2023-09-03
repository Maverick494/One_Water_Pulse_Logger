#!/usr/bin/python
"""
Created on Wed Aug  9 15:02:27 2023

@author: Justin
"""

import threading
import time

from guizero import (
    Box,
    Combo,
    info,
    Picture,
    ListBox,
    PushButton,
    Text,
    TextBox,
    TitleBox,
    Window,
)
from datetime import datetime as dt
from pulse_logger import DataLogger
from utilities import PopupHandler


class DataDisplayPage:
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        # self.start = DataLogger.start_logging()
        # self.stop = DataLogger.stop_logging()

        # Add instance variables for threads
        self.display_thread = threading.Thread(target=self.update_display)
        self.save_logging_thread = threading.Thread(target=self.save_logging)

        # Top Box for header
        self.top_box = Box(self.parent, layout="grid")
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
        )
        self.header.width = 90
        self.header.text_color = "white"

        # Middle box
        self.mid_box = Box(self.parent, layout="grid")

        self.spacer = Text(self.mid_box, text="", grid=[0, 0], width="fill")

        self.flow_rate_hdr = TitleBox(
            self.mid_box,
            text="Flow Rate",
            border=2,
            layout="auto",
            grid=[0, 1],
            width=200,
            height=50,
        )
        self.flow_rate_hdr.text_color = "white"

        self.hourly_flow_hdr = TitleBox(
            self.mid_box,
            text="Flow Current Hour",
            border=2,
            layout="auto",
            grid=[1, 1],
            width=200,
            height=50,
        )
        self.hourly_flow_hdr.text_color = "white"

        self.daily_flow_hdr = TitleBox(
            self.mid_box,
            text="Flow Today",
            border=2,
            layout="auto",
            grid=[2, 1],
            width=200,
            height=50,
        )
        self.daily_flow_hdr.text_color = "white"

        self.flow_rate = Text(
            self.flow_rate_hdr, text=0.0, size=16
        ).text_color = "white"

        self.hourly_flow = Text(
            self.hourly_flow_hdr, text=0.0, size=16
        ).text_color = "white"

        self.daily_flow = Text(
            self.daily_flow_hdr, text=0.0, size=16
        ).text_color = "white"

        # Bottom box for buttons
        self.bottom_box = Box(self.parent, layout="grid", align="bottom")
        self.return_button = PushButton(
            self.bottom_box,
            text="Start Logging",
            command=self.start,
            align="bottom",
            grid=[0, 2],
        )
        self.return_button.text_color = "white"

        self.return_button = PushButton(
            self.bottom_box,
            text="Stop Logging",
            command=self.stop,
            align="bottom",
            grid=[0, 2],
        )
        self.return_button.text_color = "white"

        self.return_button = PushButton(
            self.bottom_box,
            text="Return to Main Page",
            command=self.return_to_main,
            align="bottom",
            grid=[0, 2],
        )
        self.return_button.text_color = "white"

    def return_to_main(self):
        self.main_app.app.show()
        self.parent.destroy()
        self.display_thread.stop()
        self.save_logging_thread.stop()
        PopupHandler.popup({"Type": "info",
                            "Title":"Logging Stopped",
                            "Message": "Logging has been stopped due to leaving the Data Display Page"})

    def start(self):
        DataLogger.start_logging()
        self.display_thread.start()
        self.save_logging_thread.start()
        PopupHandler.popup({"Type": "info",
                            "Title":"Logging Started",
                            "Message": "Logging has been started"})
        
    def stop(self):
        DataLogger.stop_logging()
        self.display_thread.stop()
        self.save_logging_thread.stop()
        PopupHandler.popup({"Type": "info",
                            "Title":"Logging Stopped",
                            "Message": "Logging has been stopped"})

    def update_display(self):
        while True:
            # Access and update the display elements
            self.flow_rate.value = DataLogger.hour_total
            self.hourly_flow.value = DataLogger.hour_total
            self.daily_flow.value = DataLogger.day_total
            # Sleep for 100ms
            time.sleep(0.1)

    def save_logging(self):
        while True:
            DataLogger.save_logging()  # Call the save_logging method in DataLogger
            time.sleep(60)  # Sleep for 60 seconds
