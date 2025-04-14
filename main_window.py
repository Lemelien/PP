import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QLabel, QLineEdit, QPushButton, QTabWidget, 
                               QMessageBox, QDialog, QFormLayout, QComboBox, QDateEdit, QHeaderView, 
                               QFrame, QApplication, QScrollArea)
from PySide6.QtCore import Qt, QDate
from user_class import Connect, User, Athlete, Competition, Participation

# Класс для окна входа в систему
class LoginDialog(QDialog):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(600, 400)

        # Стили для окна входа
        self.setStyleSheet("""
            QDialog {
                background: #FFFFFF;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #003087;
                font-family: 'Arial', sans-serif;
            }
            QLabel#fieldLabel {
                font-size: 16px;
                color: #333333;
                font-family: 'Arial', sans-serif;
                margin-right: 10px;
            }
            QLineEdit {
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: #FFFFFF;
                color: #333333;
                min-height: 40px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 1px solid #0066CC;
            }
            QPushButton#loginButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton#loginButton:hover {
                background-color: #0066CC;
            }
            QPushButton#loginButton:pressed {
                background-color: #002060;
            }
            QPushButton#cancelButton {
                background-color: #D3D3D3;
                color: #333333;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton#cancelButton:hover {
                background-color: #C0C0C0;
            }
            QPushButton#cancelButton:pressed {
                background-color: #A9A9A9;
            }
        """)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title_container = QWidget()
        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Вход в систему")
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        title_container.setLayout(title_layout)

        # Поле для логина
        login_container = QWidget()
        login_layout = QHBoxLayout()
        login_layout.setAlignment(Qt.AlignLeft)
        login_layout.setSpacing(10)
        self.login_label = QLabel("Логин:")
        self.login_label.setObjectName("fieldLabel")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        login_layout.addWidget(self.login_label)
        login_layout.addWidget(self.login_input)
        login_container.setLayout(login_layout)

        # Поле для пароля
        password_container = QWidget()
        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignLeft)
        password_layout.setSpacing(10)
        self.password_label = QLabel("Пароль:")
        self.password_label.setObjectName("fieldLabel")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Введите пароль")
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        password_container.setLayout(password_layout)

        # Кнопки
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)

        self.login_button = QPushButton("Войти")
        self.login_button.setObjectName("loginButton")
        self.login_button.clicked.connect(self.check_login)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)
        button_container.setLayout(button_layout)

        # Добавляем элементы в основной layout
        main_layout.addWidget(title_container)
        main_layout.addWidget(login_container)
        main_layout.addWidget(password_container)
        main_layout.addWidget(button_container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def check_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля!")
            return
        user = self.session.query(User).filter_by(логин=login, пароль=password).first()
        if user:
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")

# Класс для окна профиля пользователя
class ProfileDialog(QDialog):
    def __init__(self, session, user, parent=None):
        super().__init__(parent)
        self.session = session
        self.user = user
        self.setWindowTitle("Профиль пользователя")
        self.setFixedSize(600, 700)

        # Стили окна профиля
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                color: #333333;
            }
            QPushButton#editButton, QPushButton#closeButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
                min-height: 40px;
            }
            QPushButton#editButton:hover, QPushButton#closeButton:hover {
                background-color: #0066CC;
            }
            QPushButton#editButton:pressed, QPushButton#closeButton:pressed {
                background-color: #002060;
            }
        """)

        # Основной layout для профиля
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Иконка пользователя
        icon_container = QWidget()
        icon_container.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 75px;
            border: 3px solid #003087;
        """)
        icon_container.setFixedSize(150, 150)
        icon_layout = QHBoxLayout()
        icon_layout.setAlignment(Qt.AlignCenter)
        self.icon_label = QLabel("👤")
        self.icon_label.setStyleSheet("font-size: 50px; color: #003087; background: transparent;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(self.icon_label)
        icon_container.setLayout(icon_layout)

        # Заголовок профиля
        self.title_label = QLabel("Профиль пользователя")
        self.title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #003087;
            padding: 10px;
        """)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Контейнер для информации
        info_container = QWidget()
        info_container.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        """)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)

        # Логин
        login_layout = QHBoxLayout()
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("font-size: 16px; color: #003087; font-weight: bold; min-width: 100px;")
        self.login_value = QLabel(self.user.логин)
        self.login_value.setStyleSheet("font-size: 16px; color: #333333; padding: 5px;")
        login_layout.addWidget(login_label)
        login_layout.addStretch()
        login_layout.addWidget(self.login_value)
        info_layout.addLayout(login_layout)

        # Имя
        name_layout = QHBoxLayout()
        name_label = QLabel("Имя:")
        name_label.setStyleSheet("font-size: 16px; color: #003087; font-weight: bold; min-width: 100px;")
        self.name_value = QLabel(self.user.имя)
        self.name_value.setStyleSheet("font-size: 16px; color: #333333; padding: 5px;")
        name_layout.addWidget(name_label)
        name_layout.addStretch()
        name_layout.addWidget(self.name_value)
        info_layout.addLayout(name_layout)

        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-size: 16px; color: #003087; font-weight: bold; min-width: 100px;")
        self.email_value = QLabel(self.user.email if self.user.email else "Не указан")
        self.email_value.setStyleSheet("font-size: 16px; color: #333333; padding: 5px;")
        email_layout.addWidget(email_label)
        email_layout.addStretch()
        email_layout.addWidget(self.email_value)
        info_layout.addLayout(email_layout)

        # Роль
        role_layout = QHBoxLayout()
        role_label = QLabel("Роль:")
        role_label.setStyleSheet("font-size: 16px; color: #003087; font-weight: bold; min-width: 100px;")
        self.role_value = QLabel(self.user.роль)
        self.role_value.setStyleSheet("font-size: 16px; color: #333333; padding: 5px;")
        role_layout.addWidget(role_label)
        role_layout.addStretch()
        role_layout.addWidget(self.role_value)
        info_layout.addLayout(role_layout)

        info_container.setLayout(info_layout)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        # Кнопка "Редактировать профиль"
        self.edit_button = QPushButton("Редактировать профиль")
        self.edit_button.setObjectName("editButton")
        self.edit_button.clicked.connect(self.edit_profile)

        # Кнопка "Закрыть"
        self.close_button = QPushButton("Закрыть")
        self.close_button.setObjectName("closeButton")
        self.close_button.clicked.connect(self.close)

        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.close_button)
        button_container.setLayout(button_layout)

        # Добавляем все элементы в основной layout
        main_layout.addWidget(icon_container)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(info_container)
        main_layout.addWidget(button_container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def edit_profile(self):
        dialog = EditProfileDialog(self.session, self.user, self)
        if dialog.exec():
            self.refresh_profile()

    def refresh_profile(self):
        self.login_value.setText(self.user.логин)
        self.name_value.setText(self.user.имя)
        self.email_value.setText(self.user.email if self.user.email else "Не указан")
        self.role_value.setText(self.user.роль)

# Класс для окна редактирования профиля
class EditProfileDialog(QDialog):
    def __init__(self, session, user, parent=None):
        super().__init__(parent)
        self.session = session
        self.user = user
        self.setWindowTitle("Редактировать профиль")
        self.setFixedSize(500, 550)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #003087;
                font-family: 'Arial', sans-serif;
                margin-bottom: 10px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
                color: #333333;
                min-height: 40px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0066CC;
            }
            QPushButton#saveButton, QPushButton#cancelButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton#saveButton:hover, QPushButton#cancelButton:hover {
                background-color: #0066CC;
            }
            QPushButton#saveButton:pressed, QPushButton#cancelButton:pressed {
                background-color: #002060;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title_label = QLabel("Редактировать профиль")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #003087; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.login_input = QLineEdit(self.user.логин)
        self.login_input.setPlaceholderText("Введите логин")
        self.name_input = QLineEdit(self.user.имя)
        self.name_input.setPlaceholderText("Введите имя")
        self.email_input = QLineEdit(self.user.email if self.user.email else "")
        self.email_input.setPlaceholderText("Введите email")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["тренер", "администратор"])
        self.role_combo.setCurrentText(self.user.роль)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Оставьте пустым, если не хотите менять")

        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("Имя:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Роль:", self.role_combo)
        form_layout.addRow("Новый пароль:", self.password_input)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self.save_profile)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_container.setLayout(button_layout)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addWidget(button_container)
        layout.addStretch()

        self.setLayout(layout)

    def save_profile(self):
        login = self.login_input.text().strip()
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        password = self.password_input.text().strip()

        if not login or not name or not role:
            QMessageBox.warning(self, "Ошибка", "Логин, имя и роль обязательны!")
            return

        existing_user = self.session.query(User).filter_by(логин=login).first()
        if existing_user and existing_user.id != self.user.id:
            QMessageBox.warning(self, "Ошибка", "Этот логин уже занят!")
            return

        self.user.логин = login
        self.user.имя = name
        self.user.email = email if email else None
        self.user.роль = role
        if password:
            self.user.пароль = password

        self.session.commit()
        QMessageBox.information(self, "Успех", "Профиль обновлён!")
        self.accept()

