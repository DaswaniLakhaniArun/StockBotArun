from datetime import datetime

def build_summary(summary: dict, title: str = "Resumen de mercados"):
    """
    Construye un mensaje bonito para Telegram con los precios y variaciones.
    
    Args:
        summary (dict): Diccionario con los datos de los activos.
        title (str): Título del mensaje.
    
    Returns:
        str: Mensaje listo para enviar a Telegram.
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    message = f"📊 *{title}* ({now})\n\n"

    for name, data in summary.items():
        if not data:
            message += f"• {name}: ❌ Datos no disponibles\n"
            continue

        price = data.get("precio", "N/A")
        change = data.get("variacion_pct", 0)

        # Emoji según la variación
        if change > 0:
            emoji = "📈"
        elif change < 0:
            emoji = "🔻"
        else:
            emoji = "⚪️"

        message += f"• {name}: {price} EUR ({emoji} {change:+.2f}%)\n"

    return message