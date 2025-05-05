import json
import os

def guardar_evento(evento, log_file):
    try:
        if not os.path.exists(log_file):
            with open(log_file, 'w') as f:
                json.dump([], f)

        with open(log_file, 'r+') as f:
            eventos = json.load(f)
            eventos.append(evento)
            f.seek(0)
            json.dump(eventos, f, indent=2)
    except Exception as e:
        print("⚠️ Error al guardar evento:", str(e))
