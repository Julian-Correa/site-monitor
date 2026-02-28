# ─────────────────────────────────────────────
#  Configuración del Site Monitor — EJEMPLO
#  Copiá este archivo como config.py y completá tus datos
# ─────────────────────────────────────────────

SITES = [
    {
        "name": "Portal OriNet",
        "url":  "https://portal-orinet.netlify.app/"
    },
]

EMAIL_CONFIG = {
    "sender":       "tu_email@gmail.com",
    "receiver":     "tu_email@gmail.com",
    "app_password": "xxxx xxxx xxxx xxxx",  # App Password de Google
}

CHECK_INTERVAL = 300  # segundos