# Класс для окна добавления спортсмена
class AddAthleteDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавить спортсмена")
        self.setFixedSize(500, 500)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #003087;
                font-family: 'Arial', sans-serif;
                margin-bottom: 10px;
            }
            QLineEdit, QComboBox, QDateEdit {
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
                color: #333333;
                min-height: 40px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #0066CC;
            }
            QPushButton#addButton, QPushButton#cancelButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton#addButton:hover, QPushButton#cancelButton:hover {
                background-color: #0066CC;
            }
            QPushButton#addButton:pressed, QPushButton#cancelButton:pressed {
                background-color: #002060;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title_label = QLabel("Добавить спортсмена")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #003087; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Введите фамилию")
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDate(QDate.currentDate())
        self.sport_input = QLineEdit()
        self.sport_input.setPlaceholderText("Введите вид спорта")
        self.coach_combo = QComboBox()
        coaches = self.session.query(User).filter_by(роль="тренер").all()
        self.coach_combo.addItem("Нет", None)
        for coach in coaches:
            self.coach_combo.addItem(coach.имя, coach.id)

        form_layout.addRow("Имя:", self.name_input)
        form_layout.addRow("Фамилия:", self.surname_input)
        form_layout.addRow("Дата рождения:", self.dob_input)
        form_layout.addRow("Вид спорта:", self.sport_input)
        form_layout.addRow("Тренер:", self.coach_combo)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.add_button = QPushButton("Добавить")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_athlete)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        button_container.setLayout(button_layout)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addWidget(button_container)
        layout.addStretch()

        self.setLayout(layout)

    def add_athlete(self):
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        dob = self.dob_input.date().toPyDate()
        sport = self.sport_input.text().strip()
        coach_id = self.coach_combo.currentData()

        if not name or not surname or not sport:
            QMessageBox.warning(self, "Ошибка", "Имя, фамилия и вид спорта обязательны!")
            return

        new_athlete = Athlete(имя=name, фамилия=surname, дата_рождения=dob, вид_спорта=sport, тренер_id=coach_id)
        self.session.add(new_athlete)
        self.session.commit()
        QMessageBox.information(self, "Успех", "Спортсмен добавлен!")
        self.accept()

