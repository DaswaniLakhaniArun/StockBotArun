import asyncio
import threading
from flask import Flask
from datetime import datetime
from config import BOT, CHAT_ID, ASSETS
from utils.data import get_price_data, get_intraday_data
from utils.alerts import check_alerts
from utils.summary import build_summary

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Finance Bot is running!"

markets = ["NYSE (EE.UU.)", "NASDAQ (EE.UU.)", "LSE (Londres)", "XETRA (Alemania)"]
market_state = {market: False for market in markets}

market_schedule = {
    "NYSE (EE.UU.)": (14, 21),
    "NASDAQ (EE.UU.)": (14, 21),
    "LSE (Londres)": (8, 16),
    "XETRA (Alemania)": (8, 16),
}

INTRADAY_ASSETS = ["Bitcoin", "Oro", "Plata"]

async def bot_loop():
    while True:
        summary = {}
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

        alerts = check_alerts(summary)
        for alert in alerts:
            await BOT.send_message(chat_id=CHAT_ID, text=alert)

        now = datetime.utcnow()
        current_hour = now.hour

        for market, (open_hour, close_hour) in market_schedule.items():
            if open_hour <= current_hour < close_hour and not market_state[market]:
                market_state[market] = True
                msg = f"🟢 *{market}* ha abierto.\n"
                msg += build_summary(summary, title="Precios de apertura")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

            elif (current_hour >= close_hour or current_hour < open_hour) and market_state[market]:
                market_state[market] = False
                msg = f"🔴 *{market}* ha cerrado.\n"
                msg += build_summary(summary, title="Precios de cierre")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

        await asyncio.sleep(60)

def run_bot():
    asyncio.run(bot_loop())

if __name__ == "__main__":
    # Enviar mensaje de prueba
    try:
        BOT.send_message(chat_id=CHAT_ID, text="✅ Bot iniciado correctamente en Render 🚀")
    except Exception as e:
        print(f"❌ Error al enviar el mensaje de prueba: {e}")

    # Ejecutar el bot en un hilo aparte
    threading.Thread(target=run_bot).start()

    # Iniciar Flask para mantener el servicio activo
    app.run(host="0.0.0.0", port=10000)