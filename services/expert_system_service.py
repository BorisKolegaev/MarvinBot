import os
import webbrowser
import subprocess
import glob
import time

from services.speech_to_text_service import speech_to_text_service
from services.synthesis_service import synthesis_service
from services.telegram_service import telegram_service
from services.website_service import website_service
from resources import configuration as conf


class ExpertSystemService:
    _instance = None

    def __init__(self):  # создание необходимых сервисов
        self.telegram = telegram_service()
        self.sp_to_txt = speech_to_text_service()
        self.synthesis_service = synthesis_service()

    def osrun(self, cmd):  # метод для запуска программ в операционной системе
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)

    def openurl(self, url):  # метод для открытия страниц в браузере
        webbrowser.open(url)

    def work(self, text):  # метод для обработки команд
        if "отмена" in text:
            return
        elif ("открой" in text) or ("перейди" in text):
            if ("калькулятор" in text) or ("посчитай" in text):
                self.osrun('calc')
                return
            elif ("paint" in text) or ("пэинт" in text):
                self.osrun('mspaint')
                return
            elif ("youtube" in text) or ("ютуб" in text):
                self.openurl('http://youtube.com')
                return
            elif ("сайт" in text) and ("центра" in text):
                self.openurl('https://www.untehdon.ru/')
                return
        elif ("найди" in text) or ("найти" in text):
            if ("youtube" in text) or ("ютуб" in text) or ("ютюб" in text):
                text = text.replace('найди', '')
                text = text.replace('ютуб', '')
                text = text.replace('ютюб', '')
                text = text.replace('в интернете', '')
                text = text.strip()
                self.openurl('https://www.youtube.com/results?search_query=' + text)
                return
            text = text.replace('найди', '')
            text = text.replace('ютуб', '')
            text = text.replace('в интернете', '')
            text = text.strip()
            self.openurl('https://www.google.com/search?q=' + text)
            return

        elif "создай" in text:
            dir_name = self.sp_to_txt.speech_to_text("ADD_DIR")
            os.mkdir(conf.DOCUMENTS_DIR + "/" + dir_name)
            return

        elif ("добавь" in text) or ("новость" in text):
            website = website_service()
            website.create_new_post()

        elif ("файл" in text) or ("перенеси" in text):
            list_of_files = glob.glob(conf.DOWNLOADS_DIR + "/*")
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)

            latest_file_updated = latest_file.replace("//", "\\")
            os.rename(latest_file_updated, latest_file_updated.replace(" ", "_"))
            print(latest_file_updated)
            os.popen("move " + latest_file_updated.replace(" ", "_") + " " + conf.DOCUMENTS_DIR)
            return

        elif "выход" in text:
            raise SystemExit

        else:  # В том случае если команда не найдена, отправить ее к GPT-3 боту и произнести ответ
            self.telegram.send_message_to_gpt3(text)
            time.sleep(4)
            answ = self.telegram.get_last_message_from_gpt3()
            self.synthesis_service.speak(answ)


def expert_system_service():
    if ExpertSystemService._instance is None:
        ExpertSystemService._instance = ExpertSystemService()
    return ExpertSystemService._instance
