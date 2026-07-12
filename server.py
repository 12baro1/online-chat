from flask import Flask
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

clients = []

@sock.route('/chat')
def chat(ws):
    clients.append(ws)
    try:
        while True:
            message = ws.receive()
            if message is None:
                break
            for client in clients[:]:
                try:
                    client.send(message)
                except:
                    if client in clients:
                        clients.remove(client)
    finally:
        if ws in clients:
            clients.remove(ws)

@app.route("/")
def home():
    return "Chat sunucusu çalışıyor."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)