import os
from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = set()

@sock.route("/chat")
def chat(ws):
    clients.add(ws)

    try:
        while True:
            message = ws.receive()

            if message is None:
                break

            # Gelen mesajı herkese gönder
            for client in list(clients):
                try:
                    client.send(message)
                except:
                    clients.remove(client)

    finally:
        clients.discard(ws)


@app.route("/")
def home():
    return "Chat sunucusu çalışıyor!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
