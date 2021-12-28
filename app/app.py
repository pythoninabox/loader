#!/usr/bin/env python3

import trio
from serial.tools.list_ports import comports
from pathlib import Path
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.menu import MDDropdownMenu

from clocker import Clocker
from clocker import PlaceholderSerialPort


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Window.bind(on_keyboard=self.events)
        self.firmware_path = False
        self.serial_port = False
        self.manager_open = False
        self.spinner_status = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            selector='file',
            ext=['.py', '.bin']
        )

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Teal"
        screen = Screen()
        Window.size = (800, 600)
        return screen

    def stampaddio():
        print("ciao ciao!")

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
        path = self.get_absolute_path(path)
        label.text = path
        self.firmware_path = path
        self.loader_button_active()
        toast(path)

    def loader_button_active(self):
        loader_button = self.root.ids.loader_button

        if self.firmware_path and self.serial_port:
            loader_button.disabled = False
        else:
            loader_button.disabled = True

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def get_absolute_path(self, path):
        p = Path(path)
        return p.resolve().__str__()

    def load_on_device(self):
        trio.run(self.nursery_erase)

    # erasing/updating operations

    async def nursery_erase(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.status_spinner, True)
            nursery.start_soon(self.erase_flash, self.serial_port)

    async def nursery_update(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.status_spinner, True)
            nursery.start_soon(self.update_flash,
                               self.serial_port, self.firmware_path)

    def active_update(self):
        trio.run(self.nursery_update)

    async def erase_flash(self, device):
        """erase esp32 flash"""

        command = ['esptool.py', '--chip', 'esp32',
                   '--port', device.device, 'erase_flash']

        toast("erasing...", duration=1)
        res = await trio.open_process(['sleep', '2'])

        clock = Clocker(res, 0.25, self.active_update)
        clock.start()

    async def update_flash(self, device, firmware):
        """update esp32 flash"""

        command = ['esptool.py', '--chip', 'esp32', '--port', device.device,
                   '--baud', '460800', 'write_flash', '-z', '0x1000', firmware]

        toast("updating...", duration=1)
        res = await trio.open_process(['sleep', '2'])

        clock = Clocker(res, 0.25, self.final_exitus)
        clock.start()

    def final_exitus(self):
        spinner_id = self.root.ids.loader_spinner
        spinner_id.active = False
        exitus = self.root.ids.exitus
        exitus.text = "PROCESS COMPLETED"

    async def status_spinner(self, status):
        spinner_id = self.root.ids.loader_spinner
        spinner_id.active = status

    def show_serial_menu(self):
        s_ports = self.get_serial_ports()

        menu_items = [
            {
                "text": f"{i.device}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.menu_callback(x),
            } for i in s_ports
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.serial_port_button,
            items=menu_items,
            width_mult=4,
            max_height=len(s_ports) * 48
        )

        self.menu.open()

    def menu_callback(self, dev):
        but = self.root.ids.serial_port_button
        but.text = dev.device
        self.serial_port = dev
        self.loader_button_active()
        self.menu.dismiss()

    def get_serial_ports(self):
        ports = comports()
        if ports:
            return ports
        else:
            return [PlaceholderSerialPort()]


MainApp().run()
