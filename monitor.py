import requests
import smtplib
import time
import logging
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import SITES, EMAIL_CONFIG, CHECK_INTERVAL

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── Estado interno ────────────────────────────────────────────────────────────
# Guarda el último estado de cada sitio para no spamear alertas
site_status = {site["url"]: True for site in SITES}


def check_site(url: str, timeout: int = 10) -> tuple[bool, int, float]:
    """
    Chequea si un sitio está online.
    Retorna: (está_online, status_code, tiempo_respuesta_ms)
    """
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        elapsed = round((time.time() - start) * 1000, 2)
        is_up = response.status_code < 500
        return is_up, response.status_code, elapsed
    except requests.ConnectionError:
        return False, 0, 0
    except requests.Timeout:
        return False, 408, 0
    except Exception as e:
        log.error(f"Error inesperado chequeando {url}: {e}")
        return False, 0, 0


def send_email(subject: str, body: str):
    """Envía un email de alerta."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = EMAIL_CONFIG["sender"]
        msg["To"]      = EMAIL_CONFIG["receiver"]

        # Versión HTML del email
        html = f"""
        <html><body style="font-family: monospace; background:#f4f7fb; padding:2rem;">
          <div style="max-width:520px; margin:auto; background:#fff; border:1px solid #dae3ed;
                      border-radius:4px; padding:2rem;">
            <h2 style="color:#0f1f30; margin-top:0;">{subject}</h2>
            <pre style="background:#f4f7fb; padding:1rem; border-radius:4px;
                        font-size:.85rem; color:#0f1f30;">{body}</pre>
            <p style="color:#6b8aaa; font-size:.75rem; margin-bottom:0;">
              Site Monitor · {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            </p>
          </div>
        </body></html>
        """

        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["app_password"])
            server.sendmail(EMAIL_CONFIG["sender"], EMAIL_CONFIG["receiver"], msg.as_string())

        log.info(f"Email enviado: {subject}")

    except Exception as e:
        log.error(f"Error enviando email: {e}")


def run():
    log.info("=" * 50)
    log.info("  Site Monitor iniciado")
    log.info(f"  Sitios monitoreados: {len(SITES)}")
    log.info(f"  Intervalo: {CHECK_INTERVAL}s")
    log.info("=" * 50)

    while True:
        for site in SITES:
            url  = site["url"]
            name = site["name"]

            is_up, status_code, response_ms = check_site(url)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            if is_up:
                log.info(f"[OK] {name} — OK ({status_code}) — {response_ms}ms")

                # Si estaba caído y volvió, notificar recuperación
                if not site_status[url]:
                    send_email(
                        subject=f"[OK] [{name}] Sitio recuperado",
                        body=(
                            f"El sitio volvió a estar online.\n\n"
                            f"URL:            {url}\n"
                            f"Estado:         {status_code}\n"
                            f"Tiempo respuesta: {response_ms}ms\n"
                            f"Hora:           {now}"
                        )
                    )
                    site_status[url] = True

            else:
                log.warning(f"[DOWN] {name} — CAÍDO (código: {status_code})")

                # Solo notificar si antes estaba online (evita spam)
                if site_status[url]:
                    send_email(
                        subject=f"[ALERTA] [{name}] Sitio caído",
                        body=(
                            f"Se detectó que el sitio está caído.\n\n"
                            f"URL:    {url}\n"
                            f"Código: {status_code}\n"
                            f"Hora:   {now}\n\n"
                            f"Se enviará otra alerta cuando el sitio se recupere."
                        )
                    )
                    site_status[url] = False

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
