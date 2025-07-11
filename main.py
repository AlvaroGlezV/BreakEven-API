from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/maxprice', methods=['POST'])
def calculate_max_price():
    data = request.json
    try:
        renta = float(data['renta'])
        expenses = float(data['expenses'])  # taxes + insurance
    except (KeyError, ValueError):
        return jsonify({'error': 'Debes enviar los campos renta y expenses como números'}), 400

    # Parámetros fijos
    tasa_anual = 0.07
    amortizacion = 30
    porcentaje_gastos = 0.2  # 20% operativos
    enganche = 0.2  # 20% de down payment

    # Cálculo
    renta_neta = renta * (1 - porcentaje_gastos)
    pago_max = renta_neta - expenses
    r = tasa_anual / 12
    n = amortizacion * 12

    # Fórmula para el préstamo máximo
    if pago_max <= 0:
        return jsonify({'max_price': 0, 'mensaje': 'El cashflow sería negativo con estos datos'})

    numerador = (1 + r) ** n - 1
    denominador = r * (1 + r) ** n
    L = pago_max * numerador / denominador
    precio_max = L / (1 - enganche)

    return jsonify({
        'max_price': round(precio_max, 2),
        'details': {
            'pago_max': round(pago_max, 2),
            'loan_amount': round(L, 2),
            'params': {'renta': renta, 'expenses': expenses}
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
