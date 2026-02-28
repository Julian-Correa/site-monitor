# 🔍 Site Monitor

Script de Python que monitorea sitios web y envía alertas por email cuando detecta que están caídos o se recuperan.

## ¿Qué hace?

- Chequea el estado HTTP de uno o más sitios cada X minutos
- Envía un **email de alerta** cuando un sitio cae
- Envía un **email de recuperación** cuando el sitio vuelve a estar online
- Evita spam: solo notifica en el cambio de estado (caído → online / online → caído)
- Guarda un log en `monitor.log` con el historial completo

## Tecnologías

- Python 3.10+
- `requests` — chequeo HTTP
- `smtplib` — envío de emails vía Gmail
- `logging` — registro de eventos

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Julian-Correa/site-monitor
cd site-monitor

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar
cp config.example.py config.py
# Editá config.py con tu email y App Password
```

## Configuración

Para usar Gmail necesitás una **App Password** (no tu contraseña normal):

1. Ir a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Crear una app password para "Mail"
3. Pegarlo en `config.py` → `EMAIL_CONFIG["app_password"]`

```python
# config.py
SITES = [
    {"name": "Mi sitio", "url": "https://mi-sitio.com"},
]

EMAIL_CONFIG = {
    "sender":       "tu@gmail.com",
    "receiver":     "tu@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx",
}

CHECK_INTERVAL = 300  # chequear cada 5 minutos
```

## Uso

```bash
python monitor.py
```

Para correrlo en segundo plano (Linux/Mac):
```bash
nohup python monitor.py &
```

Para correrlo como tarea programada en Windows, usar el **Programador de tareas** o simplemente dejarlo corriendo en una terminal.

## Ejemplo de log

```
2026-02-28 10:00:00 [INFO] ✅ Portal OriNet — OK (200) — 312.5ms
2026-02-28 10:05:00 [INFO] ✅ Portal OriNet — OK (200) — 298.1ms
2026-02-28 10:10:00 [WARNING] ❌ Portal OriNet — CAÍDO (código: 0)
2026-02-28 10:10:01 [INFO] Email enviado: 🚨 [Portal OriNet] Sitio caído
2026-02-28 10:15:00 [INFO] ✅ Portal OriNet — OK (200) — 445.2ms
2026-02-28 10:15:01 [INFO] Email enviado: ✅ [Portal OriNet] Sitio recuperado
```

## Agregar más sitios

En `config.py`, agregá entradas al array `SITES`:

```python
SITES = [
    {"name": "Portal OriNet",  "url": "https://portal-orinet.netlify.app/"},
    {"name": "Mi API",         "url": "https://mi-api.com/health"},
    {"name": "Blog personal",  "url": "https://mi-blog.com"},
]
```

---

Desarrollado por [Julian Correa](https://github.com/Julian-Correa)
