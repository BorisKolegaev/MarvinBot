import speech_recognition as sr

from services.synthesis_service import synthesis_service


class SpeechToTextService:
    _instance = None

    def __init__(self):
        self.synth = synthesis_service()
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

    def speech_to_text(self, CONTEXT):
        text = "pass"
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        if CONTEXT == "USUAL":  # отклик, если контекст фразы обычный
            self.synth.speak_enter_word()
        elif CONTEXT == "ADD_DIR":  # если необходимо уточнение - название папки
            self.synth.speak_add_dir_word()
        with self._microphone as source:
            audio = self._recognizer.listen(source)
        self.synth.speak_control_word()  # отклик от ассистента, завешающий взаимодействие

        #  -------------------  Распознавание речи на серверах Google
        try:
            text = self._recognizer.recognize_google(audio, language="ru_RU")
        except sr.UnknownValueError:
            print("Фраза не выявлена")
        except sr.RequestError as e:
            print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))
        text = text.lower()
        return text


def speech_to_text_service():
    if SpeechToTextService._instance is None:
        SpeechToTextService._instance = SpeechToTextService()
    return SpeechToTextService._instance
