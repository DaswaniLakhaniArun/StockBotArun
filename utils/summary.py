import datetime

def build_summary(summary):
    fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    mensaje = f"📊 *Resumen diario de mercados* ({fecha})\n\n"
    for name, data in summary.items():
        if data:
            mensaje += f"• {name}: {data['price']} EUR → {data['change']:+.2f}%\n"
        else:
            mensaje += f"• {name}: No hay datos disponibles\n"
    return mensaje