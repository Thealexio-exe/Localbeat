from PySide6.QtWidgets import (QApplication, QButtonGroup, QMessageBox, QScrollArea, QMainWindow, QVBoxLayout, QWidget, QToolButton, QHBoxLayout, QStackedWidget, QLabel, QPushButton ,QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path
from logic.File_json import crea_json, leggi_json, carica_impostazioni, salva_impostazioni
from UI.dialogo_playlist import PlaylistDialog
import sys

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()

        # HEADER e file caricati
        icon_online = Path(__file__).parent / "asset" / "icon" / "online.svg"
        icon_offline = Path(__file__).parent / "asset" / "icon" / "offline.svg"
        ico_main = Path(__file__).parent / "asset" / "ico" / "offline.ico"
        self.json_main = Path(__file__).parent / "data" / "main_json.json"
        self.playlists_dir = Path(__file__).parent / "data" / "playlist"
        self.playlists_dir.mkdir(parents=True, exist_ok=True)

        style_path = Path(__file__).parent / "style"

        trovati = ""
        for f in sorted(style_path.glob("*.qss")):
            trovati += f.read_text(encoding="utf-8") + "\n"

        app.setStyleSheet(trovati)

        # App
        self.setWindowTitle("LocalBeat")
        self.setWindowIcon(QIcon(str(ico_main)))

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
        page_layout = QHBoxLayout(self.Play_list_pg)

        # scroll area
        lista = QWidget()
        self.PlayList_box = QVBoxLayout(lista)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(lista)

        self.ordine = carica_impostazioni(self.json_main)
        self.righe = []

        # menu a sinistra, rimove la scroll area
        self.side_menu = QFrame()
        self.side_menu.setObjectName("side_menu")
        self.side_menu.setFixedWidth(300)
        side_layout = QVBoxLayout(self.side_menu)

        box_ordine_bt = QFrame()
        box_ordine_bt.setObjectName("menu_box_bt")
        box_ord_layout = QVBoxLayout(box_ordine_bt)

        titolo_Mn_ordine = QLabel("Ordina PlayList per:")
        titolo_Mn_ordine.setObjectName("side_title_bt")
        box_ord_layout.addWidget(titolo_Mn_ordine)

        self.gruppo_ordine = QButtonGroup(self)
        self.bt_ordine = {}
        for testo, chiave in (("Data di creazione (crescente)", "creazione_asc"),
                      ("Data di creazione (decrescente)", "creazione_desc"),
                      ("Ordine alfabetico", "alfabetico"),
                      ("Ultimo ascolto", "ultimo_ascolto")):
            bt = QPushButton(testo)
            bt.setObjectName("bt_ordine")
            bt.setCheckable(True)
            bt.setProperty("chiave", chiave)
            box_ord_layout.addWidget(bt)
            self.gruppo_ordine.addButton(bt)
            self.bt_ordine[chiave] = bt

        self.bt_ordine[self.ordine].setChecked(True)
        self.bt_ordine["ultimo_ascolto"].setEnabled(False)

        side_layout.addWidget(box_ordine_bt)
        side_layout.addStretch()

        # qui divido lo scroll con la pagina accanto
        page_layout.addWidget(self.side_menu)
        page_layout.addWidget(scroll, 1)

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
        self.gruppo_ordine.buttonClicked.connect(self.ordine_cliccato)
        self.aggiorna_nav()
        self.carica_playlist()

    # semplici funzioni per far funzionare i tasti e cambiare pagina
    def local_click(self):
        self.stack.setCurrentWidget(self.Play_list_pg)

    def back(self):
        self.stack.setCurrentWidget(self.central)

    def aggiorna_nav(self):
        home = self.stack.currentWidget() is self.central
        self.bt_back.setEnabled(not home)

    def ordine_cliccato(self, bt):
        self.ordine = bt.property("chiave")
        self.carica_playlist()

    # funzioni più lunghe, qesta crea l'intera playlist
    def crea_playlist(self):
        dialog = PlaylistDialog(self)
        if not dialog.exec():
            return

        nome = dialog.nome()
        if not nome:
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

        self.carica_playlist()

    def carica_playlist(self):

        for r in self.righe:
            self.PlayList_box.removeWidget(r)
            r.deleteLater()
        self.righe.clear()

        pl_trovate = []

        for cartelle_pl in self.playlists_dir.iterdir():
            if not cartelle_pl.is_dir():
                continue
            dati = leggi_json(cartelle_pl)
            if dati is None:
                continue
            pl_trovate.append((dati.get("creata", ""), dati.get("nome", cartelle_pl.name)))

        for _, nome in self.ordina(pl_trovate):
            self.Crea_riga(nome)

    def ordina(self, playlist):
        salva_impostazioni(self.json_main, self.ordine)

        if self.ordine == "creazione_asc":
            return sorted(playlist)
        elif self.ordine == "creazione_desc":
            return sorted(playlist, reverse=True)
        elif self.ordine == "alfabetico":
            return sorted(playlist, key=lambda p: p[1].lower())
        return playlist

        
    def Crea_riga(self, nome):
        riga = QPushButton(nome)
        riga.setObjectName("playlist_bt")
        riga.setFixedHeight(70)
        self.PlayList_box.insertWidget(len(self.righe), riga)
        self.righe.append(riga)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainFrame()
    window.showMaximized()

    sys.exit(app.exec())