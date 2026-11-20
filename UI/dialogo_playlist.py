from PySide6.QtWidgets import (QDialog, QFileDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)
from PySide6.QtGui import QIcon
from pathlib import Path

class PlaylistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ico_main = Path(__file__).parent / "asset" / "ico" / "offline.ico"
        self.setWindowIcon(QIcon(str(ico_main)))

        self.setObjectName("dialog_playlist")
        self.setWindowTitle("Crea/Personalizza Playlist")
        self.setMinimumSize(600, 340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # Qui sotto trovi il titolo
        spazio_lat = QHBoxLayout()

        spazio_lat.addStretch()
        titolo = QLabel("Crea una nuova playlist")
        spazio_lat.addWidget(titolo)
        spazio_lat.addStretch()   
        titolo.setObjectName("dialog_title")

        # casella inserisci testo e i file
        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome della playlist")

        self.file_scelti = []

        self.bt_file = QPushButton("+")
        self.bt_file.setObjectName("bt_file")
        self.bt_file.setFixedSize(44, 44)
        self.bt_file.setToolTip("Aggiungi file")

        self.info_file = QLabel("Nessun file selezionato")
        self.info_file.setObjectName("dialog_info")

        riga_nome = QHBoxLayout()
        riga_nome.addWidget(self.campo_nome)
        riga_nome.addWidget(self.bt_file)
    
        # tasti crea e annulla
        self.bt_annulla = QPushButton("Annulla")
        self.bt_crea = QPushButton("Crea")
        self.bt_crea.setObjectName("bt_crea")

        # layout
        bottoni = QHBoxLayout()
        bottoni.addStretch()
        bottoni.addWidget(self.bt_annulla)
        bottoni.addWidget(self.bt_crea)

        layout.addWidget(titolo)
        layout.addLayout(riga_nome)
        layout.addStretch()
        layout.addLayout(bottoni)

        self.bt_annulla.clicked.connect(self.reject)
        self.bt_crea.clicked.connect(self.accept)
        self.bt_file.clicked.connect(self.inserisci_file)

        self.bt_crea.setDefault(True)
        self.bt_annulla.setAutoDefault(False)
        self.bt_file.setAutoDefault(False)

    def nome(self):
        return self.campo_nome.text().strip()

    def inserisci_file(self):
        percorsi, _ = QFileDialog.getOpenFileNames(self, "Scegli i file", "", "Audio (*.mp3 *.wav *.flac *.ogg);;Tutti i file (*)")

        for per in percorsi:
            if per not in self.file_scelti:
                self.file_scelti.append(per)
        self.info_file.setText(f"{len(self.file_scelti)} file selezionati")
