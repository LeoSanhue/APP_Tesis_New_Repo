from kivy.uix.popup import Popup
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
import random
import time
from kivymd.uix.button import MDRaisedButton
from kivy.uix.modalview import ModalView
from kivymd.uix.dialog import MDDialog
from kivy.uix.accordion import ListProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.metrics import dp  # Importa dp desde kivy.metrics
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, BooleanProperty
import mysql.connector
import configparser
from datetime import datetime
from Screens.login_screen.login_screen import LoginScreen
import re
import traceback
from kivymd.uix.list import OneLineListItem
from kivymd.uix.list import TwoLineListItem


class ListScreen(Screen):

    def on_enter(self):
        self.load_students()

    def load_students(self):
        try:

            login_screen = LoginScreen()
            email = login_screen.return_userlog()
            # Supongamos que 'profesor_id' está guardado en app como un atributo.

            config = configparser.ConfigParser()
            config.read("config.ini")
            host = config["mysql"]["host"]
            user = config["mysql"]["user"]
            password = config["mysql"]["password"]
            dbname = config["mysql"]["db"]
            db = mysql.connector.connect(
                host=host, user=user, password=password, database=dbname
            )
            cursor = db.cursor(dictionary=True)
            email = login_screen.return_userlog()
            query = "SELECT curso FROM users WHERE email = %s"
            cursor.execute(query, (email,))

            # Primero, obtenemos el curso del profesor logueado
            curso = cursor.fetchone()["curso"]

            # Ahora obtenemos los estudiantes del mismo curso
            query = """
                SELECT u.username, mc.message, mc.count 
                FROM users u
                LEFT JOIN message_counts mc ON u.id = mc.user_id
                WHERE u.role = 'estudiante' AND u.curso = %s
                AND mc.count = (
                    SELECT MAX(mc_inner.count) 
                    FROM message_counts mc_inner 
                    WHERE mc_inner.user_id = u.id
                )
            """
            cursor.execute(query, (curso,))
            students = cursor.fetchall()
            db.close()

            students_list = self.ids.students_list
            students_list.clear_widgets()

            for student in students:
                primary_text = student["username"]
                secondary_text = f"{student['message']} ({student['count']})"
                students_list.add_widget(
                    TwoLineListItem(text=primary_text, secondary_text=secondary_text)
                )

        except mysql.connector.Error as e:
            print(f"Error de MySQL: {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")
