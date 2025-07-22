from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import logging

app = Flask(__name__)
CORS(app)

# Configuración de logs
logging.basicConfig(level=logging.INFO)

# Cargar archivo de recomendaciones
try:
    with open('recomendaciones.pkl', 'rb') as f:
        recomendaciones = pickle.load(f)
        # Limpiar espacios en los nombres de productos
        recomendaciones = {k.strip(): v for k, v in recomendaciones.items()}
    logging.info("recomendaciones.pkl cargado correctamente.")
except Exception as e:
    recomendaciones = {}
    logging.error(f"❌ Error al cargar recomendaciones.pkl: {e}")

@app.route('/')
def home():
    return """
    <html>
    <head><title>API de Recomendaciones</title></head>
    <body style="font-family:Arial;margin:40px">
        <h2>API de Recomendaciones</h2>
        <p>Haz una solicitud <code>POST</code> a <code>/recomendar</code> con un JSON como:</p>
        <pre>{ "producto": "Filipina Naranja" }</pre>
    </body>
    </html>
    """

@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        data = request.get_json(force=True)
        producto = data.get('producto')

        if not producto:
            return jsonify({"error": "Debes proporcionar el campo 'producto'."}), 400

        producto = producto.strip()
        sugerencias = recomendaciones.get(producto, [])

        return jsonify({
            "producto": producto,
            "recomendaciones": sugerencias  # Siempre regresa un array
        }), 200

    except Exception as e:
        logging.error(f"❌ Error en /recomendar: {e}")
        return jsonify({"error": "Error al procesar la solicitud."}), 500

if __name__ == '__main__':
    app.run(debug=True)
