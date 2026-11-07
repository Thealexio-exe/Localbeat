import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolButton, QHBoxLayout
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
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        top_bar = QHBoxLayout()

        # layout e bottoni inizializati
        self.bt_online = QToolButton()
        self.bt_online.setText("Online list")
        self.bt_offline = QToolButton()
        self.bt_offline.setText("Offline list")

        # per i file .qss
        self.bt_offline.setObjectName("bt_offl")
        self.bt_online.setObjectName("bt_onl")

        for btn in (self.bt_online, self.bt_offline):
            btn.setFixedSize(lato, lato)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)


            if btn is self.bt_online:
                btn.setIcon(QIcon(str(icon_online)))
            else:
                btn.setIcon(QIcon(str(icon_offline)))

            btn.setIconSize(QSize(lato // 2, lato // 2))


        # visualiza a scermo i pulsanti e il layout
        layout.addStretch()
        top_bar.addStretch()
        top_bar.addWidget(self.bt_online)
        top_bar.addWidget(self.bt_offline)
        top_bar.addStretch()
        top_bar.setSpacing(50)

        layout.addLayout(top_bar)
        layout.addStretch()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainFrame()
    window.showMaximized()

    sys.exit(app.exec())