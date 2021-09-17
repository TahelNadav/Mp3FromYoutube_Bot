import re
from flask import Flask, request, Response
import requests
import controller

TOKEN = ''
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url=https://eba5e4f615d2.ngrok.io/message'.format(
    TOKEN)
requests.get(TELEGRAM_INIT_WEBHOOK_URL)
app = Flask(__name__)


@app.route('/message', methods=["POST"])
def handle_message():
    """
    A function that get message from user and responds accordingly.
    If the user send link of video in youtube, the bot send mp3 file of this video.
    else, the bot offers videos that appropriate to the user message and the user choose one of them
    and the bot send mp3 file of this video.
    """
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    msg_from_user = request.get_json()['message']['text']  # link of video in youtube

    if msg_from_user == '/start':
        msg_to_send = 'Welcome to Mp3FromYouTube bot! \n' \
                      'You can submit a video link on YouTube for download. \n ' \
                      'You can submit a value for search on youtube and you will receive suggestion videos that match ' \
                      'your search \n' \
                      "For new search send /new"

        res = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                           .format(TOKEN, chat_id, msg_to_send))
        return Response("success")

    # If the user send '/new' - restart the bot
    elif msg_from_user == "/new":
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                     .format(TOKEN, chat_id, 'Enter a new value'))
        controller.app_controller.num_flag = False
        return Response("success")

    # If the user select a video to download
    elif controller.app_controller.num_flag and msg_from_user.isdigit():
        # If the user choose a incorrect num video
        if int(msg_from_user) > len(controller.app_controller.lst_results):
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                         .format(TOKEN, chat_id, "Select a correct number video"))
            return Response("success")
        # The link of the video
        link = "https://www.youtube.com/watch?v=" + controller.app_controller.lst_results[int(msg_from_user) - 1]
        msg_from_user = link
        controller.app_controller.num_flag = False

    # Try to download the video
    try:
        mp3_path = controller.app_controller.download_and_convert(msg_from_user)
        msg_from_user = ''
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                     .format(TOKEN, chat_id, "Download...."))
        # Send the mp3 file
        with open(mp3_path, 'rb') as audio:
            payload = {'chat_id': chat_id, }
            files = {'audio': audio.read(), }
        resp = requests.post(
            "https://api.telegram.org/bot{token}/sendAudio".format(token=TOKEN),
            data=payload,
            files=files).json()
        return Response("success")

    # If the user give invalid link, we send you videos that appropriate to the input
    except:
        # Dict with the results - name and link
        dic_results = controller.app_controller.search_by_keyword(msg_from_user)
        # A string of the result to send to the user
        lst_for_client = ""
        i = 1
        # A list with the results
        controller.app_controller.lst_results = []
        for key in dic_results.keys():
            controller.app_controller.lst_results += [key]
            temp = dic_results[key].split('|')[0]
            lst_for_client = lst_for_client + str(
                i) + ". " + temp + '\n' + "https://www.youtube.com/watch?v=" + key + '\n'
            i += 1
        lst_for_client = re.sub('[!@#$&#;]', '', lst_for_client)
        # Send the results to the user
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                     .format(TOKEN, chat_id, lst_for_client))
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'"
                     .format(TOKEN, chat_id, "Select a video to download by enter the number of video"))
        controller.app_controller.num_flag = True

    return Response("success")
