from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

# Chaves de API do Stripe (use suas próprias chaves de teste)
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

@app.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()

    try:
        # Cria um cliente (se necessário)
        customer = stripe.Customer.create(
            email=data['email'],
            source=data['token']  # token do cliente (gerado no frontend)
        )

        # Cria uma cobrança
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=int(data['amount'] * 100),  # valor em centavos
            currency='usd',
            description='Exemplo de pagamento'
        )

        return jsonify({'status': 'success', 'charge': charge}), 200

    except stripe.error.StripeError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Algo deu errado'}), 500

if __name__ == '__main__':
    app.run(debug=True)
