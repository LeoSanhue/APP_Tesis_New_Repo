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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
from io import BytesIO
import tempfile
import os


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

        def obtener_id_usuario_por_email(email):
            # Leer la configuración de la base de datos desde el archivo config.ini
            config = configparser.ConfigParser()
            config.read("config.ini")
            host = config["mysql"]["host"]
            user = config["mysql"]["user"]
            password = config["mysql"]["password"]
            dbname = config["mysql"]["db"]

            try:
                # Conectar a la base de datos
                db = mysql.connector.connect(
                    host=host, user=user, password=password, database=dbname
                )
                cursor = db.cursor(dictionary=True)

                # Consulta para obtener el ID del usuario por email
                query = "SELECT id FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                cursor.close()
                db.close()

                # Devolver el ID del usuario si se encuentra
                if result:
                    return result["id"]
                else:
                    return None

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None

        def obtener_puntajes_usuario(user_id):
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
            except:
                print("error")
            cursor = db.cursor(dictionary=True)
            # Obtener los puntajes del último mes para el usuario
            query = """
            SELECT date, score 
            FROM scores 
            WHERE user_id = %s AND date >= %s
            ORDER BY date
            """
            hace_un_mes = datetime.now() - timedelta(days=30)
            cursor.execute(query, (user_id, hace_un_mes))
            puntajes = cursor.fetchall()
            cursor.close()
            return puntajes

        def obtener_mensajes_usuario(user_id):
            cursor = db.cursor(dictionary=True)
            # Obtener la fecha de hace un mes
            hace_un_mes = datetime.now() - timedelta(days=30)
            login_screen = LoginScreen()
            email = login_screen.return_userlog()
            # Consultar los mensajes del último mes para el usuario con su frecuencia
            # query = "SELECT id FROM users WHERE email = %s"
            # cursor.execute(query, (email,))
            # user_id = cursor.fetchall()
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

        def truncate_at_last_punctuation(text):
            """Truncates the text at the last punctuation mark (.¡?)."""
            match = re.search(
                r"[.!?][^.!?]*$", text[::-1]
            )  # Search from the end of the text
            if match:
                return text[: -match.start()]  # Truncate at the start of the match
            return text

        def remove_last_line(text):
            """Removes the last line from the given text."""
            lines = text.split("\n")
            if len(lines) > 1:
                return "\n".join(lines[:-1]).strip()
            return text.strip()

        def save_pdf(report_text, puntajes):
            file_path = "report.pdf"

            # Create a buffer to collect PDF elements
            buffer = BytesIO()

            # Create a PDF document object using SimpleDocTemplate
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()

            # Add a title to the document
            title = Paragraph("Informe de Rendimiento", styles["Title"])
            elements = [title]

            # Add the report text
            report_paragraphs = [
                Paragraph(line, styles["Normal"]) for line in report_text.split("\n")
            ]
            elements.extend(report_paragraphs)

            # Generate the plot
            dates = [p["date"].strftime("%Y-%m-%d") for p in puntajes]
            scores = [p["score"] for p in puntajes]

            plt.figure(figsize=(6, 4))
            plt.plot(dates, scores, marker="o", linestyle="-", color="b")
            plt.title("Puntajes de los últimos 30 días")
            plt.xlabel("Fecha")
            plt.ylabel("Puntaje")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save plot to a temporary file
            with tempfile.NamedTemporaryFile(
                suffix=".png", delete=False
            ) as temp_plot_file:
                plt.savefig(temp_plot_file.name, format="png")
                temp_plot_file.close()

                # Add the plot to the PDF document
                plot_image = Image(temp_plot_file.name, width=400, height=200)
                elements.append(plot_image)

            # Build the PDF document
            doc.build(elements)

            # Save the buffer to a file
            with open(file_path, "wb") as f:
                f.write(buffer.getvalue())

            # Delete the temporary plot file after using it
            if temp_plot_file.name:
                os.remove(temp_plot_file.name)

            toast(f"Informe guardado en {file_path}")
            return file_path

        def send_email(email_address, file_path):
            ######## MODIFICAR AL IMPLEMENTAR ESTO SOLO MANDA A MI CORREO DE PRUEBAS #######################
            sender_email = ""
            thingy = "ajol gypf ryut uedv"
            subject = "Informe de Rendimiento"
            body = "Adjunto encontrarás tu informe de rendimiento."
            email_address = ""
            ##################################################S
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email_address
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            attachment = open(file_path, "rb")
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {file_path}")

            msg.attach(part)

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, thingy)
            text = msg.as_string()
            server.sendmail(sender_email, email_address, text)
            server.quit()
            toast("Correo enviado exitosamente")

        # Your Hugging Face API key
        api_key = "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"

        login_screen = LoginScreen()
        email = login_screen.return_userlog()  # Utiliza un correo válido para pruebas
        user_id = obtener_id_usuario_por_email(email)
        mensajes_usuario = obtener_mensajes_usuario(user_id)
        puntajes_usuario = obtener_puntajes_usuario(user_id)

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
                # mensaje_limpio = truncate_at_last_punctuation(mensaje_limpio)
                # Guardar el PDF
                # Enviar el PDF por correo electrónico
                file_path = save_pdf(mensaje_limpio, puntajes_usuario)
                send_email(email, file_path)
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
