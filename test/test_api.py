from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
LOG_FILE = "eventos_recibidos.json"

@app.route('/casa', methods=['POST'])
def recibir_evento():
    print("🔔 Evento recibido de HikCentral")
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or request.data.decode()
        
        evento = {
            "timestamp": datetime.now().isoformat(),
            "contenido": data
        }

        print("📦 Datos del evento:")
        print(json.dumps(evento, indent=2))

        procesar_evento(evento)
        
        return jsonify({"status": "ok", "message": "Evento recibido correctamente"}), 200

    except Exception as e:
        print("❌ Error al procesar evento:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

def procesar_evento(evento):
    """ Procesa el evento recibido """
    try:
        evento_status = evento['contenido']["params"]["events"][0]["status"]
        
        if evento_status == 1:
            guardar_evento(evento)
            print("✅ Evento de inicio procesado")
            # Aquí futuro: enviar foto por Telegram
        else:
            print(f"⚠️ Evento recibido con status {evento_status}, no procesado")

    except Exception as e:
        print(f"⚠️ Error al procesar evento: {e}")

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
        print(f"⚠️ Error al guardar evento: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
