"""
Cliente de chat básico basado en sockets TCP.
"""

import socket

HOST = "localhost"
PORT = 5000


def conectar():
    """
    Crea el socket TCP/IP y lo conecta al servidor en (HOST, PORT).
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
    except ConnectionRefusedError:
        # El servidor no está levantado o no está escuchando en ese puerto.
        print(f"[ERROR] No se pudo conectar a {HOST}:{PORT}. ¿Está el servidor corriendo?")
        raise
    except OSError as error:
        print(f"[ERROR] No se pudo conectar a {HOST}:{PORT} -> {error}")
        raise

    print(f"[INFO] Conectado al servidor en {HOST}:{PORT}")
    return cliente


def loop_envio(cliente):
    """
    Pide mensajes al usuario y los envía al servidor en un loop.

    Muestra la respuesta del servidor después de cada envío.
    Termina cuando el usuario escribe "éxito" o si se pierde la conexión.
    """
    with cliente:
        while True:
            mensaje = input("Mensaje (o 'éxito' para salir): ")

            try:
                cliente.sendall(mensaje.encode("utf-8"))

                if mensaje.lower() == "éxito":
                    print("[INFO] Cerrando conexión")
                    break

                respuesta = cliente.recv(1024)

                if not respuesta:
                    # El servidor cerró la conexión inesperadamente.
                    print("[ERROR] El servidor cerró la conexión")
                    break

                print(f"[SERVIDOR] {respuesta.decode('utf-8')}")
            except ConnectionError as error:
                # ConnectionResetError, BrokenPipeError, etc.: se perdió
                # la conexión con el servidor durante el envío/recepción.
                print(f"[ERROR] Se perdió la conexión con el servidor -> {error}")
                break


def main():
    try:
        cliente = conectar()
    except OSError:
        return

    loop_envio(cliente)


if __name__ == "__main__":
    main()
