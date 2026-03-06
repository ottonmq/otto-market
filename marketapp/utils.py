
import os  # Necesario para leer de Render
import requests
from django.utils import timezone

def enviar_alerta_telegram(mensaje):
    """
    Envía una notificación con estilo Cyberpunk a tu Telegram.
    Extrae las llaves directamente del entorno de Render.
    """
    # 🕵️‍♂️ Cambiamos settings por os.environ para máxima seguridad
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        print("🏮 [ERROR]: No se detectaron las llaves en Render, Chummer.")
        return

    # Estética de reporte neón (Manteniendo tu estructura)
    texto = (
        f"🏮 *[OTTO-MARKET SENTINEL]*\n"
        f"----------------------------\n"
        f"🚀 {mensaje}\n"
        f"----------------------------\n"
        f"⌚ {timezone.now().strftime('%d/%m/%Y %H:%M')}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {'chat_id': chat_id, 'text': texto, 'parse_mode': 'Markdown'}

    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"❌ Error de Telegram: {response.text}")
    except Exception as e:
        print(f"Error de conexión: {e}")
