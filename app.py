from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

app = Flask(__name__)

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(credentials)

# Abrir la hoja de cálculo y seleccionar la hoja
SPREADSHEET_NAME = "Gastos"
WORKSHEET_NAME = "Hoja 1"  # Cambiar si tu hoja tiene otro nombre
sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

@app.route("/")
def home():
    return "Bot de gastos operativo!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        mensaje = request.form.get("Body")
        if not mensaje:
            return "Sin mensaje", 400

        partes = [parte.strip() for parte in mensaje.split("-")]
        if len(partes) != 3:
            return "Formato incorrecto. Usá: nombre - monto - motivo", 400

        responsable, monto, motivo = partes

        try:
            monto = float(monto.replace(",", "."))
        except ValueError:
            return "Monto inválido. Usá solo números.", 400

        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Agregar la fila a la planilla
        sheet.append_row([fecha, responsable, monto, motivo])

        return "Gasto registrado correctamente", 200

    except Exception as e:
        print(f"Error en webhook: {e}")
        return "Error interno", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
