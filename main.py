from sys import path
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import subprocess
import os
import sys
from obfuscapk import main


obfuscator_name = None
apk_path = None

Obfuscators = {
    "AdvancedReflection":"AdvancedReflection",
    "ArithmeticBranch":"ArithmeticBranch",
    "AssetEncryption":"AssetEncryption",
    "CallIndirection":"CallIndirection",
    "ClassRename":"ClassRename",
    "ConstStringEncryption":"ConstStringEncryption",
    "DebugRemoval":"DebugRemoval",
    "FieldRename":"FieldRename",
    "Goto":"Goto",
    "LibEncryption":"LibEncryption",
    "MethodOverload":"MethodOverload",
    "MethodRename":"MethodRename",
    "NewAlignment":"NewAlignment",
    "NewSignature":"NewSignature",
    "Nop":"Nop",
    "RandomManifest":"RandomManifest",
    "Rebuild":"Rebuild",
    "Reflection":"Reflection",
    "Reorder":"Reorder",
    "ResStringEncryption":"ResStringEncryption",
    "VirusTotal":"VirusTotal"
}


KV = '''
MDBoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: "Apk Obfuscator"
        left_action_items: [['menu', lambda x: None]]
        elevation: 10

    MDFloatLayout:

        MDRoundFlatIconButton:
            text: "Select Apk"
            icon: "folder"
            pos_hint: {'center_x': .5, 'center_y': .6}
            on_release: app.file_manager_open()

        
        MDDropDownItem:
            id: drop_item
            pos_hint: {'center_x': .5, 'center_y': .5}
            text: 'Select Obfuscation'
            on_release: app.menu.open()

        MDRaisedButton:
            text:"Obfuscate"
            icon: "assets/file.png"
            pos_hint:{"center_x": 0.5, "center_y": 0.4}
            md_bg_color: app.theme_cls.primary_dark
            on_press:app.click()

'''
class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.screen = Builder.load_string(KV)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )
        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "git",
                "text": f"{i}",
                "height": dp(56),
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in Obfuscators.keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.screen

    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        global obfuscator_name
        obfuscator_name = text_item
        self.menu.dismiss()

    def file_manager_open(self):
        self.file_manager.show(self.user_data_dir)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.apk_path = path
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def click(self):
        try:
            main.perform_obfuscation(self.apk_path,[obfuscator_name])
        except AttributeError as e:
            toast("Please Select an apk first")
        except FileNotFoundError as e:
            toast("Please Select a valid apk file")
        except Exception as e:
            toast("Something Error Happened")

if __name__ == "__main__":
    Example().run()