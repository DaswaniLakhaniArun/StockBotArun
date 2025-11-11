import yfinance as yf
from datetime import datetime, timezone

def get_price_data(ticker: str):
    """
    Obtiene los dos últimos precios de cierre diarios del activo
    y calcula la variación porcentual entre ellos.

    Parámetros:
        ticker (str): Símbolo del activo (por ejemplo, '^GSPC', 'BTC-EUR').

    Retorna:
        tuple (precio_actual, precio_anterior, variacion_pct)
        o None si los datos no están disponibles.
    """
    try:
        data = yf.Ticker(ticker)
        hist = data.history(period="2d")
        if len(hist) < 2:
            print(f"⚠️ No hay suficientes datos para {ticker}")
            return None

        hoy = hist.iloc[-1]
        ayer = hist.iloc[-2]

        precio = float(hoy["Close"])
        precio_anterior = float(ayer["Close"])
        variacion = (precio - precio_anterior) / precio_anterior * 100

        return round(precio, 2), round(precio_anterior, 2), round(variacion, 2)
    except Exception as e:
        print(f"❌ Error al obtener datos diarios de {ticker}: {e}")
        return None


def get_intraday_change(ticker: str):
    """
    Obtiene el movimiento intradía (intervalo de 1 minuto) del activo
    para el día actual. Útil para ver la variación mientras el mercado está abierto.

    Parámetros:
        ticker (str): Símbolo del activo (por ejemplo, '^IXIC', 'GC=F').

    Retorna:
        tuple (precio_apertura, precio_actual, variacion_pct)
        o None si los datos no están disponibles.
    """
    try:
        data = yf.Ticker(ticker)
        hist = data.history(interval="1m", period="1d")
        if hist.empty:
            print(f"⚠️ No hay datos intradía disponibles para {ticker}")
            return None

        precio_apertura = float(hist.iloc[0]["Open"])
        precio_actual = float(hist.iloc[-1]["Close"])
        variacion = (precio_actual - precio_apertura) / precio_apertura * 100

        return round(precio_apertura, 2), round(precio_actual, 2), round(variacion, 2)
    except Exception as e:
        print(f"❌ Error al obtener datos intradía de {ticker}: {e}")
        return None


def get_market_status():
    """
    Devuelve el estado aproximado (abierto o cerrado) de los principales mercados
    según la hora actual en UTC. Útil para mostrar en el resumen del bot.

    Retorna:
        dict con los mercados y su estado (🟢 Abierto / 🔴 Cerrado)
    """
    ahora_utc = datetime.now(timezone.utc)
    hora = ahora_utc.hour

    # Horarios de referencia aproximados (UTC)
    mercados = {
        "NYSE": {"apertura": 14, "cierre": 21},
        "NASDAQ": {"apertura": 14, "cierre": 21},
        "LSE (Londres)": {"apertura": 8, "cierre": 16},
        "XETRA (Alemania)": {"apertura": 8, "cierre": 16},
    }

    estado = {}
    for nombre, horas in mercados.items():
        if horas["apertura"] <= hora < horas["cierre"]:
            estado[nombre] = "🟢 Abierto"
        else:
            estado[nombre] = "🔴 Cerrado"

    return estado