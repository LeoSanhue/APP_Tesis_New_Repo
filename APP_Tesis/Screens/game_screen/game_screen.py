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


class ScoreScreen(Screen):
    points = NumericProperty(0)  # Define el atributo points
    streak = NumericProperty(0)  # Define el atributo streak
    new_record_streak = BooleanProperty(False)  # Define el atributo new_record_streak
    new_record_score = BooleanProperty(False)  # Define el atributo new_record_score

    def __init__(
        self,
        points=0,
        streak=0,
        new_record_streak=False,
        new_record_score=False,
        **kwargs,
    ):
        super(ScoreScreen, self).__init__(**kwargs)
        self.points = points  # Establece el puntaje
        self.streak = streak  # Establece la racha
        self.new_record_streak = (
            new_record_streak  # Establece si es un nuevo récord de racha
        )
        self.new_record_score = (
            new_record_score  # Establece si es un nuevo récord de puntaje
        )


class SignButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


class StartButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


class SuperLabel(MDLabel):
    bg_color = ListProperty([1, 1, 1, 1])


class GameScreen(Screen):
    EASY_MODE_MULTIPLIER = 1
    MEDIUM_MODE_MULTIPLIER = 2
    HARD_MODE_MULTIPLIER = 4

    global difficulty
    global difficulty_multiplier
    difficulty = "a"
    difficulty_multiplier = 0

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.difficulty_multiplier = self.EASY_MODE_MULTIPLIER
        self.difficulty_mode = "easy"
        self.time_limit = 15  # Tiempo límite en segundos
        self.points = 0
        self.start_time = time.time()
        self.current_streak = 0
        self.exercise_log = []
        self.max_streak = 0

        Clock.schedule_once(
            self.next_exercise, 0
        )  # Retrasar la ejecución de next_exercise

    def get_user_id(self, email):
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]
        print(email, " jeugo id")

        db = mysql.connector.connect(
            host=host, user=user, password=password, database=dbname
        )
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0] if result else None

    def set_difficulty_mode(self):
        if self.difficulty == "easy":  # Cambia self.difficulty a difficulty
            self.difficulty_multiplier = self.EASY_MODE_MULTIPLIER
        elif self.difficulty == "medium":
            self.difficulty_multiplier = self.MEDIUM_MODE_MULTIPLIER
        elif self.difficulty == "hard":
            self.difficulty_multiplier = self.HARD_MODE_MULTIPLIER
        self.difficulty_mode = (
            self.difficulty
        )  # Cambia self.difficulty_mode a difficulty
        print(f"modo:", self.difficulty_mode)

    def calculate_score(self, is_correct):
        if is_correct:
            return self.difficulty_mode
        else:
            return 0

    def generate_exercise(self):
        num_digits = (
            1
            if self.difficulty_multiplier == self.EASY_MODE_MULTIPLIER
            else 2 if self.difficulty_multiplier == self.MEDIUM_MODE_MULTIPLIER else 2
        )
        operations = ["+", "-"]

        correct_result = None
        while correct_result is None or (
            (
                self.difficulty_multiplier == self.MEDIUM_MODE_MULTIPLIER
                and abs(correct_result) >= 100
            )
            or (
                self.difficulty_multiplier > self.MEDIUM_MODE_MULTIPLIER
                and abs(correct_result) >= 200
            )
        ):
            num1 = random.randint(-(10**num_digits), 10**num_digits - 1)
            num2 = random.randint(1, 10**num_digits - 1)

            #####FACIL###########

            if self.difficulty_multiplier == self.EASY_MODE_MULTIPLIER:
                num1 = random.randint(0, 10**num_digits - 1)
                num2 = random.randint(0, 10**num_digits - 1)
                operations = ["+", "-"]
                operation = random.choice(operations)
                exercise = f"{num1} {operation} {num2}"
            #####MEDIO###########

            if self.difficulty_multiplier == self.MEDIUM_MODE_MULTIPLIER:
                compound_operations = ["{}-(-{})", "{}+(-{})", "{}+{}", "{}-{}"]
                compound_operation = random.choice(compound_operations)
                exercise = compound_operation.format(num1, num2)
            #####DIFICL###########

            else:
                compound_operations = [
                    "{}-(-{})",
                    "{}+(-{})",
                    "{}+{}",
                    "{}-{}",
                    "-({})+{}",
                    "-({})-{}",
                    "-({})+(-{})",
                    "-({})-(-{})",
                ]
                compound_operation = random.choice(compound_operations)
                exercise = compound_operation.format(num1, num2)

            correct_result = eval(exercise)

        return exercise, correct_result

    def show_score_screen(self):
        new_record_streak = False
        new_record_score = False  # Verificar si ya existe una instancia de ScoreScreen
        score_screen = None
        for screen in self.manager.screens:
            if isinstance(screen, ScoreScreen):
                score_screen = screen
                break

        # Si no existe, crear una nueva instancia
        if not score_screen:
            login_screen = LoginScreen()
            email = login_screen.return_userlog()
            user_id = self.get_user_id(email)

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
            cursor.execute(
                "SELECT max_streak, max_score FROM users WHERE id = %s", (user_id,)
            )
            result = cursor.fetchone()
            previous_max_streak = result[0] if result else 0

            cursor.execute("SELECT max_score FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            previous_max_score = result[0] if result else 0
            cursor.close()
            db.close()

            if self.max_streak > previous_max_streak:
                new_record_streak = True
            if self.points > previous_max_score:
                new_record_score = True
            score_screen = ScoreScreen(
                points=self.points,
                streak=self.max_streak,
                new_record_streak=new_record_streak,
                new_record_score=new_record_score,
            )
            self.manager.add_widget(score_screen)

        # Actualizar los datos de la instancia existente o nueva
        if score_screen:
            score_screen.points = self.points
            score_screen.streak = self.max_streak
            score_screen.new_record_streak = new_record_streak
            score_screen.new_record_score = new_record_score
        # log
        self.print_exercise_log()

        # Imprimir el mensaje correspondiente
        self.print_final_message()
        self.manager.current = "score_screen"

    def print_final_message(self):
        # Tabla de mensajes
        messages = [
            {"suma": False, "resta": False, "mensaje": "Necesita mejorar"},
            {"suma": True, "resta": False, "mensaje": "Regular resta"},
            {"suma": False, "resta": True, "mensaje": "Regular suma"},
            {"suma": True, "resta": True, "mensaje": "Sabe operar"},
        ]

        # Inicializar contadores
        suma_correcta = 0
        resta_correcta = 0
        suma_total = 0
        resta_total = 0

        # Contar resultados correctos para cada tipo de operación
        if hasattr(self, "exercise_log"):
            for entry in self.exercise_log:
                if entry["type"] == "suma":
                    suma_total += 1
                    if entry["correct"]:
                        suma_correcta += 1
                elif entry["type"] == "resta":
                    resta_total += 1
                    if entry["correct"]:
                        resta_correcta += 1

        # Calcular porcentajes de respuestas correctas
        suma_percentage = (suma_correcta / suma_total) * 100 if suma_total > 0 else 0
        resta_percentage = (
            (resta_correcta / resta_total) * 100 if resta_total > 0 else 0
        )

        # Determinar el mensaje basado en los porcentajes
        if suma_percentage >= 70 and resta_percentage >= 70:
            final_message = "Sabe operar"
        elif suma_percentage < 20 and resta_percentage < 20:
            final_message = "Necesita mejorar"
        else:
            suma_fallada = suma_total - suma_correcta
            resta_fallada = resta_total - resta_correcta

            if suma_fallada > resta_fallada:
                final_message = "Regular suma"
            elif resta_fallada > suma_fallada:
                final_message = "Regular resta"
            else:
                # Determinar el mensaje basado en la tabla
                for criteria in messages:
                    if criteria["suma"] == (suma_correcta > 0) and criteria[
                        "resta"
                    ] == (resta_correcta > 0):
                        final_message = criteria["mensaje"]
                        break

        # Imprimir el mensaje final
        print(final_message)

        # Contar y almacenar los mensajes
        return final_message

    def save_score(self, score):
        login_screen = LoginScreen()
        email = login_screen.return_userlog()
        print(email, " juego")
        message = self.print_final_message()
        print(message)
        config = configparser.ConfigParser()
        config.read("config.ini")
        host = config["mysql"]["host"]
        user = config["mysql"]["user"]
        password = config["mysql"]["password"]
        dbname = config["mysql"]["db"]

        user_id = self.get_user_id(email)
        if user_id is None:
            print(f"No se encontró el usuario con el email: {email}")
            return
        try:
            db = mysql.connector.connect(
                host=host, user=user, password=password, database=dbname
            )
            cursor = db.cursor()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                INSERT INTO scores (user_id, score, date, email, message)
                VALUES (%s, %s, %s, %s,%s)
                """,
                (user_id, score, date, email, message),
            )
            # Guardar la puntuación
            cursor.execute(
                "SELECT count FROM message_counts WHERE message = %s AND user_id = %s",
                (message, user_id),
            )
            result = cursor.fetchone()

            if result:
                # Si el mensaje ya existe, incrementar el contador
                new_count = result[0] + 1
                cursor.execute(
                    "UPDATE message_counts SET count = %s WHERE message = %s AND user_id = %s",
                    (new_count, message, user_id),
                )
            else:
                # Si el mensaje no existe, insertarlo con un contador de 1
                cursor.execute(
                    "INSERT INTO message_counts (user_id, message, count) VALUES (%s, %s, %s)",
                    (user_id, message, 1),
                )

            result = cursor.fetchone()
            previous_max_streak = result[0] if result else 0
            previous_max_score = result[1] if result else 0

            if self.max_streak > previous_max_streak:
                cursor.execute(
                    "UPDATE users SET max_streak = %s WHERE id = %s",
                    (self.max_streak, user_id),
                )

            if score > previous_max_score:
                cursor.execute(
                    "UPDATE users SET max_score = %s WHERE id = %s",
                    (score, user_id),
                )

            db.commit()
            cursor.close()
            db.close()
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            traceback.print_exc()
        except Exception as e:
            print(f"Unexpected error: {e}")
            traceback.print_exc()

    def print_exercise_log(self):
        if hasattr(self, "exercise_log"):
            for entry in self.exercise_log:
                print(entry)
        else:
            print("No hay ejercicios en el log.")

    def show_score_modal(self):
        # Detener el temporizador antes de mostrar el diálogo
        Clock.unschedule(self.update_timer)

        # Crear el contenido del popup
        box = BoxLayout(orientation="vertical")
        label = Label(text=f"Tu puntaje final es: {self.points}")
        # close_button = Button(text="Cerrar")
        # close_button.bind(on_release=self.dismiss_score_modal)

        box.add_widget(label)
        # box.add_widget(close_button)

        # Crear el popup
        dialog = Popup(
            title="Puntaje final",
            auto_dismiss=True,
            content=box,
            size_hint=(None, None),
            size=(250, 100),
        )

        self.dialog = dialog
        dialog.open()

    def dismiss_score_modal(self, instance):
        if self.dialog:
            self.dialog.dismiss()  # Descartar el popup
            self.dialog = None  # Limpiar la referencia al popup

    def generate_quick_answers(self, correct_result):
        # Genera dos respuestas aleatorias que se aproximan a la correcta, junto con la respuesta correcta
        delta = random.randint(1, 5)  # Variación permitida
        answer1 = correct_result + random.choice([-1, 1]) * delta
        answer2 = correct_result + random.choice([-1, 1]) * (
            delta + random.randint(1, 3)
        )
        return round(answer1, 2), round(answer2, 2), round(correct_result, 2)

    def next_exercise(self, dt):
        if time.time() - self.start_time < self.time_limit:
            exercise, correct_result = self.generate_exercise()
            self.ids.button_start_game.text = exercise
            answer1, answer2, correct_answer = self.generate_quick_answers(
                correct_result
            )

            button_order = [0, 1, 2]
            random.shuffle(button_order)

            self.ids[f"button{button_order[0] + 1}"].text = str(answer1)
            self.ids[f"button{button_order[1] + 1}"].text = str(answer2)
            self.ids[f"button{button_order[2] + 1}"].text = str(correct_answer)
            self.ids.score_label.text = f"Puntaje: {self.points}"
        else:
            print("Tiempo terminado. Puntos:", self.points)
            self.save_score(self.points)
            self.show_score_screen()
            Clock.unschedule(self.update_timer)

    def check_quick_answer(self, user_input):
        try:
            user_result = float(user_input)
        except ValueError:
            print("Por favor, ingresa un número válido.")
            return

        exercise_text = self.ids.button_start_game.text
        exercise_text = exercise_text.replace(" ", "")  # Remove all spaces

        # Ensure the expression is evaluable by Python's eval function
        try:
            correct_result = eval(exercise_text)
        except Exception as e:
            print(f"Error al evaluar el ejercicio: {e}")
            return

        # Initialize exercise log if not present
        if not hasattr(self, "exercise_log"):
            self.exercise_log = []

        # Determine exercise type
        if "+" in exercise_text or "-(" in exercise_text:
            exercise_type = "suma"
        elif "-" in exercise_text:
            exercise_type = "resta"
        else:
            exercise_type = "compuesta"  # For other compound operations

        # Determine the main operation type
        def determine_main_operator(expression):
            open_parentheses = 0
            for char in expression:
                if char == "(":
                    open_parentheses += 1
                elif char == ")":
                    open_parentheses -= 1
                elif (char == "+" or char == "-") and open_parentheses == 0:
                    return char
            return None

        main_operator = determine_main_operator(exercise_text)
        if main_operator == "+":
            exercise_type = "suma"
        elif main_operator == "-":
            exercise_type = "resta"
        else:
            exercise_type = "compuesta"  # For other compound operations

        # Check answer and update log
        if user_result == correct_result:
            self.points += 1 * self.difficulty_multiplier
            self.current_streak += 1
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
            print("¡Respuesta correcta!")
            self.exercise_log.append({"type": exercise_type, "correct": True})
        else:
            self.current_streak = 0
            print("Respuesta incorrecta.")
            self.exercise_log.append({"type": exercise_type, "correct": False})
        self.next_exercise(None)  # Pasar None como parámetro

    def start_game(self):
        # Ocultar el botón de comenzar
        # self.ids.button_start_game.opacity = 0
        self.ids.button_start_game.disabled = True
        self.ids.button_start_game.font_size = 50

        # Mostrar elementos del juego
        self.ids.button1.opacity = 1
        self.ids.button2.opacity = 1
        self.ids.button3.opacity = 1
        self.ids.timer_label.opacity = 1
        self.ids.score_label.opacity = 1
        self.initialize_game_state()
        # Configurar el temporizador
        self.start_time = time.time()  # Reiniciar el tiempo
        Clock.schedule_interval(
            self.update_timer, 1
        )  # Actualizar el temporizador cada segundo

        # Iniciar el primer ejercicio
        self.set_difficulty_mode()
        self.next_exercise(None)

    def initialize_game_state(self):
        # Reiniciar valores al iniciar el juego
        self.exercise_log = []
        self.max_streak = 0
        self.current_streak = 0
        self.points = 0
        self.difficulty_multiplier = 1  # Ajusta esto según sea necesario

    def update_timer(self, dt):
        # Actualizar el temporizador
        time_passed = time.time() - self.start_time
        time_left = max(
            0, self.time_limit - time_passed
        )  # Asegurarse de que el tiempo restante no sea negativo
        self.ids.timer_label.text = f"Tiempo restante:\n {int(time_left)}s"

        # Verificar si se acabó el tiempo
        if time_left == 0:
            print("Tiempo terminado. Puntos:", self.points)
            self.save_score(self.points)
            self.show_score_screen()

    def on_enter(self):
        modal_buttons_layout = BoxLayout(
            orientation="vertical"
        )  # Layout para contener los botones
        modal_buttons = [
            Button(
                text="Fácil",
                size_hint_y=None,
                height=40,
                on_press=lambda instance: self.set_difficulty("easy"),
                on_release=lambda instance: self.dismiss_modal(),
            ),
            Button(
                text="Medio",
                size_hint_y=None,
                height=40,
                on_press=lambda instance: self.set_difficulty("medium"),
                on_release=lambda instance: self.dismiss_modal(),
            ),
            Button(
                text="Difícil",
                size_hint_y=None,
                height=40,
                on_press=lambda instance: self.set_difficulty("hard"),
                on_release=lambda instance: self.dismiss_modal(),
            ),
        ]
        for button in modal_buttons:
            modal_buttons_layout.add_widget(button)  # Agrega cada botón al layout

        modal = Popup(
            title="Dificultad",
            content=modal_buttons_layout,  # Agrega el layout como contenido del Popup
            size_hint=(None, None),
            size=(200, 200),
            auto_dismiss=False,
            on_dismiss=self.update_difficulty_label,
        )
        self.modal = modal
        modal.open()

    def dismiss_modal(self):
        if self.modal:
            self.modal.dismiss()  # Dismiss the popup

    def update_difficulty_label(self, instance):
        self.ids.button_start_game.text = (
            f"Nvel de dificultad: {self.difficulty_mode}\n iDale para comenzar!"
        )

    def set_difficulty(self, difficulty):  # Agrega self aquí
        self.difficulty = difficulty  # Usa self.difficulty en lugar de solo difficulty
        print(f"donde cambia:", self.difficulty)
        self.ids.button_start_game.opacity = 1

    # print(self.difficulty)

    def on_leave(self):
        # Reiniciar todas las variables y elementos de la pantalla
        self.difficulty_multiplier = self.EASY_MODE_MULTIPLIER
        self.points = 0
        self.start_time = 0
        self.ids.timer_label.text = "Tiempo restante:"
        self.ids.button_start_game.opacity = 0
        self.ids.button_start_game.text = "Preparado?"
        self.ids.button_start_game.font_size = 20
        self.ids.button_start_game.disabled = False
        self.ids.button1.opacity = 0
        self.ids.button2.opacity = 0
        self.ids.button3.opacity = 0
        self.ids.timer_label.opacity = 0
        self.ids.score_label.opacity = 0
        # Detener cualquier temporizador en ejecución
        Clock.unschedule(self.update_timer)


class DifficultySelectionModal(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_difficulty(self, difficulty):
        print(f"Modal:", difficulty)
