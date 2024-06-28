from kivy.uix.behaviors.touchripple import Ellipse
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
from Screens.login_screen.login_screen import LoginScreen
from kivy.metrics import dp  # Importa dp desde kivy.metrics
import requests
import mysql.connector
from datetime import datetime, timedelta
import configparser
import re
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.uix.image import Image
from kivy.properties import StringProperty


class UserProfileScreen(Screen):
    dialog = None

    def on_enter(self):
        self.load_user_data()

    def load_user_data(self):
        login_screen = LoginScreen()
        email = login_screen.return_userlog()
        print(email, " user")

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
            query = "SELECT * FROM users WHERE email=%s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                self.ids.profile_user_name.text = result["username"]
                # self.ids.profile_user_email.text = result["email"]
                self.ids.profile_institution.text = result["institution"]
                self.ids.highest_score.text = str(result["max_score"])
                self.ids.growth_rate.text = str(result["growth_rate"])
                self.ids.longest_streak.text = str(result["max_streak"])

                # Update the Ellipse's source property
                profile_picture_widget = self.ids.profile_picture
                for instruction in profile_picture_widget.canvas.before.children:
                    if isinstance(instruction, Ellipse):
                        instruction.source = result["profile_picture_path"]
                        break

            cursor.close()
            db.close()
        except Exception as e:
            toast(f"Revisa tu conexion {e}")
        return

    def update_user_data(self, user_data):
        # Implementar lógica para actualizar datos del usuario en la base de datos
        pass

    def save_profile_picture(self, image_path):
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
            cursor = db.cursor()
            query = "UPDATE users SET profile_picture_path=%s WHERE username=%s"
            cursor.execute(query, (image_path, user))
            db.commit()

            cursor.close()
            db.close()
        except Exception as e:
            toast(f"Revisa tu conexion {e}")
        return

    def prompIA(self):

        # Conexión a la base de datos MySQL
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]
        db = mysql.connector.connect(
            host=host, user=user, password=password, database=dbname
        )

        def obtener_mensajes_usuario(user_id):
            cursor = db.cursor(dictionary=True)
            # Obtener la fecha de hace un mes
            hace_un_mes = datetime.now() - timedelta(days=30)

            # Consultar los mensajes del último mes para el usuario con su frecuencia
            query = """
            SELECT message, COUNT(message) as count 
            FROM scores 
            WHERE user_id = %s AND date >= %s
            GROUP BY message
            """
            cursor.execute(query, (user_id, hace_un_mes))
            mensajes = cursor.fetchall()
            cursor.close()
            return mensajes

        def generate_message(prompt, api_key):
            API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
            headers = {"Authorization": f"Bearer {api_key}"}

            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 251,  # Limit the length of the generated message
                    "num_return_sequences": 1,  # Number of sequences to generate
                    "temperature": 0.7,  # Creativity of the response
                },
            }

            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                generated_message = response.json()[0]["generated_text"]
                return generated_message
            else:
                return f"Error: {response.status_code} - {response.json()}"

        def remove_first_line(text):
            """Removes the first line from the given text."""
            lines = text.split("\n")
            if len(lines) > 1:
                return "\n".join(lines[1:]).strip()
            return text.strip()

        def truncate_at_first_punctuation(text):
            """Truncates the text at the first punctuation mark (.¡?)."""
            match = re.search(r"[.!?]", text)
            if match:
                return text[: match.end()]
            return text

        def remove_last_line(text):
            """Removes the last line from the given text."""
            lines = text.split("\n")
            if len(lines) > 1:
                return "\n".join(lines[:-1]).strip()
            return text.strip()

        # Your Hugging Face API key
        api_key = "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"

        # Ejemplo de uso
        user_id = 1  # ID del usuario para el que quieres generar el mensaje
        mensajes_usuario = obtener_mensajes_usuario(user_id)

        if mensajes_usuario:
            mensaje_mas_frecuente = max(mensajes_usuario, key=lambda x: x["count"])
            mensaje = mensaje_mas_frecuente["message"]
            count = mensaje_mas_frecuente["count"]

            # Construir el prompt basado en el tipo de mensaje
            if mensaje == "Sabe operar":
                prompt = f"Felicita al estudiante por su excelente desempeño en matemáticas. Escribe en español. termina el mensaje antes de los 200 caracteres puedes rellenar con espacios cuando termines tu idea y no menciones los caracteres totales"
            elif mensaje == "Regular suma":
                prompt = f"Anima al estudiante a mejorar en sumas ha tenido pobre rendimiento. Motívalo a seguir mejorando y no le des ejercicios. Escribe en español. termina el mensaje antes de los 200 caracteres puedes rellenar con espacios cuando termines tu idea y no menciones los caracteres totales"
            elif mensaje == "Regular resta":
                prompt = f"Anima al estudiante a mejorar en restas. Motívalo a seguir mejorando y no le des ejercicios. Escribe en español. termina el mensaje antes de los 200 caracteres puedes rellenar con espacios cuando termines tu idea y no menciones los caracteres totales"
            elif mensaje == "Necesita mejorar":
                prompt = f"Motiva al estudiante a mejorar en matemáticas. Anímalo a continuar trabajando duro para mejorar. Escribe en español. termina el mensaje antes de los 200 caracteres puedes rellenar con espacios cuando termines tu idea y no menciones los caracteres totales"

            # Generar el mensaje personalizado
            mensaje_personalizado = generate_message(prompt, api_key)
            if mensaje_personalizado:
                mensaje_limpio = remove_first_line(mensaje_personalizado)
                mensaje_limpio = remove_last_line(mensaje_limpio)
                mensaje_truncado = truncate_at_first_punctuation(mensaje_limpio)

                return mensaje_limpio
            else:
                print("No se pudo generar el mensaje personalizado.")
        else:
            print("No se encontraron mensajes para este usuario en el último mes.")

    def show_confirmation_dialog(self):
        app = MDApp.get_running_app()
        if not self.dialog:
            self.dialog = MDDialog(
                title="Tu rendimiento este mes ha sido!!",
                text=self.prompIA(),
                buttons=[
                    MDFlatButton(
                        text="Continuar",
                        theme_text_color="Custom",
                        text_color=app.theme_cls.primary_color,
                        on_release=lambda instance: self.dismiss_modal(),
                    ),
                ],
            )
        self.dialog.open()

    def dismiss_modal(self):
        if self.dialog:
            self.dialog.dismiss()  # Dismiss the popup


class Content(BoxLayout):
    pass
