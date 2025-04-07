from flask import Flask, request
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Twilio manda los datos en form-urlencoded
    msg_body = request.form.get('Body')
    
    if msg_body:
        now = datetime.datetime.now()
        fecha = now.strftime("%d/%m/%Y %H:%M")

        # Formato esperado: "Sofi - 2400 - Mercado"
        partes = msg_body.split(" - ")
        if len(partes) == 3:
            responsable, monto, motivo = partes
            # Conectamos a la planilla
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
            sheet

