import yfinance as yf

def get_price_data(ticker):
    """Obtiene el precio y variación diaria de un activo."""
    data = yf.Ticker(ticker)
    hist = data.history(period="2d")
    if len(hist) < 2:
        return None

    today = hist.iloc[-1]
    yesterday = hist.iloc[-2]
    
    price = round(today["Close"], 2)
    prev_close = round(yesterday["Close"], 2)
    change_pct = (price - prev_close) / prev_close * 100
    
    return {
        "precio": price,
        "precio_anterior": prev_close,
        "variacion_pct": change_pct
    }

def get_intraday_data(ticker):
    """Obtiene la variación intradía (precio actual vs apertura)."""
    data = yf.Ticker(ticker)
    hist = data.history(interval="5m", period="1d")
    if len(hist) == 0:
        return None

    open_price = round(hist.iloc[0]["Open"], 2)
    current_price = round(hist.iloc[-1]["Close"], 2)
    change_pct = (current_price - open_price) / open_price * 100

    return {
        "apertura": open_price,
        "actual": current_price,
        "variacion_intradia": change_pct
    }