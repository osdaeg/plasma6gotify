#!/usr/bin/env python3
import websocket
import json
import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/scripts/gotify_notify/gotify_notify.env"))

GOTIFY_URL = os.getenv("GOTIFY_URL")
TOKEN = os.getenv("GOTIFY_TOKEN")

#print(GOTIFY_URL)
#print(TOKEN)

def on_message(ws, message):
    data = json.loads(message)
    title = data.get("title", "Gotify")
    body = data.get("message", "")
    priority = data.get("priority", 5)

    if priority <= 3:
        urgency = "low"
    elif priority <= 7:
        urgency = "normal"
    else:
        urgency = "critical"

    subprocess.run([
        "notify-send",
        "--urgency", urgency,
        "--icon", "dialog-information",
        "--app-name", "Gotify",
        title,
        body
    ])

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Conexión cerrada, reconectando...")

while True:
    try:
        ws = websocket.WebSocketApp(
            f"{GOTIFY_URL}?token={TOKEN}",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()
    except Exception as e:
        print(f"Excepción: {e}")
    time.sleep(5)
