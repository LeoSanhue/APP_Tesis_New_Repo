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
import mysql.connector
from datetime import datetime
from kivymd.toast import toast
import configparser


def icon(name):
    # Simula la función `icon`, retorna una cadena basada en el nombre del icono
    return f"[Icon: {name}]"


class LoginScreen(Screen):
    def save_userlog(valor, estado):
        # Guardar la variable en el diccionario de estado
        userlog[0] = valor

    def get_icon(self, name):
        return icon(name)

    def return_userlog(estado):
        # Retornar la variable guardada del diccionario de estado
        return userlog[0]

    def login(self):
        app = MDApp.get_running_app()
        input_email = self.ids.username_field.text
        input_password = self.ids.password_field.text

        # Verificar si los campos están vacíos
        if not input_email or not input_password:
            toast("Por favor, complete todos los campos.")
            return

        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]
        try:
            db = mysql.connector.connect(
                host=str(host),
                user=str(user),
                password=str(password),
                database=str(dbname),
            )
            cursor = db.cursor()
            query = (
                "SELECT count(*) FROM users where email='"
                + str(input_email)
                + "* and password ="
                + str(input_password)
                + "'"
            )
            cursor.execute(query)
            data = cursor.fetchone()

            # Modifica tu consulta SQL para seleccionar el usuario y la contraseña
            query = (
                "SELECT email, password FROM users WHERE email='"
                + str(input_email)
                + "' AND password ='"
                + str(input_password)
                + "'"
            )
            cursor.execute(query)

            # Obtén los resultados de la consulta
            result = cursor.fetchone()

            # Verifica si se encontró un usuario y contraseña correspondientes

            if result:  # Si se encontraron resultados
                email_from_db = result[0]
                password_from_db = result[1]
                for record in data:
                    print("Usuario:", input_email, "DBusuario", email_from_db)
                    print("Contraseña:", input_password, "DBPASS", password_from_db)
                    print(record)
                if input_email == email_from_db and input_password == password_from_db:
                    toast("Login y passwords\n son correctos")
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    update_query = (
                        "UPDATE users SET last_login='"
                        + now
                        + "' WHERE email='"
                        + email_from_db
                        + "' AND password ='"
                        + password_from_db
                        + "'"
                    )
                    cursor.execute(update_query)
                    db.commit()

                    db.close()
                    LoginScreen.save_userlog(email_from_db, userlog)
                    print(userlog, " login")
                    app.set_screen("main_screen")
                    self.manager.current = "main_screen"
                else:
                    toast("Contraseña \nincorrecta")
            else:
                # No se encontró un usuario con esa dirección de correo electrónico
                toast("Correo electrónico o \nContraseña incorrecta")
        except Exception as e:
            toast(f"Revisa tu conexion {e}")
            return

    def show_password_incorrect_modal(self):
        modal = ModalView(size_hint=(0.5, 0.3))
        content = [
            MDLabel(
                text="Contraseña incorrecta. \n Inténtalo de nuevo.", halign="center"
            )
        ]
        close_button = MDFlatButton(text="", on_release=modal.dismiss)

        modal.add_widget(content[0])  # Accede al primer elemento de la lista
        modal.add_widget(close_button)

        modal.open()

    def register(self):
        app = MDApp.get_running_app()
        app.set_screen("register_screen")


userlog = {}
