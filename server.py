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


def manejar_cliente(conn, addr):
    """
    Atiende una conexión de cliente ya aceptada.

    Recibe mensajes en un loop hasta que el cliente cierre la conexión
    o envíe la palabra "éxito" (que cierra la sesión desde el servidor).
    """
    print(f"[INFO] Cliente conectado: {addr}")

    with conn:
        while True:
            datos = conn.recv(1024)

            if not datos:
                # El cliente cerró la conexión sin enviar "éxito"
                print(f"[INFO] Cliente {addr} cerró la conexión")
                break

            mensaje = datos.decode("utf-8").strip()
            print(f"[INFO] Mensaje recibido de {addr}: {mensaje}")

            if mensaje.lower() == "éxito":
                print(f"[INFO] Cliente {addr} finalizó la sesión")
                break

            # Placeholder: acá en el siguiente paso va guardar_mensaje()
            # y la respuesta al cliente (secciones 1.3 y 1.5 del PLAN.md).


def main():
    servidor = iniciar_socket()
    try:
        while True:
            conn, addr = servidor.accept()
            manejar_cliente(conn, addr)
    except KeyboardInterrupt:
        print("\n[INFO] Servidor detenido manualmente")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
