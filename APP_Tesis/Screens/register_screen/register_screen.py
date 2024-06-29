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
from kivymd.toast import toast
from kivy.clock import Clock
import re
import mysql.connector
import configparser
from datetime import datetime

# Define la cadena KV con las pantallas de inicio de sesión y la pantalla principal
# GLOBAL##########################################
global user
global pw
global email
global apodo
user = "username"
pw = "password"
email = "usermail"
apodo = "leo"
# CAMBIAR EN CASO DE ##############################


class RegisterScreen(Screen):

    def check_password_match(self):
        repassword = self.ids.repassword_field.text
        password = self.ids.password_field.text
        if password == repassword:
            self.ids.repassword_field.icon_left = "check"
        else:
            self.ids.repassword_field.icon_left = "close"

    def register(self):
        offensive_words = [
            "ofensiva1",
            "ofensiva2",
            "ofensiva3",
        ]  # Lista de palabras ofensivas

        username = self.ids.username_field.text
        password = self.ids.password_field.text
        repassword = self.ids.repassword_field.text
        usermail = self.ids.email_field.text

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not (
            8 <= len(username) <= 20
            and 8 <= len(password) <= 12
            and any(c.isdigit() for c in password)
            and any(not c.isalnum() for c in password)
            and re.match(email_regex, usermail)
            and password == repassword
            and not any(
                offensive_word in username for offensive_word in offensive_words
            )
        ):
            self.show_invalid_criteria_modal()
            return

        config = configparser.ConfigParser()
        config.read("config.ini")
        if "mysql" not in config:
            toast("Configuración MySQL no encontrada")
            return
        if not all(
            key in config["mysql"] for key in ["host", "user", "password", "db"]
        ):
            toast("Configuración MySQL incompleta")
            return

        host = config["mysql"]["host"]
        db_user = config["mysql"]["user"]
        db_password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]
        try:

            db = mysql.connector.connect(
                host=host, user=db_user, password=db_password, database=dbname
            )
            cursor = db.cursor()

            # Verificar si el correo electrónico ya está registrado
            email_query = "SELECT count(*) FROM users WHERE email=%s"
            cursor.execute(email_query, (usermail,))
            email_exists = cursor.fetchone()[0]

            # Verificar si el nombre de usuario ya está registrado
            username_query = "SELECT count(*) FROM users WHERE username=%s"
            cursor.execute(username_query, (username,))
            username_exists = cursor.fetchone()[0]

            if email_exists > 0:
                toast("Correo electrónico ya registrado")
                db.close()
                return

            if username_exists > 0:
                toast("Nombre de usuario ya registrado")
                db.close()
                return
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Insertar nuevo usuario
            sql_command = "INSERT INTO users (username, password, email, profile_picture_path, institution, max_score, growth_rate, max_streak, last_login) VALUES (%s, %s, %s, 'assets/images/1.png', 'Universidad del Biobio',0,0,0,%s)"
            values = (username, password, usermail, now)
            cursor.execute(sql_command, values)
            db.commit()
            db.close()

            toast("Registro Exitoso")
            self.show_register_success_modal()

            global user, pw, email
            user = username
            pw = password
            email = usermail
        except mysql.connector.Error as db_error:
            toast(f"Error de conexión a la base de datos: {db_error}")
        except Exception as e:
            toast(f"Error: {e}")

    def show_invalid_criteria_modal(self):
        modal = MDDialog(
            title="Intenta otra vez",
            size_hint=(0.5, 0.3),
            auto_dismiss=True,
            text="La contraseña debe contener al menos un número y un signo y ambos campos entre 8 y 12 caracteres o es ofensivo.",
            size_hint_y=None,
        )
        modal.open()

    def show_register_success_modal(self):
        modal = MDDialog(
            title="Listo!",
            size_hint=(0.5, 0.3),
            auto_dismiss=True,
            text="Registro Exitoso",
            radius=[20, 7, 20, 7],
            size_hint_y=None,
        )
        modal.open()
