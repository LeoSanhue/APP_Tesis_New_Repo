import random
import time


def generar_ejercicio():
    operaciones = ["+", "-", "*", "/"]
    operacion = random.choice(operaciones)
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    # Evitamos la división por cero
    while operacion == "/" and num2 == 0:
        num2 = random.randint(1, 20)

    resultado = eval(f"{num1} {operacion} {num2}")

    ejercicio = f"{num1} {operacion} {num2}"
    return ejercicio, resultado


def verificar_respuesta(ejercicio, resultado_usuario, resultado_correcto):
    if resultado_usuario == resultado_correcto:
        return True
    else:
        return False


def main():
    puntos = 0
    tiempo_limite = 30  # Segundos
    inicio_tiempo = time.time()

    while time.time() - inicio_tiempo < tiempo_limite:
        ejercicio, resultado_correcto = generar_ejercicio()
        print("Resuelve:", ejercicio)
        respuesta_usuario = input("Tu respuesta: ")

        try:
            respuesta_usuario = float(respuesta_usuario)
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue

        if verificar_respuesta(ejercicio, respuesta_usuario, resultado_correcto):
            puntos += 1
            print("¡Respuesta correcta!")
        else:
            print("Respuesta incorrecta.")

    print("Tiempo terminado. Puntos:", puntos)


if __name__ == "__main__":
    main()
