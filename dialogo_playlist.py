from PySide6.QtWidgets import (QDialog,QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)
from pathlib import Path

class PlaylistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("dialog_playlist")
        self.setWindowTitle("Crea/Personalizza Playlist")
        self.setMinimumWidth(100)

        layout = QVBoxLayout(self)

        titolo = QLabel("Crea una nuova playlist")
        titolo.setObjectName("dialog_title")

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome della playlist")

        self.bt_annulla = QPushButton("Annulla")
        self.bt_crea = QPushButton("Crea")
        self.bt_crea.setObjectName("bt_crea")

        bottoni = QHBoxLayout()
        bottoni.addStretch()
        bottoni.addWidget(self.bt_annulla)
        bottoni.addWidget(self.bt_crea)

        layout.addWidget(titolo)
        layout.addWidget(self.campo_nome)
        layout.addStretch()
        layout.addLayout(bottoni)

        self.bt_annulla.clicked.connect(self.reject)
        self.bt_crea.clicked.connect(self.accept)

    def nome(self):
        return self.campo_nome.text().strip()

