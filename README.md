# Chat Básico Cliente-Servidor con Sockets y Base de Datos

TP de la Propuesta Formativa Obligatoria: servidor de sockets TCP en Python
que recibe mensajes de clientes, los guarda en SQLite y responde con una
confirmación.

## Requisitos

- Python 3 (sin dependencias externas: se usa `socket` y `sqlite3`, ambos
  nativos).

## Cómo ejecutar

1. Levantar el servidor (queda escuchando en `localhost:5000`):
   ```
   python server.py
   ```
2. En otra terminal, levantar el cliente:
   ```
   python client.py
   ```
3. Escribir mensajes en la terminal del cliente. Por cada uno, el servidor
   responde `Mensaje recibido: <timestamp>`.
4. Escribir `éxito` para cerrar la conexión.

Los mensajes recibidos quedan guardados en `mensajes.db` (se crea
automáticamente en la raíz del proyecto la primera vez que se levanta el
servidor), en la tabla `mensajes` (`id`, `contenido`, `fecha_envio`,
`ip_cliente`).

## Pruebas realizadas

### 1. Envío de mensajes y respuesta del servidor

Con el servidor corriendo, se ejecuta el cliente y se envían varios mensajes:

```
$ python client.py
[INFO] Conectado al servidor en localhost:5000
Mensaje (o 'éxito' para salir): hola
[SERVIDOR] Mensaje recibido: 2026-09-10T20:49:33
Mensaje (o 'éxito' para salir): éxito
[INFO] Cerrando conexión
```

Log del servidor en paralelo:

```
2026-09-10 20:49:20 [INFO] Servidor escuchando en localhost:5000
2026-09-10 20:49:30 [INFO] Cliente conectado: ('127.0.0.1', 50098)
2026-09-10 20:49:33 [INFO] Mensaje recibido de ('127.0.0.1', 50098): hola
2026-09-10 20:49:33 [INFO] Cliente ('127.0.0.1', 50098) finalizó la sesión
```

### 2. Persistencia en la base de datos

Tras el envío anterior, se consulta `mensajes.db`:

```
$ python -c "
import sqlite3
db = sqlite3.connect('mensajes.db')
for fila in db.execute('SELECT * FROM mensajes'):
    print(fila)
"
(1, 'hola', '2026-09-10T20:49:33', '127.0.0.1')
```

### 3. Puerto ocupado

Con un servidor ya corriendo, se intenta levantar un segundo servidor en
paralelo:

```
$ python server.py
[ERROR] No se pudo iniciar el servidor en localhost:5000 -> [WinError 10048]
Normalmente solo se permite un uso de cada dirección de socket...
```

El proceso corta de forma controlada, sin traceback crudo, y el primer
servidor sigue funcionando.

### 4. Corte abrupto de conexión

Se simula un cliente que corta la conexión de golpe (RST) en medio del envío:

```
2026-09-10 20:56:37 [INFO] Cliente conectado: ('127.0.0.1', 56689)
2026-09-10 20:56:37 [INFO] Mensaje recibido de ('127.0.0.1', 56689): mensaje antes del corte
2026-09-10 20:56:37 [ERROR] Conexión perdida con ('127.0.0.1', 56689) -> [WinError 10054]
Se ha forzado la interrupción de una conexión existente por el host remoto
2026-09-10 20:56:38 [INFO] Cliente conectado: ('127.0.0.1', 56690)
2026-09-10 20:56:38 [INFO] Mensaje recibido de ('127.0.0.1', 56690): sigo vivo
2026-09-10 20:56:38 [INFO] Mensaje recibido de ('127.0.0.1', 56690): éxito
2026-09-10 20:56:38 [INFO] Cliente ('127.0.0.1', 56690) finalizó la sesión
```

El mensaje enviado antes del corte quedó guardado en la base, el error se
loguea sin tirar abajo el servidor, y el servidor sigue aceptando nuevos
clientes con normalidad.

## Estructura del proyecto

```
server.py    # Servidor: socket, base de datos, manejo de errores
client.py    # Cliente: conexión y envío interactivo de mensajes
mensajes.db  # Base SQLite, generada en runtime
PLAN.md      # Checklist de implementación de la PFO
README.md    # Este archivo
```
