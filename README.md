# gotify-notify

Cliente ligero de [Gotify](https://gotify.net/) para **KDE Plasma 6** que muestra las notificaciones del servidor como notificaciones nativas del escritorio, con soporte de urgencia según prioridad.

## ¿Cómo funciona?

El script se conecta al servidor Gotify vía **WebSocket** y usa `notify-send` para mostrar cada mensaje como una notificación nativa de Plasma. Corre como servicio de usuario de systemd, arranca automáticamente con la sesión y se reconecta solo si la red no está disponible al inicio.

## Requisitos

- KDE Plasma 6
- Python 3
- `notify-send` (paquete `libnotify-bin`)
- Servidor Gotify corriendo en la red local

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/osdaeg/plasma6gotify.git
mv plasma6gotify gotify_notify
cd gotify_notify
```

### 2. Instalar dependencias

```bash
pip install websocket-client python-dotenv --break-system-packages
```

### 3. Configurar las variables de entorno

Copiá el archivo de ejemplo y editalo con tus datos:

```bash
cp gotify_notify.env.example gotify_notify.env
```

```env
GOTIFY_URL=ws://192.168.1.10:8088/stream
GOTIFY_TOKEN=tu-client-token
```

### 4. Obtener el token de cliente

1. Abrí la interfaz web de Gotify
2. Ir a **Clients** → crear un nuevo cliente
3. Copiar el token generado

> ⚠️ Usá el token de **Client**, no el de App. El token de App es para enviar mensajes, el de Client es para recibirlos.

### 5. Instalar el servicio systemd

```bash
mkdir -p ~/.config/systemd/user
cp gotify.service ~/.config/systemd/user/gotify.service
```

Editá el archivo del servicio y ajustá la ruta del script y tu usuario:

```ini
ExecStart=/usr/bin/python3 /home/tu_usuario/scripts/gotify_notify/gotify_notify.py
```

Verificá también que el UID en `DBUS_SESSION_BUS_ADDRESS` coincida con el tuyo (`id -u`).

### 6. Activar el servicio

```bash
systemctl --user daemon-reload
systemctl --user enable gotify.service
systemctl --user start gotify.service
```

## Niveles de urgencia

Las notificaciones se muestran con distinta urgencia según la prioridad asignada en Gotify:

| Prioridad Gotify | Urgencia      | Comportamiento                        |
|------------------|---------------|---------------------------------------|
| 0 – 3            | `low`         | Silenciosa, se cierra sola            |
| 4 – 7            | `normal`      | Normal, se cierra sola                |
| 8 – 10           | `critical`    | Borde naranja, no se cierra sola      |

## Comandos útiles

```bash
# Ver estado del servicio
systemctl --user status gotify.service

# Ver logs en tiempo real
journalctl --user -u gotify.service -f

# Reiniciar
systemctl --user restart gotify.service

# Detener
systemctl --user stop gotify.service
```

## Estructura del proyecto

```
gotify-notify/
├── gotify_notify.py           # Script principal
├── gotify_notify.env.example  # Plantilla de configuración
├── gotify_notify.env          # Tu configuración local (no se sube a Git)
├── gotify.service             # Servicio systemd de usuario
├── .gitignore
└── README.md
```

## Notas

- El script usa un bucle `while True` con reintentos cada 5 segundos para reconectarse automáticamente si la red no está disponible al inicio de sesión.
- El `ExecStartPre=/bin/sleep 5` en el servicio le da tiempo a Plasma para levantar el bus DBus antes de que arranque el script.
- Las credenciales se leen desde `gotify_notify.env` vía `python-dotenv`. Nunca hardcodear la URL ni el token en el script.

## Licencia

AGPL
