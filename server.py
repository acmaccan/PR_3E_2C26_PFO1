"""
Servidor de chat básico basado en sockets TCP.
"""

import socket

HOST = "localhost"
PORT = 5000


def iniciar_socket():
    """
    Crea, configura y deja escuchando el socket TCP/IP del servidor.

    Devuelve el socket ya bindeado a (HOST, PORT) y en modo listen(),
    listo para aceptar conexiones entrantes de clientes.
    """
    # Configuración del socket TCP/IP
    # AF_INET  -> familia de direcciones IPv4
    # SOCK_STREAM -> socket orientado a conexión (TCP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar la dirección/puerto inmediatamente después de cerrar
    # el servidor, evitando el error "Address already in use" al reiniciar.
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORT))
    except OSError as error:
        # Puerto ocupado u otro problema al bindear: informamos y salimos
        # de forma controlada en lugar de dejar el traceback crudo.
        print(f"[ERROR] No se pudo iniciar el servidor en {HOST}:{PORT} -> {error}")
        raise

    servidor.listen()
    print(f"[INFO] Servidor escuchando en {HOST}:{PORT}")

    return servidor


def main():
    servidor = iniciar_socket()
    try:
        # Placeholder: en el siguiente paso acá va el loop de accept()
        # y el manejo de clientes (sección 1.2 del PLAN.md).
        pass
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
