import sys
import signal
import os
import winreg

from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QTimer,
    QSharedMemory,
)

from PySide6.QtGui import (
    QPixmap,
    QGuiApplication,
    QIcon,
    QPainter,
    QPainterPath,
    QColor,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QSystemTrayIcon,
    QMenu,
)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)


# -------------------------
# TIMER SETTINGS
# -------------------------

TEST_MODE = False

if TEST_MODE:
    REMINDER_INTERVAL = 10 * 1000
    VISIBLE_TIME = 5 * 1000
else:
    REMINDER_INTERVAL = 30 * 60 * 1000
    VISIBLE_TIME = 60 * 1000


APP_NAME = "DesktopVirtualPet"


# -------------------------
# SPEECH BUBBLE
# -------------------------

class SpeechBubble(QWidget):
    def __init__(self, text):
        super().__init__()

        self.setFixedSize(210, 78)

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.label.setStyleSheet("""
            QLabel {
                background: transparent;
                color: black;
                font-size: 12px;
            }
        """)

        bubble_layout = QHBoxLayout(self)
        bubble_layout.setContentsMargins(18, 10, 12, 14)
        bubble_layout.addWidget(self.label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("white"))

        path = QPainterPath()

        # Main rounded speech bubble
        path.addRoundedRect(
            12,
            4,
            self.width() - 20,
            self.height() - 18,
            26,
            26
        )

        # Tail on LEFT side, pointing toward the pet
        # Tail on RIGHT side, pointing toward the pet
        tail = QPainterPath()

        tail.moveTo(
            self.width() - 45,
            self.height() - 22
        )

        tail.lineTo(
            self.width() - 5,
            self.height() - 5
        )

        tail.lineTo(
            self.width() - 55,
            self.height() - 13
        )

        tail.closeSubpath()

        path = path.united(tail)
        painter.drawPath(path)


app = QApplication(sys.argv)

shared_memory = QSharedMemory("DesktopVirtualPetSingleInstance")

if not shared_memory.create(1):
    sys.exit(0)


signal.signal(signal.SIGINT, lambda sig, frame: app.quit())

ctrl_c_timer = QTimer()
ctrl_c_timer.timeout.connect(lambda: None)
ctrl_c_timer.start(100)


window = QWidget()

window.setWindowFlags(
    Qt.FramelessWindowHint
    | Qt.WindowStaysOnTopHint
    | Qt.Tool
)

window.setAttribute(Qt.WA_TranslucentBackground)


# CHANGED:
# Horizontal layout so pet and message sit side-by-side
layout = QHBoxLayout()
layout.setSpacing(4)
layout.setContentsMargins(0, 0, 0, 0)


# Reminder message
message = SpeechBubble(
    "💧 Drink some water!\n"
    "Despite it all, she still blooms. 🌸"
)


# Pet image
pet_label = QLabel()


def close_app(event):
    if event.button() == Qt.RightButton:
        app.quit()


pet_label.mousePressEvent = close_app

pet_path = resource_path("assets/pet.png")

pet_image = QPixmap(pet_path)

PET_WIDTH = 160
PET_HEIGHT = 200

pet_image = pet_image.scaled(
    PET_WIDTH,
    PET_HEIGHT,
    Qt.KeepAspectRatio,
    Qt.SmoothTransformation
)

pet_label.setPixmap(pet_image)
pet_label.setAlignment(Qt.AlignCenter)


# CHANGED:
# Pet first, message second = message appears on RIGHT side
layout.addWidget(
    message,
    alignment=Qt.AlignVCenter
)

layout.addWidget(
    pet_label,
    alignment=Qt.AlignBottom
)


window.setLayout(layout)


screen = QGuiApplication.primaryScreen().availableGeometry()

window.adjustSize()

x = screen.right() - window.width() - 20
y = screen.bottom() - window.height() - 20

window.move(x, y)

window.show()


animation = QPropertyAnimation(window, b"pos")

start_position = window.pos()

end_position = QPoint(
    start_position.x(),
    start_position.y() - 15
)

animation.setStartValue(start_position)
animation.setEndValue(end_position)

animation.setDuration(1200)
animation.setEasingCurve(QEasingCurve.InOutSine)

animation.setLoopCount(-1)

animation.start()


def show_pet():
    window.show()

    # Hide after 60 seconds
    QTimer.singleShot(
        VISIBLE_TIME,
        window.hide
    )


reminder_timer = QTimer()
reminder_timer.timeout.connect(show_pet)

reminder_timer.start(REMINDER_INTERVAL)


def is_startup_enabled():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )

        winreg.QueryValueEx(
            key,
            APP_NAME
        )

        winreg.CloseKey(key)

        return True

    except FileNotFoundError:
        return False


def toggle_startup(checked):

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )

    if checked:

        if getattr(sys, "frozen", False):

            command = f'"{sys.executable}"'

        else:

            python_path = sys.executable

            pythonw_path = python_path.replace(
                "python.exe",
                "pythonw.exe"
            )

            script_path = os.path.abspath(__file__)

            command = (
                f'"{pythonw_path}" '
                f'"{script_path}"'
            )

        winreg.SetValueEx(
            key,
            APP_NAME,
            0,
            winreg.REG_SZ,
            command
        )

    else:

        try:
            winreg.DeleteValue(
                key,
                APP_NAME
            )

        except FileNotFoundError:
            pass

    winreg.CloseKey(key)


def pause_reminders():

    reminder_timer.stop()

    pause_action.setEnabled(False)
    resume_action.setEnabled(True)


def resume_reminders():

    reminder_timer.start(
        REMINDER_INTERVAL
    )

    pause_action.setEnabled(True)
    resume_action.setEnabled(False)


def restart_timer():

    reminder_timer.stop()

    reminder_timer.start(
        REMINDER_INTERVAL
    )


# -------------------------
# SYSTEM TRAY
# -------------------------

tray_icon = QSystemTrayIcon()

tray_icon.setIcon(
    QIcon(
        resource_path(
            "assets/pet.png"
        )
    )
)

tray_menu = QMenu()

show_action = tray_menu.addAction("Show Pet")

pause_action = tray_menu.addAction("Pause Reminders")

resume_action = tray_menu.addAction("Resume Reminders")

restart_action = tray_menu.addAction("Restart Timer")

startup_action = tray_menu.addAction("Start with Windows")

startup_action.setCheckable(True)

startup_action.setChecked(
    is_startup_enabled()
)

exit_action = tray_menu.addAction("Exit")


# Initial button states

pause_action.setEnabled(True)

resume_action.setEnabled(False)


# Connect menu buttons

show_action.triggered.connect(
    show_pet
)

pause_action.triggered.connect(
    pause_reminders
)

resume_action.triggered.connect(
    resume_reminders
)

restart_action.triggered.connect(
    restart_timer
)

startup_action.triggered.connect(
    toggle_startup
)

exit_action.triggered.connect(
    app.quit
)


tray_icon.setContextMenu(
    tray_menu
)

tray_icon.show()


# Show pet immediately when program starts

if TEST_MODE:

    show_pet()

else:

    window.hide()


sys.exit(
    app.exec()
)