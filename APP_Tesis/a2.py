from kivy.lang import Builder

from kivymd.app import MDApp

KV = """
MDScreen:

    MDFloatingActionButton:
        icon: "plus"
      

        
"""


class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)


Example().run()
