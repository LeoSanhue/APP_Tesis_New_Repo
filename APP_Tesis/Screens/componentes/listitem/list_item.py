from kivy.uix.accordion import BooleanProperty
from kivymd.uix.list import (
    BaseListItem,
    IRightBodyTouch,
    OneLineRightIconListItem,
    TwoLineRightIconListItem,
)
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.properties import BooleanProperty
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp


class BaseListItemWithSwitch(BaseListItem):
    """Base class for one-line and two-line items in thw settings list."""

    active = BooleanProperty(False)  # active/inactive


class BaseListItemWithButton(BaseListItem):
    """Base class for one-line and two-line items in thw settings list."""

    active = BooleanProperty(False)  # active/inactive


class RightSwitchContainer(IRightBodyTouch, MDSwitch):
    """
    The class implements a container for placing the switch on the right side of the settings list item.
    """


class RightButtonContainer(IRightBodyTouch, MDIconButton):
    """
    The class implements a container for placing the button on the right side of the settings list item.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        self.icon = "robot"  # Cambia "check" por el ícono que desees
        self.text_color = app.theme_cls.primary_color


class OneLineListItemWithSwitch(OneLineRightIconListItem, BaseListItemWithSwitch):
    """The class implements a one-line item of the settings list."""


class TwoLineListItemWithSwitch(TwoLineRightIconListItem, BaseListItemWithSwitch):
    """The class implements a two-line item of the settings list."""

    active = BooleanProperty(False)  # active/inactive


class OneLineListItemWithButton(OneLineRightIconListItem, BaseListItemWithButton):
    """The class implements a one-line item of the settings list."""


class TwoLineListItemWithButton(TwoLineRightIconListItem, BaseListItemWithButton):
    """The class implements a two-line item of the settings list."""

    active = BooleanProperty(False)  # active/inactive
