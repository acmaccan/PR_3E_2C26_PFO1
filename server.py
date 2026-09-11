"""
Servidor de chat básico basado en sockets TCP.
"""

import socket
import sqlite3
from datetime import datetime

HOST = "localhost"
PORT = 5000
DB_PATH = "mensajes.db"


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


def inicializar_db():
    """
    Crea la tabla `mensajes` en la base SQLite si todavía no existe.
    """
    # Inserción / esquema en base de datos
    try:
        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                """
                CREATE TABLE IF NOT EXISTS mensajes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contenido TEXT NOT NULL,
                    fecha_envio TEXT NOT NULL,
                    ip_cliente TEXT NOT NULL
                )
                """
            )
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo inicializar la base de datos -> {error}")
        raise


def guardar_mensaje(contenido, ip_cliente):
    """
    Inserta un mensaje recibido en la tabla `mensajes`.

    Devuelve el timestamp (fecha_envio) con el que quedó guardado,
    o None si no se pudo guardar por un error de base de datos.
    """
    fecha_envio = datetime.now().isoformat(timespec="seconds")

    try:
        with sqlite3.connect(DB_PATH) as db:
            db.execute(
                "INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                (contenido, fecha_envio, ip_cliente),
            )
    except sqlite3.Error as error:
        print(f"[ERROR] No se pudo guardar el mensaje en la base de datos -> {error}")
        return None

    return fecha_envio


def manejar_cliente(conn, addr):
    """
    Atiende una conexión de cliente ya aceptada.

    Recibe mensajes en un loop hasta que el cliente cierre la conexión
    o envíe la palabra "éxito" (que cierra la sesión desde el servidor).
    """
    print(f"[INFO] Cliente conectado: {addr}")

    try:
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

                guardar_mensaje(mensaje, addr[0])

                # Placeholder: acá en el siguiente paso va la respuesta
                # al cliente (sección 1.5 del PLAN.md).
    except ConnectionError as error:
        # El cliente se desconectó abruptamente (ConnectionResetError,
        # BrokenPipeError, etc.). Se registra y se sigue atendiendo
        # al resto de las conexiones sin tirar abajo el servidor.
        print(f"[ERROR] Conexión perdida con {addr} -> {error}")
    except UnicodeDecodeError as error:
        # Datos recibidos que no se pudieron decodificar como texto.
        print(f"[ERROR] Mensaje inválido recibido de {addr} -> {error}")


def main():
    inicializar_db()
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
