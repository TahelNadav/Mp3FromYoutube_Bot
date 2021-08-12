



from flask import Flask, request, Response

import requests
from telegram.bot import *

import controller

TOKEN = '1846481971:AAEhcOBGX7mvpFvrQGl32HN0iX9R3-aXU4A'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://6a32fc616edf.ngrok.io/message'.format(TOKEN)

requests.get(TELEGRAM_INIT_WEBHOOK_URL)

app = Flask(__name__)



@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    msg_from_user = request.get_json()['message']['text']#link of video in youtube
    mp3_path=controller.app_controller.download_and_convert(msg_from_user)

    with open(mp3_path, 'rb') as audio:
        payload = {
            'chat_id': chat_id,

        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=TOKEN),
            data=payload,
            files=files).json()
    return Response("success")


@app.route('/sanity')
def sanity():return "Server is running"

