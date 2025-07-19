import os
import requests

MONAD_RPC_URL = os.getenv("MONAD_RPC_URL")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
THRESHOLD = float(os.getenv("THRESHOLD", "10"))  # Seuil par défaut 10 monad

def get_wallet_balance(address):
    # Exemple simple JSON-RPC request, à adapter selon l’API réelle Monad
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    try:
        response = requests.post(MONAD_RPC_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        print("Réponse JSON brute :", data)
        if 'result' in data:
            balance_wei = int(data['result'], 16)
            balance_monad = balance_wei / 1e18  # conversion Wei -> Monad
            return balance_monad
        else:
            print("Clé 'result' manquante dans la réponse.")
            return None
    except Exception as e:
        print(f"Erreur en récupérant le solde: {e}")
        return None

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        print("Message Telegram envoyé.")
    except Exception as e:
        print(f"Erreur en envoyant Telegram: {e}")

def main():
    balance = get_wallet_balance(WALLET_ADDRESS)
    if balance is None:
        print("Impossible d’obtenir le solde.")
        return
    print(f"Solde du wallet {WALLET_ADDRESS} : {balance} Monad")
    if balance > THRESHOLD:
        msg = f"Le solde du wallet a dépassé le seuil : {balance} Monad"
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
    else:
        print("Seuil non dépassé, rien à faire.")

if __name__ == "__main__":
    main()
