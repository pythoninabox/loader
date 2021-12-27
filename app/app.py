#!/usr/bin/env python3

import random
import subprocess
from pathlib import Path
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

from kivymd.uix.menu import MDDropdownMenu
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            selector='file',
            ext=['.py']
        )
        print(self.theme_cls.font_styles)

    def build(self):
        print(self.theme_cls.__dict__)
        self.theme_cls.theme_style = "Light"
        screen = Screen()
        Window.size = (800, 600)
        return screen

    def file_manager_open(self):
        self.file_manager.show('/')  # entry point of browser
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        label = self.root.ids.firmware_path
        loader_button = self.root.ids.loader_button

        loader_button.disabled = False
        label.text = self.get_absolute_path(path)
        self.firmware_path = path
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def get_absolute_path(self, path):
        p = Path(path)
        return p.resolve().__str__()

    def load_on_device(self):
        print(self.firmware_path)

    def show_serial_menu(self):
        menu_items = [
            {
                "text": f"Item {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in range(random.randint(2, 8))
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.serial_port_button,
            items=menu_items,
            width_mult=4,
        )

        self.menu.open()

    def menu_callback(self, text_item):
        print(text_item)

    """
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True"""


MainApp().run()
