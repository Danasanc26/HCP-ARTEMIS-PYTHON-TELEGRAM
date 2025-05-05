from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
import time


app = Flask(__name__)
LOG_FILE = "eventos_recibidos.json"

# Ruta que coincide con el valor de `eventDest` usado en la suscripción
@app.route('/casa', methods=['POST'])
def recibir_evento():
    print("🔔 Evento recibido de HikCentral")

    try:
        # Intenta leer JSON del cuerpo
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()
        if not data:
            data = request.data.decode()

        evento = {
            "timestamp": datetime.now().isoformat(),
            "contenido": data
        }

        # Mostrar en consola
        print("📦 Datos del evento:")
        print(json.dumps(evento, indent=2))

        evento_status = data["params"]["events"][0]["status"]

        if evento_status == 1:
                #Guardar en archivo JSON
                guardar_evento(evento)
                print("Evento de inicio procesado")
        else:
                print(f"⚠️ Evento recibido con status {evento_status}, no procesado")

        return jsonify({"status": "ok", "message": "Evento recibido correctamente"}), 200

    except Exception as e:
        print("❌ Error al procesar evento:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    
# Guardar evento en archivo JSON
def guardar_evento(evento):
    try:
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)

        with open(LOG_FILE, 'r+') as f:
            eventos = json.load(f)
            eventos.append(evento)
            f.seek(0)
            json.dump(eventos, f, indent=2)
    except Exception as e:
        print("⚠️ Error al guardar evento:", str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

