import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QToolButton, QHBoxLayout, QStackedWidget, QLabel, QPushButton ,QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()

        # HEADER
        icon_online = Path(__file__).parent / "asset" / "icon" / "online.svg"
        icon_offline = Path(__file__).parent / "asset" / "icon" / "offline.svg"

        style_path = Path(__file__).parent / "style" / "style.qss"
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

        # nome app 
        self.setWindowTitle("LocalBeat")

        # auto regolamento tasti
        screen = self.screen().availableGeometry()
        lato_corto = min(screen.width(), screen.height())
        lato = max(150, int(lato_corto * 0.25))
        
        # box per i bottoni
        self.central = QWidget()
        self.stack = QStackedWidget()
        
        # box barra
        self.nav_bar = QFrame()
        self.nav_bar.setObjectName("nav_bar")
        nav_layout = QHBoxLayout(self.nav_bar)

        # pulsate back
        
        self.bt_back = QPushButton("<")
        self.bt_back.setFixedSize(30, 30)
        nav_layout.addWidget(self.bt_back)

        nav_layout.addStretch()

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.nav_bar)
        main_layout.addWidget(self.stack, 1)
        self.setCentralWidget(container)

        self.stack.addWidget(self.central)
        layout = QVBoxLayout(self.central)
        top_bar = QHBoxLayout()

        # layout e bottoni inizializati
        self.bt_online = QToolButton()
        self.bt_online.setText("Online list")
        self.bt_offline = QToolButton()
        self.bt_offline.setText("Offline list")

        # per i file .qss
        self.bt_offline.setObjectName("bt_offl")
        self.bt_online.setObjectName("bt_onl")

        for bt in (self.bt_online, self.bt_offline):
            bt.setFixedSize(lato, lato)
            bt.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)


            if bt is self.bt_online:
                bt.setIcon(QIcon(str(icon_online)))
            else:
                bt.setIcon(QIcon(str(icon_offline)))

            bt.setIconSize(QSize(lato // 2, lato // 2))

        # visualiza a scermo i pulsanti e il layout
        layout.addStretch()
        top_bar.addStretch()

        top_bar.addWidget(self.bt_online)
        top_bar.addWidget(self.bt_offline)
        top_bar.addStretch()
        top_bar.setSpacing(50)

        layout.addLayout(top_bar)
        layout.addStretch()

        # creo la seconda pagina
        self.local_page = QWidget()
        local_layout = QVBoxLayout(self.local_page)
        local_layout.addWidget(QLabel("Schermata Local"))
        self.stack.addWidget(self.local_page)

        # interazione pulsante
        self.bt_offline.clicked.connect(self.local_click)


    def local_click(self):
        self.bt_back.clicked.connect(self.back)
        self.stack.setCurrentWidget(self.local_page)

    def back(self):
        self.stack.setCurrentWidget(self.central)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainFrame()
    window.showMaximized()

    sys.exit(app.exec())