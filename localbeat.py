from PySide6.QtWidgets import (QApplication, QMessageBox, QScrollArea, QInputDialog, QMainWindow, QVBoxLayout, QWidget, QToolButton, QHBoxLayout, QStackedWidget, QLabel, QPushButton ,QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path
from datetime import datetime
import sys
from File_json import crea_json


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()

        # HEADER
        icon_online = Path(__file__).parent / "asset" / "icon" / "online.svg"
        icon_offline = Path(__file__).parent / "asset" / "icon" / "offline.svg"
        self.playlists_dir = Path(__file__).parent / "playlists"
        self.playlists_dir.mkdir(exist_ok=True)

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

        # seconda pagina || pagina home-Playlist 
        self.Play_list_pg = QWidget()
        page_layout = QVBoxLayout(self.Play_list_pg)

        
        lista = QWidget()
        self.PlayList_box = QVBoxLayout(lista)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(lista)
        page_layout.addWidget(scroll)

        self.stack.addWidget(self.Play_list_pg)
        

        # questa parte serve ha creare la barra crea-playlist, non sarà facile
        self.bt_add_playlist = QPushButton("+   Crea playlist")
        self.bt_add_playlist.setObjectName("add_playlist")
        self.bt_add_playlist.setFixedHeight(70)
        self.PlayList_box.addWidget(self.bt_add_playlist)
        self.PlayList_box.addStretch()


        # interazione pulsante
        self.bt_offline.clicked.connect(self.local_click)
        self.bt_back.clicked.connect(self.back)
        self.bt_add_playlist.clicked.connect(self.crea_playlist)
        self.stack.currentChanged.connect(self.aggiorna_nav)
        self.aggiorna_nav()


    def local_click(self):
        self.stack.setCurrentWidget(self.Play_list_pg)

    def back(self):
        self.stack.setCurrentWidget(self.central)

    def aggiorna_nav(self):
        home = self.stack.currentWidget() is self.central
        self.bt_back.setEnabled(not home)

    def crea_playlist(self):
        nome, Pass = QInputDialog.getText(self, "Nuova play list", "Inserisci nome: ")
        nome = nome.strip()
        
        if not nome or not Pass:
            return
        elif any(c in nome for c in '\\/:*?"<>|'):
            QMessageBox.warning(self, "Errore", 'Non inserire questi caratteri Pls: \\ / : * ? " < > |')
            return

        cartella = self.playlists_dir / nome
        if cartella.exists():
            QMessageBox.warning(self, "Errore", "Esiste di già una play list con lo stesso nome")
            return

        cartella.mkdir()
        crea_json(nome, cartella)

        self.Crea_riga(nome)

        
    def Crea_riga(self, nome):
        riga = QPushButton(nome)
        riga.setObjectName("playlist_bt")
        riga.setFixedHeight(70)
        self.PlayList_box.insertWidget(0, riga)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainFrame()
    window.showMaximized()

    sys.exit(app.exec())