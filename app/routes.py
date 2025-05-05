from flask import Blueprint, request, jsonify
from datetime import datetime
import json
from .utils import guardar_evento

main = Blueprint('main', __name__)
LOG_FILE = "eventos_recibidos.json"

@main.route('/casa', methods=['POST'])
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
            guardar_evento(evento, LOG_FILE)
            print("Evento de inicio procesado")
        else:
            print(f"⚠️ Evento recibido con status {evento_status}, no procesado")

        return jsonify({"status": "ok", "message": "Evento recibido correctamente"}), 200

    except Exception as e:
        print("❌ Error al procesar evento:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
