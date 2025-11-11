from config import UMBRAL_NORMAL, UMBRAL_EXTREMO, UMBRAL_NORMAL_CRYPTO, UMBRAL_EXTREMO_CRYPTO

def check_alerts(summary: dict):
    """
    Genera alertas cuando se superan los umbrales.
    Se diferencian índices / commodities de criptos.
    """
    alerts = []

    for name, data in summary.items():
        if not data or "variacion_pct" not in data:
            continue

        change = data["variacion_pct"]

        # Diferencia umbrales según tipo de activo
        if name in ["Bitcoin", "Plata"]:
            normal = UMBRAL_NORMAL_CRYPTO
            extreme = UMBRAL_EXTREMO_CRYPTO
        else:
            normal = UMBRAL_NORMAL
            extreme = UMBRAL_EXTREMO

        if abs(change) >= extreme:
            emoji = "🚨" if change < 0 else "🚀"
            alerts.append(f"{emoji} *{name}* ha cambiado un {change:.2f}% hoy (movimiento extremo).")
        elif abs(change) >= normal:
            emoji = "🔻" if change < 0 else "📈"
            alerts.append(f"{emoji} *{name}* se ha movido un {change:.2f}% hoy.")

    return alerts