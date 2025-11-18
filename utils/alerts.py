import json
import os
from config import UMBRAL_NORMAL, UMBRAL_EXTREMO, UMBRAL_NORMAL_CRYPTO, UMBRAL_EXTREMO_CRYPTO

STATE_FILE = "data/state.json"

def load_state():
    """Carga el estado previo desde state.json."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_state(state):
    """Guarda el estado actual en state.json."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def check_alerts(data_dict):
    """
    Revisa los cambios en los activos y genera alertas solo una vez por cruce de umbral.
    """
    alerts = []
    state = load_state()

    for name, data in data_dict.items():
        variacion = data.get("variacion_pct", 0)

        # Detectar si es cripto o activo normal
        is_crypto = "Bitcoin" in name
        umbral_normal = UMBRAL_NORMAL_CRYPTO if is_crypto else UMBRAL_NORMAL
        umbral_extremo = UMBRAL_EXTREMO_CRYPTO if is_crypto else UMBRAL_EXTREMO
        
        previous_state = state.get(name, "neutral")
        
        # --- Condiciones de alerta ---
        if variacion >= umbral_extremo and previous_state != "up_extreme":
            alerts.append(f"🚀 *{name}* sube un {variacion:.2f}% hoy (nivel EXTREMO).")
            state[name] = "up_extreme"
        
        elif umbral_normal <= variacion < umbral_extremo and previous_state != "up":
            alerts.append(f"📈 *{name}* sube un {variacion:.2f}% hoy.")
            state[name] = "up"
        
        elif variacion <= -umbral_extremo and previous_state != "down_extreme":
            alerts.append(f"💥 *{name}* cae un {variacion:.2f}% hoy (nivel EXTREMO).")
            state[name] = "down_extreme"
        
        elif -umbral_extremo < variacion <= -umbral_normal and previous_state != "down":
            alerts.append(f"📉 *{name}* cae un {variacion:.2f}% hoy.")
            state[name] = "down"
        
        # --- Reset del estado cuando vuelve a la normalidad ---
        elif -umbral_normal < variacion < umbral_normal and previous_state != "neutral":
            state[name] = "neutral"
        
        save_state(state)
        return alerts