# Класс для окна добавления соревнования
class AddCompetitionDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Добавить соревнование")
        self.setFixedSize(500, 450)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #003087;
                font-family: 'Arial', sans-serif;
                margin-bottom: 10px;
            }
            QLineEdit, QDateEdit {
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
                color: #333333;
                min-height: 40px;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #0066CC;
            }
            QPushButton#addButton, QPushButton#cancelButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton#addButton:hover, QPushButton#cancelButton:hover {
                background-color: #0066CC;
            }
            QPushButton#addButton:pressed, QPushButton#cancelButton:pressed {
                background-color: #002060;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title_label = QLabel("Добавить соревнование")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #003087; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Введите место проведения")

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Дата проведения:", self.date_input)
        form_layout.addRow("Место:", self.location_input)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.add_button = QPushButton("Добавить")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.add_competition)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)
        button_container.setLayout(button_layout)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addWidget(button_container)
        layout.addStretch()

        self.setLayout(layout)

    def add_competition(self):
        name = self.name_input.text().strip()
        date = self.date_input.date().toPyDate()
        location = self.location_input.text().strip()

        if not name or not location:
            QMessageBox.warning(self, "Ошибка", "Название и место проведения обязательны!")
            return

        new_competition = Competition(название=name, дата_проведения=date, место=location)
        self.session.add(new_competition)
        self.session.commit()
        QMessageBox.information(self, "Успех", "Соревнование добавлено!")
        self.accept()

