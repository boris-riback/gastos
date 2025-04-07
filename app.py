from flask import Flask, request
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Flask app
app = Flask(__name__)

# Google Sheets setup
SPREADSHEET_NAME = "Gastos"
WORKSHEET_NAME = "Hoja 1"

def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_dict = json.loads(os.environ["CREDENTIALS_JSON"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(credentials)
    return client

@app.route("/", methods=["GET"])
def home():
    return "Bot de gastos activo 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        message = data["messages"][0]["body"]

        # Parsear el mensaje: "responsable - monto - motivo"
        partes = message.split(" - ")
        if len(partes) != 3:
            return "Formato incorrecto. Usá: nombre - monto - motivo", 400

        responsable, monto_str, motivo = [p.strip() for p in partes]
        try:
            monto = float(monto_str.replace(",", "."))  # admite coma o punto decimal
        except ValueError:
            return "El monto no es un número válido.", 400

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cargar a la planilla
        client = get_gspread_client()
        sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
        sheet.append_row([fecha, responsable, monto, motivo])

        return "Gasto registrado correctamente ✅", 200

    except Exception as e:
        return f"Error al procesar el webhook: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
