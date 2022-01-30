import requests
import codecs
from resources import configuration as conf


class Website_service():
    _instance = None

    def create_new_post(self):  # публикация новой новости на сайте
        url = 'http://localhost:5000/admin'  # URL вебсайта (проект Website)

        #  заголовок новости берется из файла resources/website/title.txt

        with codecs.open(conf.RESOURCES_DIR + '\website\\title.txt', 'r', encoding='utf8') as f:
            title = f.read()

        #  текст новости берется из файла resources/website/text.txt

        with codecs.open(conf.RESOURCES_DIR + '\website\\text.txt', 'r', encoding='utf8') as f:
            text = f.read()

        print(title)
        print(text)

        # --------------------------------  формирование запроса
        myobj = {'title': title,
                 'text': text
        }

        x = requests.post(url, data=myobj)  # отправка запроса

        print(x.text)


def website_service():
    if Website_service._instance is None:
        Website_service._instance = Website_service()
    return Website_service._instance
