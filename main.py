from PySide6.QtWidgets import QApplication
from main_window import MainWindow, LoginDialog
from user_class import Connect

if __name__ == "__main__":
    app = QApplication([])
    session = Connect.create_connection()

    while True:
        # Открываем окно авторизации
        login_dialog = LoginDialog(session)
        if login_dialog.exec() != LoginDialog.Accepted:
            break  # Если пользователь закрыл окно авторизации, выходим из цикла

        # Если авторизация успешна, открываем главное окно
        window = MainWindow(login_dialog.current_user, session)
        window.show()
        # Запускаем цикл обработки событий для текущего окна
        app.exec()