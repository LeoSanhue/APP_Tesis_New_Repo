from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
import configparser
import mysql.connector
from Screens.login_screen.login_screen import LoginScreen
from kivymd.app import MDApp


class BackgroundViewerScreen(Screen):
    def on_enter(self):
        # Limpiar la lista de fondos
        self.ids.background_list.clear_widgets()

        # Lista de fondos
        backgrounds = [
            "assets/images/background1.jpg",
            "assets/images/background2.jpg",
            "assets/images/background3.jpg",
            "assets/images/background4.jpg",
            "assets/images/background5.jpg",
            "assets/images/background6.jpg",
            "assets/images/background7.jpg",
            "assets/images/background8.jpg",
            "assets/images/background9.jpg",
            "assets/images/background10.jpg",
        ]  # Puedes cargar los fondos desde tu directorio

        # Agregar los fondos a la lista
        for background_path in backgrounds:
            img = Image(
                source=background_path, size_hint_y=None, height=200, allow_stretch=True
            )
            img.bind(on_touch_down=self.on_image_touch_down)
            self.ids.background_list.add_widget(img)

    def on_image_touch_down(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.show_confirmation_dialog(instance.source)
            return True  # Detener la propagación del evento táctil
        return False  # No detener la propagación si no se toca la imagen

    def show_confirmation_dialog(self, image):
        # Crear una vista modal
        modal = ModalView(size_hint=(0.8, 0.4), auto_dismiss=False)

        # Crear un layout principal para el modal
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)

        # Crear un layout para la pregunta
        question_layout = MDBoxLayout(
            orientation="vertical", size_hint_y=None, height=50
        )
        question_layout.add_widget(
            Label(
                text="¿Deseas seleccionar\nesta imagen como fondo?",
                size_hint_y=None,
                height=50,
                font_size=18,
            )
        )

        # Crear un layout para los botones
        button_layout = MDBoxLayout(
            orientation="horizontal", size_hint_y=None, height=50, spacing=20
        )

        # Botones de confirmación
        btn_confirm = MDRaisedButton(
            text="Seleccionar",
            halign="center",
            on_release=lambda x: self.select_background(image, modal),
        )
        btn_cancel = MDRaisedButton(
            text="Cancelar", halign="center", on_release=modal.dismiss
        )

        # Agregar los botones al layout de botones
        button_layout.add_widget(btn_cancel)
        button_layout.add_widget(btn_confirm)

        # Agregar ambos layouts al layout principal
        main_layout.add_widget(question_layout)
        main_layout.add_widget(button_layout)

        # Establecer el contenido del modal
        modal.add_widget(main_layout)
        modal.open()

    def select_background(self, image, modal):
        # Llamar a la función para guardar la imagen seleccionada en la base de datos
        self.change_background(image)
        modal.dismiss()

    def change_background(self, background_path):
        # Cambiar el fondo de la aplicación
        app = MDApp.get_running_app()
        app.change_background(background_path)
        print(f"Fondo {background_path} guardado como fondo de la app.")
