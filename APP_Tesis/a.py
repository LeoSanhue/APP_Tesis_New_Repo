import os


class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def save_theme(self, theme):
        try:
            with open(self.config_file, "w") as configfile:
                configfile.write(f"theme = {theme}\n")
                print(f"Guardando tema en archivo de configuración: {theme}")
        except IOError as e:
            print(f"Error al guardar el archivo de configuración: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def load_theme(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as configfile:
                    for line in configfile:
                        if line.startswith("theme ="):
                            theme = line.split("=", 1)[1].strip()
                            print(
                                f"Tema cargado desde archivo de configuración: {theme}"
                            )
                            return theme
            except IOError as e:
                print(f"Error al leer archivo de configuración: {e}")
        else:
            print(
                "Archivo de configuración no encontrado. Usando configuración por defecto."
            )
            self.save_theme("Light")
            return "Light"


# Ejemplo de uso
config_manager = ConfigManager("settings.txt")
# config_manager.save_theme("Light")
theme = config_manager.load_theme()
print(f"Tema actual: {theme}")
