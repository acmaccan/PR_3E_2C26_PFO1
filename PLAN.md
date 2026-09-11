# TP: Implementación de un Chat Básico Cliente-Servidor con Sockets y Base de Datos

## Objetivo

Aprender a configurar un servidor de sockets en Python que reciba mensajes de
clientes, los almacene en una base de datos y envíe confirmaciones, aplicando
buenas prácticas de modularización y manejo de errores. Comentar el código
para explicar las configuraciones del servidor.

## Alcance

- **Servidor**: socket TCP escuchando en `localhost:5000`.
- **Cliente**: se conecta al servidor y envía mensajes interactivamente.
- **Persistencia**: SQLite para guardar cada mensaje recibido.

---

## 1. Servidor (`server.py`)

### 1.1 Inicializar el socket
- [x] Función `iniciar_socket()` que crea el socket TCP/IP (`AF_INET`, `SOCK_STREAM`).
- [x] Bind a `localhost:5000`.
- [x] `listen()` para aceptar conexiones entrantes.
- [x] Comentar la sección: `# Configuración del socket TCP/IP`.

### 1.2 Aceptar conexiones y recibir mensajes
- [x] Función `manejar_cliente(conn, addr)` (o loop principal) que:
  - Acepta la conexión (`accept()`).
  - Recibe datos (`recv()`) en un loop hasta que el cliente cierre o envíe `éxito`.
  - Decodifica el mensaje recibido.

### 1.3 Guardar mensaje en base de datos
- [x] Función `guardar_mensaje(contenido, ip_cliente)` que inserta en SQLite.
- [x] Esquema de la tabla `mensajes`:
  | Campo         | Tipo     | Descripción                     |
  |---------------|----------|----------------------------------|
  | id            | INTEGER  | PK autoincremental               |
  | contenido     | TEXT     | Mensaje enviado por el cliente   |
  | fecha_envio   | TEXT     | Timestamp de recepción           |
  | ip_cliente    | TEXT     | IP del cliente que envió         |
- [x] Función `inicializar_db()` que crea la tabla si no existe.

### 1.4 Manejo de errores
- [x] Puerto ocupado (`OSError` al hacer `bind`) → mensaje claro y salida controlada.
- [x] Base de datos no accesible (errores de `sqlite3`) → capturar excepción y loggear.
- [x] Errores de conexión con el cliente (`ConnectionResetError`, etc.) → no debe tirar abajo el servidor completo.

### 1.5 Responder al cliente
- [x] Tras guardar el mensaje, responder con: `"Mensaje recibido: <timestamp>"`.

### 1.6 Estructura sugerida de funciones
```python
def iniciar_socket(): ...
def inicializar_db(): ...
def guardar_mensaje(contenido, ip_cliente): ...
def manejar_cliente(conn, addr): ...
def main(): ...
```

---

## 2. Cliente (`client.py`)

- [ ] Conectarse al servidor (`localhost:5000`).
- [ ] Loop de envío de mensajes:
  - Pedir input al usuario.
  - Enviar mensaje al servidor.
  - Mostrar la respuesta recibida.
  - Repetir hasta que el usuario escriba `éxito` (cierra la conexión).
- [ ] Manejo básico de errores de conexión (servidor no disponible, etc.).

---

## 3. Base de datos

- [ ] Usar el módulo `sqlite3` (nativo de Python, sin dependencias extra).
- [ ] Archivo de DB, por ejemplo `mensajes.db`, en la raíz del proyecto.
- [ ] Verificar que la tabla se crea automáticamente al iniciar el servidor.

---

## 4. Buenas prácticas

- [ ] Modularizar: separar funciones por responsabilidad (socket, DB, manejo de errores).
- [ ] Comentar cada sección clave (ej: `# Configuración del socket TCP/IP`, `# Inserción en base de datos`).
- [ ] Manejo de excepciones con `try/except` específicos, no genéricos silenciosos.
- [ ] (Opcional) Logging en vez de `print` para trazabilidad.

---

## 5. Pruebas locales

- [ ] Ejecutar primero el servidor: `python server.py`.
- [ ] Ejecutar el cliente en otra terminal: `python client.py`.
- [ ] Probar:
  - Envío de varios mensajes seguidos.
  - Cierre correcto al escribir `éxito`.
  - Verificar que los mensajes quedan guardados en la DB (consultar con `sqlite3` o script auxiliar).
  - Simular error: correr dos servidores a la vez (puerto ocupado) y verificar el mensaje de error.

---

## 6. Entrega

- [ ] Subir el código a un repositorio (GitHub / Bitbucket) **o**
- [ ] Comprimir la solución en `.zip` / `.rar` si no se usa repositorio.
- [ ] Incluir un `README.md` con instrucciones de ejecución (cómo levantar servidor y cliente).

---

## Estructura de archivos propuesta

```
pfo-01/
├── server.py
├── client.py
├── mensajes.db        # generado en runtime
├── README.md
└── PLAN.md            # este archivo
```
