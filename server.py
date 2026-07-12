import os
from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []

@sock.route("/chat")
def chat(ws):
    clients.append(ws)
    try:
        while True:
            msg = ws.receive()
            if msg is None:
                break

            for c in clients.copy():
                try:
                    c.send(msg)
                except:
                    clients.remove(c)
    finally:
        if ws in clients:
            clients.remove(ws)

@app.route("/")
def index():
    return "Chat sunucusu çalışıyor!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
