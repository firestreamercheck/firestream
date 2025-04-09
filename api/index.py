from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Dicionário com chaves de exemplo
LICENSAS = {
    "ABC123": {"ativa_em": "2024-12-10", "dias_validade": 10},
    "XYZ789": {"ativa_em": "2025-04-01", "dias_validade": 30},
}

@app.route("/", methods=["GET"])
def root():
    return "API de Licenciamento Online"

@app.route("/verificar_licenca", methods=["POST"])
def verificar_licenca():
    data = request.get_json()
    chave = data.get("chave")

    if chave in LICENSAS:
        info = LICENSAS[chave]
        ativacao = datetime.strptime(info["ativa_em"], "%Y-%m-%d")
        dias = info["dias_validade"]
        dias_usados = (datetime.now() - ativacao).days
        valido = dias_usados <= dias

        return jsonify({
            "valido": valido,
            "dias_restantes": max(dias - dias_usados, 0)
        })
    else:
        return jsonify({"valido": False}), 401
