from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime
import os

app = Flask(__name__)

# Ruta al archivo de credenciales
CREDENTIALS_FILE = "credenciales/credenciales.json"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Abrir planilla de gastos
sheet = client.open("Gastos diarios").sheet1

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    mensaje = data.get("mensaje", "")

    partes = mensaje.split(" - ")
    if len(partes) != 3:
        return {"status": "error", "mensaje": "Formato incorrecto. Usá: nombre - monto - motivo"}

    responsable = partes[0].strip()
    monto = partes[1].strip()
    motivo = partes[2].strip()
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fila = [fecha_hora, responsable, monto, motivo]
    sheet.append_row(fila)

    return {"status": "ok", "mensaje": "Gasto registrado correctamente"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
