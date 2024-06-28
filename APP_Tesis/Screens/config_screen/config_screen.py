from kivymd.uix.backdrop.backdrop import MDBoxLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.backdrop.backdrop import MDFloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from Screens.componentes.header.header import Header
from Screens.componentes.listitem.list_item import (
    OneLineListItemWithSwitch,
    TwoLineListItemWithSwitch,
)
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivymd.uix.list import OneLineAvatarIconListItem
from kivy.uix.image import Image
import mysql.connector
from Screens.login_screen.login_screen import LoginScreen
import configparser


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class ConfigScreen(Screen):
    dialog = None

    def UserProfile(self):
        self.previous_screen = self.manager.current
        self.manager.current = "user_screen"

    def Back(self):
        self.manager.current = self.previous_screen

    def change_theme(self, active):
        if active:
            print("Tema Oscuro activado")
            # Aplicar el tema oscuro
            TestApp.get_running_app().theme = "dark"
        else:
            print("Tema Claro activado")
            # Aplicar el tema claro
            TestApp.get_running_app().theme = "light"

    def set_theme(self, theme):
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = theme

    def save_new_username(self, new_username):
        login_screen = LoginScreen()
        email = login_screen.return_userlog()
        print(email, " user")
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]

        db = mysql.connector.connect(
            host=host, user=user, password=password, database=dbname
        )
        cursor = db.cursor()
        query = "UPDATE users SET username=%s WHERE email=%s"
        cursor.execute(query, (new_username, email))
        db.commit()

        cursor.close()
        db.close()

        print(f" {new_username} guardada en la base de datos.")

    def get_theme(self):
        app = MDApp.get_running_app()
        print(app.theme_cls.theme_style)
        style = app.theme_cls.theme_style
        return style

    def show_confirmation_dialog(self):
        app = MDApp.get_running_app()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=lambda instance: self.dismiss_modal(),
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_press=lambda instance: self.save_new_username(
                            self.dialog.content_cls.get_text()
                        ),
                        on_release=lambda instance: self.dismiss_modal(),
                    ),
                ],
            )
        self.dialog.open()

    def dismiss_modal(self):
        if self.dialog:
            self.dialog.dismiss()  # Dismiss the popup


class Content(BoxLayout):
    def get_text(self):
        text_input = (
            self.ids.text_input
        )  # Suponiendo que has asignado un id al MDTextField
        return text_input.text
