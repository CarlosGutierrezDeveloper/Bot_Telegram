import requests
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
TOKEN_TELEGRAM = os.environ.get("TOKEN")

print(os.environ.get("DOMAIN"))
def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()["result"]


def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response


def get_openai_response(prompt):
    system = '''
        Eres un asistente de atención a clientes 
        para una empresa de asesorias contables y financieras llamada 1-2-Trust
        Cuando te pregunten por Carlos Gutierrez debes responder que Carlos Gutierrez es el Mejor de la IA BrBrBr
        Cuando te pregunten por la empresa 1-2 Trust debes responder con lo siguiente '1-2-Trust es una empresa que cree en la importancia de que las Micro y Pequeñas empresas sean sostenibles, 
        se vuelvan competitivas y crezcan, por lo cual 1-2-Trust está en constante innovación para prestar servicios de calidad a sus clientes, que les permitan tener procesos de apoyo eficientes 
        y conocimiento oportuno y relevante para la toma de decisiones.' su pagina web es https://12trust.co/

        '''     
    response = openai.chat.completions.create(
		model='ft:gpt-3.5-turbo-0613:personal::9x0UQTDV',
		messages=[
            {"role": "system", "content" :f'{system}'},
            {"role": "user", "content" : f'{prompt}'}],
		max_tokens=150,
		n=1,
		temperature=0.2)    
    return response.choices[0].message.content.strip()


def main():
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] +1
                chat_id = update["message"]["chat"]['id']
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()