import os
import time
import requests
import telegram

def main():
    chat_id = os.getenv('CHAT_ID')
    devman_token = os.getenv('DEVMAN_TOKEN')
    bot_token = os.getenv("BOT_TOKEN")
    bot = telegram.Bot(token=bot_token)
    url = "https://dvmn.org/api/long_polling/"
    headers = {"Authorization": f"Token {devman_token}"}
    timestamp = None


    while True:
        payload = {"timestamp": timestamp}
        response = requests.get(url, params=payload, headers=headers)
        response_file = response.json()
        try:
            response.raise_for_status()
            status = response_file["status"]

            if status == "found":
                timestamp = response_file["last_attempt_timestamp"]
                last_attempt = response_file["new_attempts"][0]
                lesson_title = last_attempt["lesson_title"]
                if last_attempt["is_negative"]:
                    bot.send_message(chat_id=chat_id, text=f"У вас проверили работу {lesson_title}.К сожалению, в работе нашлись ошибки")
                else:
                    bot.send_message(chat_id=chat_id, text=f"У вас проверили работу {lesson_title}.Преподавателю всё понравилось, можно приступать к следущему уроку!")
            if status == "timeout":
              timestamp = response_file["timestamp_to_request"]

        except ConnectionError:
            print("Ошибка")
            time.sleep(3600)
        except requests.exceptions.ReadTimeout:
            print("Ошибка")


if __name__ == '__main__':
    main()
        