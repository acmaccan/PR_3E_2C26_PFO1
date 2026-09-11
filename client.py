"""
Cliente de chat básico basado en sockets TCP.
"""

import logging
import socket

HOST = "localhost"
PORT = 5000

logger = logging.getLogger(__name__)


def conectar():
    """
    Crea el socket TCP/IP y lo conecta al servidor en (HOST, PORT).
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((HOST, PORT))
    except ConnectionRefusedError:
        # El servidor no está levantado o no está escuchando en ese puerto.
        logger.error("No se pudo conectar a %s:%s. ¿Está el servidor corriendo?", HOST, PORT)
        raise
    except OSError as error:
        logger.error("No se pudo conectar a %s:%s -> %s", HOST, PORT, error)
        raise

    logger.info("Conectado al servidor en %s:%s", HOST, PORT)
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
                    logger.info("Cerrando conexión")
                    break

                respuesta = cliente.recv(1024)

                if not respuesta:
                    # El servidor cerró la conexión inesperadamente.
                    logger.error("El servidor cerró la conexión")
                    break

                # Respuesta del servidor: es contenido de la conversación,
                # no un log de trazabilidad, así que se muestra con print().
                print(f"[SERVIDOR] {respuesta.decode('utf-8')}")
            except ConnectionError as error:
                # ConnectionResetError, BrokenPipeError, etc.: se perdió
                # la conexión con el servidor durante el envío/recepción.
                logger.error("Se perdió la conexión con el servidor -> %s", error)
                break


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        cliente = conectar()
    except OSError:
        return

    loop_envio(cliente)


if __name__ == "__main__":
    main()
