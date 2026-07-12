from flask import Flask
from flask_sock import Sock
import os

app = Flask(__name__)
sock = Sock(app)

clients = []

@sock.route("/chat")
def chat(ws):
    print("Yeni bağlantı geldi")

    clients.append(ws)

    try:
        while True:
            msg = ws.receive()

            if msg is None:
                break

            for client in clients:
                try:
                    client.send(msg)
                except:
                    pass

    finally:
        if ws in clients:
            clients.remove(ws)


@app.route("/")
def home():
    return "Chat sunucusu çalışıyor!"
