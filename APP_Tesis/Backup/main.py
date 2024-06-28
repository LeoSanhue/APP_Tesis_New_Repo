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

# from kivymd.uix.divider import MDDivider

import random
import time
import re
from kivymd.uix.button import MDRaisedButton


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


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class LoginScreen(Screen):
    def login(self):
        # Aquí implementa la lógica de inicio de sesión
        # Por ahora, simplemente verifica si el nombre de usuario y la contraseña son "admin"
        # if (
        #    self.ids.username_field.text == "admin"
        #    and self.ids.password_field.text == "admin"
        # ):
        # Si el inicio de sesión es correcto, navega a la pantalla principal
        self.manager.current = "main_screen"

    #  else:
    # Si la contraseña es incorrecta, mostrar un modal
    #     self.show_password_incorrect_modal()

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
        self.manager.current = "register_screen"


class RegisterScreen(Screen):

    def check_password_match(self):
        # print("tick")
        repassword = self.ids.repassword_field.text
        password = self.ids.password_field.text
        if password == repassword:
            # Aquí debes poner la contraseña que deseas comparar
            self.ids.repassword_field.icon_left = "check"
            # print("es igual", password, "a", repassword)
            return
        else:
            self.ids.repassword_field.icon_left = "close"
            # print("no es igual:", password, "a", repassword)
            return

    def register(self):
        offensive_words = [
            "ofensiva1",
            "ofensiva2",
            "ofensiva3",
        ]  # Lista de palabras ofensivas
        # Obtiene los valores de usuario y contraseña
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        repassword = self.ids.repassword_field.text
        usermail = self.ids.email_field.text

        # Expresión regular para validar el formato del correo electrónico
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # Valida los criterios de longitud y Valida los criterios de composición
        if not (
            8 <= len(username) <= 12
            and 8 <= len(password) <= 12
            and any(c.isdigit() for c in password)
            and any(not c.isalnum() for c in password)
            and re.match(email_regex, usermail)
            and password == repassword
            and any(
                offensive_word in username for offensive_word in self.offensive_words
            )
        ):
            self.show_invalid_criteria_modal()
            return
        # Aquí implementa la lógica de registro
        # Por ahora, simplemente muestra un modal de registro exitoso
        self.show_register_success_modal()
        print("Usuario:", username)
        print("Contraseña:", password)
        print("Correo electrónico:", usermail)

        # GLOBAL##########################################
        global user
        global pw
        global email
        global apodo
        user = username
        pw = password
        email = usermail
        # CAMBIAR EN CASO DE ##############################

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

        # Otros métodos aquí...


class UserProfileScreen(Screen):
    def on_enter(self):
        #      # Actualiza el texto de los campos de edición con la información del perfil de usuario
        self.ids.profile_user_name.text = (
            user  # Asigna el nombre de usuario preexistente
        )
        self.ids.profile_user_email.text = (
            email  # Asigna el correo electrónico preexistente
        )

    def go_back_to_main_screen(self):
        self.manager.current = "main_screen"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.time_limit = 30  # Tiempo límite en segundos
        self.points = 0
        self.start_time = time.time()
        Clock.schedule_once(
            self.next_exercise, 0
        )  # Retrasar la ejecución de next_exercise

    def generate_exercise(self):
        operations = ["+", "-", "*", "/"]
        operation = random.choice(operations)
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)

        # Evitar división por cero
        while operation == "/" and num2 == 0:
            num2 = random.randint(1, 20)

        exercise = f"{num1} {operation} {num2}"
        correct_result = eval(exercise)
        return exercise, correct_result

    def check_answer(self):
        user_input = self.ids.user_input.text.strip()
        if not user_input:
            return

        try:
            user_result = float(user_input)
        except ValueError:
            print("Por favor, ingresa un número válido.")
            return

        exercise_text = self.ids.exercise_label.text
        num1, operation, num2 = exercise_text.split()
        correct_result = eval(f"{num1} {operation} {num2}")

        if user_result == correct_result:
            self.points += 1
            print("¡Respuesta correcta!")
        else:
            print("Respuesta incorrecta.")

        self.ids.user_input.text = ""  # Limpiar el campo de entrada
        self.next_exercise(None)  # Pasar None como parámetro

    def next_exercise(self, dt):
        if time.time() - self.start_time < self.time_limit:
            exercise, _ = self.generate_exercise()
            self.ids.exercise_label.text = exercise
        else:
            print("Tiempo terminado. Puntos:", self.points)
            self.show_score_modal()

    def show_score_modal(self):
        # Lógica para mostrar un modal con el puntaje
        pass


class MainScreen(Screen):

    def UserProfile(self):
        self.previous_screen = self.manager.current
        self.manager.current = "user_screen"

    def Back(self):
        self.manager.current = self.previous_screen

    def on_button_press_1(self):
        print("¡El botón ha sido presionado en la pantalla scr 1!")

    def on_button_press_2(self):
        print("¡El botón ha sido presionado en la pantalla scr 2!")


class ConfigScreen(Screen):
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


class TestApp(MDApp):

    def build(self):
        self.set_theme("Dark", "LightGreen", "LightGreen")
        self.theme_cls.primary_hue = "A200"
        self.screen_manager = ScreenManager()
        self.previous_screen = ""
        # Agrega la pantalla de inicio de sesión y la pantalla principal al administrador de pantallas
        self.screen_manager.add_widget(LoginScreen())
        self.screen_manager.add_widget(MainScreen())
        return Builder.load_file("app.kv")

    def set_theme(self, theme, primary, accent):
        self.theme_cls.theme_style = theme
        self.theme_cls.primary_palette = primary
        self.theme_cls.accent_palette = accent


TestApp().run()
