import asyncio
import threading
import json
import os
import schedule
import time
from flask import Flask
from datetime import datetime, timezone, timedelta
from config import BOT, CHAT_ID, ASSETS
from utils.data import get_price_data, get_intraday_data
from utils.alerts import check_alerts
from utils.summary import build_summary

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Finance Bot is running!"


# ======== CONFIGURACIÓN DE MERCADOS ======== #
# Europa y EE.UU. agrupados para evitar duplicados
MARKETS = {
    "Europa (LSE & XETRA)": (8, 16),
    "EE.UU. (NYSE & NASDAQ)": (14, 21)
}

# Estado de apertura/cierre de cada grupo de mercado
market_state = {market: False for market in MARKETS}

# Activos con actualización intradía
INTRADAY_ASSETS = ["Bitcoin", "Oro", "Plata"]

STATE_FILE = "data/state.json"


# ======== FUNCIONES AUXILIARES ======== #
def reset_state_daily():
    """Vacía el archivo state.json cada día antes de la apertura del mercado."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            json.dump({}, f)
        print("🧹 Estado reseteado automáticamente antes de la apertura de mercado.")
    else:
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump({}, f)
        print("🧹 state.json creado y reseteado por primera vez.")


def run_schedule():
    """Ejecuta las tareas programadas en un hilo separado."""
    while True:
        schedule.run_pending()
        time.sleep(60)


# Configurar el reseteo diario a las 08:00 hora Madrid (07:00 UTC)
schedule.every().day.at("07:00").do(reset_state_daily)
threading.Thread(target=run_schedule, daemon=True).start()


# ======== BUCLE PRINCIPAL DEL BOT ======== #
async def bot_loop():
    while True:
        summary = {}

        # Obtener datos de los activos
        for name, ticker in ASSETS.items():
            if name in INTRADAY_ASSETS:
                data = get_intraday_data(ticker)
                if data:
                    summary[name] = {
                        "precio": data["actual"],
                        "precio_anterior": data["apertura"],
                        "variacion_pct": data["variacion_intradia"]
                    }
            else:
                data = get_price_data(ticker)
                if data:
                    summary[name] = data

        # Comprobar alertas
        alerts = check_alerts(summary)
        for alert in alerts:
            await BOT.send_message(chat_id=CHAT_ID, text=alert)

        # Determinar hora actual (UTC)
        now = datetime.utcnow()
        current_hour = now.hour

        # Comprobar apertura/cierre de mercados
        for market, (open_hour, close_hour) in MARKETS.items():
            if open_hour <= current_hour < close_hour and not market_state[market]:
                market_state[market] = True
                msg = f"🟢 *{market}* ha abierto los mercados.\n"
                msg += build_summary(summary, title="Precios de apertura")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

            elif (current_hour >= close_hour or current_hour < open_hour) and market_state[market]:
                market_state[market] = False
                msg = f"🔴 *{market}* ha cerrado los mercados.\n"
                msg += build_summary(summary, title="Precios de cierre")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

        await asyncio.sleep(60)


# ======== EJECUCIÓN PRINCIPAL ======== #
def run_bot():
    asyncio.run(bot_loop())


if __name__ == "__main__":
    # Enviar mensaje de prueba al iniciar
    try:
        BOT.send_message(chat_id=CHAT_ID, text="✅ Bot iniciado correctamente en Render 🚀")
    except Exception as e:
        print(f"❌ Error al enviar el mensaje de prueba: {e}")

    # Ejecutar el bot en un hilo aparte
    threading.Thread(target=run_bot).start()

    # Mantener Flask activo para Render
    app.run(host="0.0.0.0", port=10000)