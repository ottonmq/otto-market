import requests
from django.conf import settings
from django.utils import timezone

def enviar_alerta_telegram(mensaje):
    """
    Envía una notificación con estilo Cyberpunk a tu Telegram.
    """
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Estética de reporte neón
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
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error de conexión: {e}")
