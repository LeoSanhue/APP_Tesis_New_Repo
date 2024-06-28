from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton
import configparser
import mysql.connector
from Screens.login_screen.login_screen import LoginScreen


class ImageViewerScreen(Screen):
    def on_enter(self):
        # Limpiar la lista de imágenes
        self.ids.image_list.clear_widgets()

        # Lista de imágenes
        images = [
            "assets/images/1.png",
            "assets/images/2.png",
            "assets/images/3.png",
            "assets/images/4.png",
            "assets/images/5.png",
            "assets/images/6.png",
        ]  # Puedes cargar las imágenes desde tu directorio

        # Agregar las imágenes a la lista
        for image_path in images:
            img = Image(
                source=image_path, size_hint_y=None, height=200, allow_stretch=True
            )
            img.bind(on_touch_down=self.on_image_touch_down)
            self.ids.image_list.add_widget(img)

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
                text="¿Deseas seleccionar esta \n imagen  como foto de perfil?",
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
            on_release=lambda x: self.select_profile_picture(image, modal),
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

    def select_profile_picture(self, image, modal):
        # Llamar a la función para guardar la imagen seleccionada en la base de datos
        self.save_profile_picture(image)
        modal.dismiss()

    def save_profile_picture(self, image_path):
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
        query = "UPDATE users SET profile_picture_path=%s WHERE email=%s"
        cursor.execute(query, (image_path, email))
        db.commit()

        cursor.close()
        db.close()

        print(f"Imagen {image_path} guardada en la base de datos.")
