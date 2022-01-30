# coding=utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDesktopWidget

from services.expert_system_service import expert_system_service
from services.speech_to_text_service import speech_to_text_service


class App(QWidget):

    def __init__(self):
        super().__init__()

        self.exp_sys = expert_system_service()
        self.sp_to_txt = speech_to_text_service()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # не скрывать окно
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # окно без рамки
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)  # прозрачный фон

        # ---------------------------------------------------------- установка позиции окна

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)

        q = QDesktopWidget().availableGeometry()

        self.left = int((q.width() / 3) + 350)
        self.top = q.height()
        self.width = 510
        self.height = 40
        self.initUI()

    def initUI(self):

        # ---------------------------------------------------------- настройка кнопки "Спросить"

        self.button = QPushButton("Спросить", self)
        self.button.setGeometry(330, 5, 100, 30)
        self.button.setStyleSheet("background-color: #32CD32; border-radius : 12; border: 1px solid black")

        # ---------------------------------------------------------- настройка текстового поля

        self.lineedit = QLineEdit(self)
        self.lineedit.setGeometry(10, 8, 300, 25)
        self.lineedit.installEventFilter(self)
        self.lineedit.setStyleSheet("background-color: black; color: yellow; font-family: Lucida Console;"
                                    "border: 2px solid #556B2F; border-radius : 10; padding: 5")

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.connectActions()  # вызов функции обработки действий

        self.show()  # показ окна

    def connectActions(self):
        self.button.clicked.connect(self.ent)  # при нажатии кнопки вызов метода ent()

    def ent(self):
        text = self.sp_to_txt.speech_to_text("USUAL")  # преобразование голоса в текст
        self.exp_sys.work(text)  # обработка текстовой команды

    #  ------ в случае нажатия Enter, строка ввода отчищается, а команда считывается и обрабатывается
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.lineedit:
            if event.key() == QtCore.Qt.Key_Return and self.lineedit.hasFocus():
                text = self.lineedit.text()
                self.lineedit.setText("")  # стереть содержимое текстового поля
                print(text)
                self.exp_sys.work(text)  # отправить команду на обработку
        return super().eventFilter(obj, event)

#  ------------ запуск приложения
print(sys.path)
app = QApplication(sys.argv)
ex = App()

sys.exit(app.exec_())
