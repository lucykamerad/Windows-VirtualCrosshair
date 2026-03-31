import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt6.QtCore import Qt

import config_manager
from crosshair_window import CrosshairOverlay
from settings_window import SettingsUI


def create_app_icon():
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("red"))
    painter.setPen(Qt.GlobalColor.transparent)
    painter.drawEllipse(8, 8, 16, 16)
    painter.drawLine(16, 0, 16, 32)
    painter.drawLine(0, 16, 32, 16)
    painter.end()
    return QIcon(pixmap)


def main():
    # Needed to allow tooltips and system tray icons to work properly in some environments
    app = QApplication(sys.argv)

    # Do not quit when the last (settings) window is closed, as the overlay and tray icon remain
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(create_app_icon())

    # Load configuration
    config = config_manager.load_config()

    # Create the overlay (transparent, click-through)
    overlay = CrosshairOverlay(config)

    # Create the settings UI
    settings_ui = SettingsUI(config, overlay, app)

    # Show settings initially so the user knows it's running
    settings_ui.show()

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
