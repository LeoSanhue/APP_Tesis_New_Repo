from kivymd.uix.card import MDSeparator
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
from Screens.user_profile_screen.user_profile_screen import UserProfileScreen
from Screens.login_screen.login_screen import *  # Importa la clase LoginScreen
from Screens.config_screen.config_screen import *  # Importa la clase ConfigScreen
from Screens.game_screen.game_screen import *  # Importa la clase GameScreen
from Screens.register_screen.register_screen import *  # Importa la clase RegisterScreen
from Screens.config_screen.image_viewer import *
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

Window.size = (350, 600)


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


class NewsItem(MDBoxLayout):
    image_source = StringProperty()
    text = StringProperty()
    news_id = StringProperty()  # Agregar news_id como un atributo

    def __init__(self, image_source, text, **kwargs):
        super().__init__(**kwargs)
        self.image_source = image_source
        self.text = text


#        self.add_widget(sep)


class MainScreen(Screen):

    def change_app_bar_title(self, new_title):
        # Cambia el título de la TopAppBar
        self.ids.topbar.title = new_title

    def UserProfile(self):
        self.previous_screen = self.manager.current
        self.manager.current = "user_screen"

    def Back(self):
        self.manager.current = self.previous_screen

    def set_selected_tab(self, tab_name):
        self.selected_tab = tab_name
        self.root.ids.bot_nav.current = tab_name

    def deselect_tabs(self):
        # Método para desseleccionar todas las pestañas en MDBottomNavigation
        for (
            item
        ) in self.ids.bot_nav.ids.keys():  # Itera sobre todas las claves de los IDs
            if item.startswith("tab_"):  # Verifica si el ID es una pestaña
                self.ids.bot_nav.ids[item].state = "normal"

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tabs_label, tab_text):
        # Método que se llama cada vez que se cambia de pestaña
        self.deselect_tabs()  # Deselecciona todas las pestañas

    def on_enter(self):
        self.ids.news_container.clear_widgets()  # Limpiar los widgets existentes
        news_data = [
            {
                "id": 1,
                "image": "assets/images/sample1.jpg",
                "text": "La IA revoluciona la enseñanza en colegios",
            },
            {
                "id": 2,
                "image": "assets/images/sample2.jpg",
                "text": "Inteligencia artificial mejora aprendizaje estudiantil",
            },
            {
                "id": 3,
                "image": "assets/images/sample3.jpg",
                "text": "Colegios adoptan IA para personalizar la educación",
            },
            {
                "id": 4,
                "image": "assets/images/sample4.jpg",
                "text": "Robots docentes: el futuro de la educación escolar",
            },
            {
                "id": 5,
                "image": "assets/images/sample5.jpg",
                "text": "IA en las aulas: el nuevo aliado de los maestros",
            },
        ]

        for news in news_data:
            # Verificar si el widget ya existe en news_container
            if not self._widget_exists(news["id"]):
                news_item = NewsItem(image_source=news["image"], text=news["text"])
                self.ids.news_container.add_widget(news_item)
                print(news["id"])
        ################################################
        for item in self.ids.bot_nav.children:
            item.active = False

        # Set active state based on current screen
        current_screen = self.manager.current_screen.name
        for item in self.ids.bot_nav.children:
            if item.ids == "main_screen":
                item.active = True
        self.deselect_tabs()

    def highlight_tab(self, tab_name, instance):
        # Ejemplo de cómo podrías resaltar visualmente un item
        if tab_name == "News":
            instance.background_color = [0.1, 0.5, 0.9, 1]  # Cambia el color de fondo
        elif tab_name == "User":
            instance.background_color = [0.9, 0.1, 0.5, 1]
        elif tab_name == "Games":
            instance.background_color = [0.5, 0.9, 0.1, 1]
        elif tab_name == "Settings":
            instance.background_color = [0.3, 0.7, 0.2, 1]

    def highlight_desired_tab(self, *args):
        # Supongamos que deseas resaltar la pestaña 'News' que está en el índice 0
        self.ids.bot_nav.switch_tab(1)

    def _widget_exists(self, widget_id):
        # Verificar si un widget con el mismo id ya existe en news_container
        for child in self.ids.news_container.children:
            if hasattr(child, "news_id") and child.news_id == widget_id:
                return True
        return False
