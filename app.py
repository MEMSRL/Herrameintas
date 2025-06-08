from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

herramientas = []
obras = [{"id": 0, "nombre": "Obrador Central"}]
movimientos = []

def get_obra_nombre(obra_id):
    for obra in obras:
        if obra["id"] == obra_id:
            return obra["nombre"]
    return "¿?"

@app.route('/')
def index():
    return render_template('index.html', herramientas=herramientas, obras=obras)

@app.route('/api/herramientas', methods=['GET'])
def api_listar_herramientas():
    return jsonify(herramientas)

@app.route('/api/herramienta', methods=['POST'])
def api_alta_herramienta():
    data = request.json
    herramienta = {
        "codigo": data["codigo"],
        "descripcion": data["descripcion"],
        "ubicacion": 0
    }
    herramientas.append(herramienta)
    return jsonify({"status": "ok"})

@app.route('/api/obra', methods=['POST'])
def api_alta_obra():
    data = request.json
    nueva_id = max([o["id"] for o in obras], default=0) + 1
    obras.append({"id": nueva_id, "nombre": data["nombre"]})
    return jsonify({"status": "ok"})

@app.route('/api/traslado', methods=['POST'])
def api_traslado():
    data = request.json
    codigos = data["codigos"]
    destino = int(data["destino"])
    usuario = data["usuario"]
    fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    for codigo in codigos:
        for h in herramientas:
            if h["codigo"] == codigo:
                movimientos.append({
                    "codigo": codigo,
                    "descripcion": h["descripcion"],
                    "origen": get_obra_nombre(h["ubicacion"]),
                    "destino": get_obra_nombre(destino),
                    "usuario": usuario,
                    "fecha": fecha
                })
                h["ubicacion"] = destino
    return jsonify({"status": "ok"})

@app.route('/api/obras', methods=['GET'])
def api_listar_obras():
    return jsonify(obras)

@app.route('/api/movimientos', methods=['GET'])
def api_listar_movimientos():
    return jsonify(list(reversed(movimientos)))

if __name__ == '__main__':
    app.run(debug=True)
