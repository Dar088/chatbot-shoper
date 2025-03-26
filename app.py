import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Klucz API OpenAI (należy go przechowywać w bezpieczny sposób)
OPENAI_API_KEY = "your-openai-api-key"

def get_chatbot_response(user_input):
    faq_knowledge = """
    1. Jeśli nie widzisz aktualnych danych w aplikacji z żółtą pszczołą, sprawdź:
       - Czy bramka GSM znajduje się blisko urządzeń.
       - Czy aplikacja z zieloną pszczołą ma dostęp do uprawnień telefonu (Bluetooth, lokalizacja, internet).
       - Jeśli problem nie ustępuje, wyłącz aplikację, wyłącz Bluetooth i lokalizację, zrestartuj telefon i spróbuj ponownie.
    
    2. Bramka GSM:
       - Jeśli masz nową bramkę, upewnij się, że aktywowałeś kartę SIM.
       - Sprawdź, czy karta SIM jest prawidłowo włożona (Mikro SIM).
       - Jeśli bramka nie synchronizuje danych, sprawdź poziom naładowania baterii oraz aktywny transfer danych.
    
    3. Serce Ula:
       - Jeśli urządzenie nie działa, sprawdź poziom baterii w aplikacji.
       - Po wymianie baterii sprawdź, czy nowa jest sprawna.
       - Jeśli problem nie ustępuje, zrestartuj urządzenie, wyciągając baterię na 30 sekund.
    
    4. Waga:
       - Jeśli waga nie działa, skontaktuj się z obsługą klienta.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym chatbotem dla sklepu internetowego serceula.pl. Odpowiadasz na pytania o użytkowanie produktu i jego połączenie z aplikacją mobilną."},
            {"role": "user", "content": user_input},
            {"role": "system", "content": faq_knowledge}
        ]
    )
    return response["choices"][0]["message"]["content"]

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Brak wiadomości"}), 400
    
    bot_response = get_chatbot_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