# Класс для окна добавления участия
class AddParticipationDialog(QDialog):
    def __init__(self, session, athletes, competitions, parent=None):
        super().__init__(parent)
        self.session = session
        self.athletes = athletes
        self.competitions = competitions
        self.setWindowTitle("Добавить участие")
        self.setFixedSize(500, 400)

        # Стили
        self.setStyleSheet("""
            QDialog {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #003087;
                font-family: 'Arial', sans-serif;
                margin-bottom: 10px;
            }
            QComboBox, QLineEdit {
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: white;
                color: #333333;
                min-height: 40px;
            }
            QComboBox:focus, QLineEdit:focus {
                border: 1px solid #0066CC;
            }
            QPushButton#saveButton, QPushButton#cancelButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
                min-height: 40px;
            }
            QPushButton#saveButton:hover, QPushButton#cancelButton:hover {
                background-color: #0066CC;
            }
            QPushButton#saveButton:pressed, QPushButton#cancelButton:pressed {
                background-color: #002060;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Заголовок
        title_label = QLabel("Добавить участие")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #003087; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.athlete_combo = QComboBox()
        for athlete in self.athletes:
            self.athlete_combo.addItem(f"{athlete.имя} {athlete.фамилия}", athlete.id)

        self.competition_combo = QComboBox()
        for competition in self.competitions:
            self.competition_combo.addItem(competition.название, competition.id)

        self.result_input = QLineEdit()
        self.result_input.setPlaceholderText("Введите результат (опционально)")

        form_layout.addRow("Спортсмен:", self.athlete_combo)
        form_layout.addRow("Соревнование:", self.competition_combo)
        form_layout.addRow("Результат:", self.result_input)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignCenter)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self.save_participation)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        button_container.setLayout(button_layout)

        layout.addWidget(title_label)
        layout.addLayout(form_layout)
        layout.addWidget(button_container)
        layout.addStretch()

        self.setLayout(layout)

    def save_participation(self):
        athlete_id = self.athlete_combo.currentData()
        competition_id = self.competition_combo.currentData()
        result = self.result_input.text().strip()

        new_participation = Participation(спортсмен_id=athlete_id, соревнование_id=competition_id, результат=result if result else None)
        self.session.add(new_participation)
        self.session.commit()
        QMessageBox.information(self, "Успех", "Участие добавлено!")
        self.accept()

# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self, current_user, session):
        super().__init__()
        self.session = session
        self.current_user = current_user
        self.setWindowTitle("Паралимпийский резерв")
        self.setFixedSize(1200, 800)

        # Стили главного окна
        self.setStyleSheet("""
            QMainWindow {
                background: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                color: #003087;
                font-family: 'Arial', sans-serif;
            }
            QPushButton#logoutButton, QPushButton#profileButton, QPushButton#refreshButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 100px;
                min-height: 40px;
            }
            QPushButton#logoutButton:hover, QPushButton#profileButton:hover, QPushButton#refreshButton:hover {
                background-color: #0066CC;
            }
            QPushButton#logoutButton:pressed, QPushButton#profileButton:pressed, QPushButton#refreshButton:pressed {
                background-color: #002060;
            }
            QPushButton {
                background-color: #003087;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #0066CC;
            }
            QPushButton:pressed {
                background-color: #002060;
            }
            QTableWidget {
                border: 1px solid #D3D3D3;
                background-color: white;
                font-size: 16px;
                color: #333333;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget::item {
                color: #333333;
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #003087;
                color: white;
                padding: 10px;
                border: 1px solid #002060;
                font-weight: bold;
                font-size: 16px;
            }
            QTabWidget::pane {
                border: 1px solid #D3D3D3;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #E6E7E8;
                color: #003087;
                padding: 10px;
                font-size: 14px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: #003087;
                color: white;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Основной layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Верхняя панель
        top_bar = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignRight)

        self.profile_button = QPushButton("Профиль")
        self.profile_button.setObjectName("profileButton")
        self.profile_button.clicked.connect(self.show_profile)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setObjectName("refreshButton")
        self.refresh_button.clicked.connect(self.refresh_all_tables)

        self.logout_button = QPushButton("Выйти")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout)

        top_layout.addWidget(self.profile_button)
        top_layout.addWidget(self.refresh_button)
        top_layout.addWidget(self.logout_button)
        top_bar.setLayout(top_layout)

        # Приветственное сообщение
        welcome_container = QWidget()
        welcome_layout = QHBoxLayout()
        welcome_layout.setAlignment(Qt.AlignCenter)
        welcome_label = QLabel(f"Добро пожаловать, {self.current_user.имя}!")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #003087;")
        welcome_layout.addWidget(welcome_label)
        welcome_container.setLayout(welcome_layout)

        # Статистика
        stats_container = QWidget()
        stats_container.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 5px;
            padding: 10px;
            border: 1px solid #D3D3D3;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        """)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        stats_layout.setAlignment(Qt.AlignCenter)

        athletes_count = self.session.query(Athlete).count()
        competitions_count = self.session.query(Competition).count()
        participations_count = self.session.query(Participation).count()

        athletes_label = QLabel(f"Спортсменов: {athletes_count}")
        athletes_label.setStyleSheet("font-size: 16px; color: #003087;")
        competitions_label = QLabel(f"Соревнований: {competitions_count}")
        competitions_label.setStyleSheet("font-size: 16px; color: #003087;")
        participations_label = QLabel(f"Участий: {participations_count}")
        participations_label.setStyleSheet("font-size: 16px; color: #003087;")

        stats_layout.addWidget(athletes_label)
        stats_layout.addWidget(competitions_label)
        stats_layout.addWidget(participations_label)
        stats_container.setLayout(stats_layout)

        # Вкладки
        self.tabs = QTabWidget()

        # Вкладка "Спортсмены"
        self.athletes_tab = QWidget()
        athletes_layout = QVBoxLayout()
        athletes_layout.setSpacing(15)

        self.athlete_table = QTableWidget()
        self.athlete_table.setColumnCount(6)
        self.athlete_table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Дата рождения", "Вид спорта", "Тренер"])
        self.athlete_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.athlete_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.athlete_table.setEditTriggers(QTableWidget.NoEditTriggers)

        athlete_buttons = QWidget()
        athlete_button_layout = QHBoxLayout()
        athlete_button_layout.setAlignment(Qt.AlignCenter)
        athlete_button_layout.setSpacing(15)

        self.add_athlete_button = QPushButton("Добавить спортсмена")
        self.add_athlete_button.clicked.connect(self.add_athlete)
        self.delete_athlete_button = QPushButton("Удалить спортсмена")
        self.delete_athlete_button.clicked.connect(self.delete_athlete)

        athlete_button_layout.addWidget(self.add_athlete_button)
        athlete_button_layout.addWidget(self.delete_athlete_button)
        athlete_buttons.setLayout(athlete_button_layout)

        athletes_layout.addWidget(self.athlete_table)
        athletes_layout.addWidget(athlete_buttons)
        self.athletes_tab.setLayout(athletes_layout)

        # Вкладка "Соревнования"
        self.competitions_tab = QWidget()
        competitions_layout = QVBoxLayout()
        competitions_layout.setSpacing(15)

        self.competition_table = QTableWidget()
        self.competition_table.setColumnCount(4)
        self.competition_table.setHorizontalHeaderLabels(["ID", "Название", "Дата проведения", "Место"])
        self.competition_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.competition_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.competition_table.setEditTriggers(QTableWidget.NoEditTriggers)

        competition_buttons = QWidget()
        competition_button_layout = QHBoxLayout()
        competition_button_layout.setAlignment(Qt.AlignCenter)
        competition_button_layout.setSpacing(15)

        self.add_competition_button = QPushButton("Добавить соревнование")
        self.add_competition_button.clicked.connect(self.add_competition)
        self.delete_competition_button = QPushButton("Удалить соревнование")
        self.delete_competition_button.clicked.connect(self.delete_competition)

        competition_button_layout.addWidget(self.add_competition_button)
        competition_button_layout.addWidget(self.delete_competition_button)
        competition_buttons.setLayout(competition_button_layout)

        competitions_layout.addWidget(self.competition_table)
        competitions_layout.addWidget(competition_buttons)
        self.competitions_tab.setLayout(competitions_layout)

        # Вкладка "Участие"
        self.participation_tab = QWidget()
        participation_layout = QVBoxLayout()
        participation_layout.setSpacing(15)

        self.participation_table = QTableWidget()
        self.participation_table.setColumnCount(4)
        self.participation_table.setHorizontalHeaderLabels(["ID", "Спортсмен", "Соревнование", "Результат"])
        self.participation_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.participation_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.participation_table.setEditTriggers(QTableWidget.NoEditTriggers)

        participation_buttons = QWidget()
        participation_button_layout = QHBoxLayout()
        participation_button_layout.setAlignment(Qt.AlignCenter)
        participation_button_layout.setSpacing(15)

        self.add_participation_button = QPushButton("Добавить участие")
        self.add_participation_button.clicked.connect(self.add_participation)
        self.delete_participation_button = QPushButton("Удалить участие")
        self.delete_participation_button.clicked.connect(self.delete_participation)

        participation_button_layout.addWidget(self.add_participation_button)
        participation_button_layout.addWidget(self.delete_participation_button)
        participation_buttons.setLayout(participation_button_layout)

        participation_layout.addWidget(self.participation_table)
        participation_layout.addWidget(participation_buttons)
        self.participation_tab.setLayout(participation_layout)

        # Добавляем вкладки
        self.tabs.addTab(self.athletes_tab, "Спортсмены")
        self.tabs.addTab(self.competitions_tab, "Соревнования")
        self.tabs.addTab(self.participation_tab, "Участие")

        # Добавляем элементы в основной layout
        main_layout.addWidget(top_bar)
        main_layout.addWidget(welcome_container)
        main_layout.addWidget(stats_container)
        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Обновляем таблицы
        self.update_athlete_table()
        self.update_competition_table()
        self.update_participation_table()

    def update_athlete_table(self):
        try:
            athletes = self.session.query(Athlete).all()
            self.athlete_table.setRowCount(len(athletes))
            for row, athlete in enumerate(athletes):
                self.athlete_table.setItem(row, 0, QTableWidgetItem(str(athlete.id)))
                self.athlete_table.setItem(row, 1, QTableWidgetItem(athlete.имя))
                self.athlete_table.setItem(row, 2, QTableWidgetItem(athlete.фамилия))
                self.athlete_table.setItem(row, 3, QTableWidgetItem(str(athlete.дата_рождения)))
                self.athlete_table.setItem(row, 4, QTableWidgetItem(athlete.вид_спорта))
                self.athlete_table.setItem(row, 5, QTableWidgetItem(athlete.тренер.имя if athlete.тренер else "Нет"))
            self.athlete_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные спортсменов: {str(e)}")

    def update_competition_table(self):
        try:
            competitions = self.session.query(Competition).all()
            self.competition_table.setRowCount(len(competitions))
            for row, competition in enumerate(competitions):
                self.competition_table.setItem(row, 0, QTableWidgetItem(str(competition.id)))
                self.competition_table.setItem(row, 1, QTableWidgetItem(competition.название))
                self.competition_table.setItem(row, 2, QTableWidgetItem(str(competition.дата_проведения)))
                self.competition_table.setItem(row, 3, QTableWidgetItem(competition.место))
            self.competition_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные соревнований: {str(e)}")

    def update_participation_table(self):
        try:
            participations = self.session.query(Participation).all()
            self.participation_table.setRowCount(len(participations))
            for row, participation in enumerate(participations):
                self.participation_table.setItem(row, 0, QTableWidgetItem(str(participation.id)))
                athlete = self.session.query(Athlete).filter_by(id=participation.спортсмен_id).first()
                competition = self.session.query(Competition).filter_by(id=participation.соревнование_id).first()
                self.participation_table.setItem(row, 1, QTableWidgetItem(f"{athlete.имя} {athlete.фамилия}" if athlete else "Неизвестно"))
                self.participation_table.setItem(row, 2, QTableWidgetItem(competition.название if competition else "Неизвестно"))
                self.participation_table.setItem(row, 3, QTableWidgetItem(participation.результат if participation.результат else "Не указан"))
            self.participation_table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные участий: {str(e)}")

    def refresh_all_tables(self):
        self.update_athlete_table()
        self.update_competition_table()
        self.update_participation_table()
        QMessageBox.information(self, "Успех", "Все таблицы обновлены!")

    def add_athlete(self):
        dialog = AddAthleteDialog(self.session, self)
        if dialog.exec():
            self.update_athlete_table()

    def delete_athlete(self):
        selected_rows = self.athlete_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите спортсмена для удаления!")
            return

        for row in selected_rows:
            athlete_id = int(self.athlete_table.item(row.row(), 0).text())
            athlete = self.session.query(Athlete).filter_by(id=athlete_id).first()
            if athlete:
                self.session.delete(athlete)
        self.session.commit()
        self.update_athlete_table()
        QMessageBox.information(self, "Успех", "Спортсмен удалён!")

    def add_competition(self):
        dialog = AddCompetitionDialog(self.session, self)
        if dialog.exec():
            self.update_competition_table()

    def delete_competition(self):
        selected_rows = self.competition_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите соревнование для удаления!")
            return

        for row in selected_rows:
            competition_id = int(self.competition_table.item(row.row(), 0).text())
            competition = self.session.query(Competition).filter_by(id=competition_id).first()
            if competition:
                self.session.delete(competition)
        self.session.commit()
        self.update_competition_table()
        QMessageBox.information(self, "Успех", "Соревнование удалено!")

    def add_participation(self):
        athletes = self.session.query(Athlete).all()
        competitions = self.session.query(Competition).all()

        if not athletes or not competitions:
            QMessageBox.warning(self, "Ошибка", "Нет спортсменов или соревнований для добавления участия!")
            return

        dialog = AddParticipationDialog(self.session, athletes, competitions, self)
        if dialog.exec():
            self.update_participation_table()

    def delete_participation(self):
        selected_rows = self.participation_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите участие для удаления!")
            return

        for row in selected_rows:
            participation_id = int(self.participation_table.item(row.row(), 0).text())
            participation = self.session.query(Participation).filter_by(id=participation_id).first()
            if participation:
                self.session.delete(participation)
        self.session.commit()
        self.update_participation_table()
        QMessageBox.information(self, "Успех", "Участие удалено!")

    def show_profile(self):
        dialog = ProfileDialog(self.session, self.current_user, self)
        dialog.exec()

    def logout(self):
        self.close()

    def closeEvent(self, event):
        self.session.close()
        event.accept()
