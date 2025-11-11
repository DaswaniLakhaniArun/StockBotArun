import asyncio
from datetime import datetime
from config import BOT, CHAT_ID, ASSETS
from utils.data import get_price_data, get_intraday_data
from utils.alerts import check_alerts
from utils.summary import build_summary

# Estado de cada bolsa (True = abierta)
markets = ["NYSE (EE.UU.)", "NASDAQ (EE.UU.)", "LSE (Londres)", "XETRA (Alemania)"]
market_state = {market: False for market in markets}

# Horarios de apertura/cierre UTC
market_schedule = {
    "NYSE (EE.UU.)": (14, 21),
    "NASDAQ (EE.UU.)": (14, 21),
    "LSE (Londres)": (8, 16),
    "XETRA (Alemania)": (8, 16),
}

# Activos que usan intradía (crypto, oro, plata)
INTRADAY_ASSETS = ["Bitcoin", "Oro", "Plata"]

async def main():
    while True:
        # --- 1. Obtener datos ---
        summary = {}
        for name, ticker in ASSETS.items():
            if name in INTRADAY_ASSETS:
                data = get_intraday_data(ticker)
                # Renombramos campos para coherencia con summary.py
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

        # --- 2. Enviar alertas ---
        alerts = check_alerts(summary)
        for alert in alerts:
            await BOT.send_message(chat_id=CHAT_ID, text=alert)

        # --- 3. Apertura / cierre de bolsas ---
        now = datetime.utcnow()
        current_hour = now.hour

        for market, (open_hour, close_hour) in market_schedule.items():
            if open_hour <= current_hour < close_hour and not market_state[market]:
                # Bolsa acaba de abrir
                market_state[market] = True
                msg = f"🟢 *{market}* ha abierto.\nPrecios de apertura:\n"
                msg += build_summary(summary, title="Precios de apertura")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

            elif (current_hour >= close_hour or current_hour < open_hour) and market_state[market]:
                # Bolsa acaba de cerrar
                market_state[market] = False
                msg = f"🔴 *{market}* ha cerrado.\nPrecios de cierre:\n"
                msg += build_summary(summary, title="Precios de cierre")
                await BOT.send_message(chat_id=CHAT_ID, text=msg)

        await asyncio.sleep(60)  # Revisa cada minuto

if __name__ == "__main__":
    asyncio.run(main())