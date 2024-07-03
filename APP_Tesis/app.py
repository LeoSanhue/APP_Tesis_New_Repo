from kivy.uix.settings import Settings
from kivymd.uix.backdrop.backdrop import MDBoxLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.backdrop.backdrop import MDFloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp  # CAMBIAR
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
from Screens.user_profile_screen.user_profile_screen import UserProfileScreen
from Screens.login_screen.login_screen import *  # Importa la clase LoginScreen
from Screens.config_screen.config_screen import *  # Importa la clase ConfigScreen
from Screens.game_screen.game_screen import *  # Importa la clase GameScreen
from Screens.game_screen.list_screen import *  # Importa la clase GameScreen
from Screens.register_screen.register_screen import *  # Importa la clase RegisterScreen
from Screens.config_screen.image_viewer import *
from Screens.config_screen.background_viewer import *
import main_screen as main_screen
from kivy.uix.screenmanager import (
    ScreenManager,
    SlideTransition,
    FadeTransition,
    WipeTransition,
)
from kivy.animation import Animation
from kivy.uix.accordion import ListProperty
from kivy.uix.actionbar import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivymd.uix.transition import MDSlideTransition
import mysql.connector
from kivymd.uix.button import MDIconButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.core.window import Window
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from io import BytesIO

Window.size = (350, 600)


class BackgroundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundLayout())


class BackgroundLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source="assets/images/background1.jpg"))


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class ProfileButton(Image, Button):
    pass


class SearchBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class ProfileCard(FakeRectangularElevationBehavior, MDFloatLayout):
    pass


class SignButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


def icon(name):
    # Simula la función `icon`, retorna una cadena basada en el nombre del icono
    return f"[Icon: {name}]"


class TestApp(MDApp):
    tema = BooleanProperty(False)  # Asume que Light = False, Dark = True
    config_file = "settings.txt"  # Nombre del archivo de configuración

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = configparser.ConfigParser()
        self.config_file = "settings.txt"

    def build(self):
        try:
            self.theme_cls.theme_style = self.load_theme()
        except:
            self.theme_cls.theme_style = "Light" if not self.tema else "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.material_style = "M3"
        self.screen_manager = ScreenManager()
        self.previous_screen = ""
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.screen_manager.add_widget(LoginScreen(name="login_screen"))
        self.screen_manager.add_widget(main_screen.MainScreen(name="main_screen"))
        self.screen_manager.add_widget(ScoreScreen(name="score_screen"))
        self.screen_manager.add_widget(ConfigScreen(name="config_screen"))
        self.screen_manager.add_widget(ListScreen(name="list_screen"))
        self.screen_manager.add_widget(RegisterScreen(name="register_screen"))
        self.screen_manager.add_widget(ImageViewerScreen(name="image_viewer_screen"))
        self.screen_manager.add_widget(
            BackgroundViewerScreen(name="background_viewer_screen")
        )

        return Builder.load_file("app.kv")

    def get_icon(self, name):
        return icon(name)

    def load_theme(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as configfile:
                    for line in configfile:
                        if line.startswith("theme ="):
                            theme = line.split("=", 1)[1].strip()
                            print(
                                f"Tema cargado desde archivo de configuración: {theme}"
                            )
                            return theme
            except IOError as e:
                print(f"Error al leer archivo de configuración: {e}")
        else:
            print(
                "Archivo de configuración no encontrado. Usando configuración por defecto."
            )
            self.save_theme("Light")
            return "Light"

    def save_theme(self, theme):
        try:
            with open(self.config_file, "w") as configfile:
                configfile.write(f"theme = {theme}\n")
                print(f"Guardando tema en archivo de configuración: {theme}")
        except IOError as e:
            print(f"Error al guardar el archivo de configuración: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def set_theme(self):
        if self.active():
            self.theme_cls.theme_style = "Light"
            self.tema = False
            self.save_theme("Light")
        else:
            self.theme_cls.theme_style = "Dark"
            self.tema = True
            self.save_theme("Dark")

    def active(self):
        # Devuelve True si self.theme_cls.the_style es "Dark", de lo contrario False
        if self.theme_cls.theme_style == "Dark":
            return True
        return False

    def set_screen(self, screen_name):
        self.root.transition = MDSlideTransition(direction="left")
        if screen_name == "game_screen" and self.load_user_role():
            screen_name = "list_screen"
        self.root.current = screen_name

    def back_with_animation(self, screen_name):
        self.root.transition = MDSlideTransition(direction="right")
        self.root.current = screen_name

    def load_user_role(self):
        login_screen = LoginScreen()
        email = login_screen.return_userlog()
        print(email, " prof")

        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]
        try:
            db = mysql.connector.connect(
                host=host, user=user, password=password, database=dbname
            )
            cursor = db.cursor(dictionary=True)
            email = login_screen.return_userlog()
            query = "SELECT role FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result["role"] == "profesor":
                cursor.close()
                db.close()
                return True
            else:
                cursor.close()
                db.close()
                return False
        except Exception as e:
            toast(f"Revisa tu conexion {e}")
            return False

    def submit(self):
        ###### MYSQL #################
        mydb = mysql.connector.connect(
            host="localhost",  # ip
            user="id19372144_root",  # use-*r root
            passwd="AC--hOfTwsMwGK8v",  # password pass password
            # database="second_db",  # nombre base de datos
        )
        # cursor
        c = mydb.cursor()
        # comando
        sql_command = """INSERT INTO users (name, email)
                VALUES (%s, %s)"""
        values = (self.root.ids.dbword_input.text,)
        # ejecutar
        c.execute(sql_command, values)
        # mensajito
        self.root.ids.dbword_label.text = f"{self.root.ids.word_input.text}"
        # clear input
        self.root.ids.dbword_input.text = ""

        mydb.commit()
        mydb.close()

    def highlight_tab(self, screen_name, tab_index):
        screen = self.screen_manager.get_screen(screen_name)
        bot_nav = screen.ids.bot_nav
        bot_nav.switch_tab(tab_index)

    def show_records(self):
        ###### MYSQL #################
        mydb = mysql.connector.connect(
            host="localhost",  # ip
            user="tesis",  # user root
            passwd="4533",  # password pass password
            database="second_db",  # nombre base de datos
        )
        # cursor
        c = mydb.cursor()

        # mostrar

        c.execute("SELECT * FROM users")
        records = c.fetchall()
        word = ""

        # loop thru records
        for record in records:
            word = f"{word}\n{record[0]}"
            self.root.ids.dbword_label.text = f"{word}"
        # commit
        mydb.commit()
        mydb.close()

    def switch_action(self, switch_id, is_active):
        if switch_id == "tema":
            if is_active:
                print("El interruptor 'tema' está activado")
                self.set_theme("Light", "Blue", "Blue")
            else:
                print("El interruptor 'tema' está desactivado")
                self.set_theme("Dark", "Blue", "Blue")
        # Agregar más casos para otros interruptores si es necesario

    def change_background(self, background_path):
        # Cambiar el fondo de la aplicación
        rect = self.root.ids.background_rectangle.canvas.get_group("rectangle")[0]
        print(background_path)
        rect.source = background_path


if __name__ == "__main__":
    LabelBase.register(
        name="LuckiestGuy", fn_regular="assets/fonts/LuckiestGuy-Regular.ttf"
    )
    TestApp().run()


# Ejecuta la aplicación
