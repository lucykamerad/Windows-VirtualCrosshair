import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QComboBox, QPushButton, QColorDialog,
                             QApplication, QSystemTrayIcon, QMenu, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QPixmap, QPainter, QFont
import config_manager


class SettingsUI(QWidget):
    def __init__(self, config, overlay, app):
        super().__init__()
        self.config = config
        self.overlay = overlay
        self.app = app
        self.initUI()
        self.setup_tray_icon()

    def initUI(self):
        self.setWindowTitle("Virtual Crosshair Settings")
        self.setFixedSize(340, 480)

        # Apply premium dark theme via Qt Style Sheets
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }
            QFrame {
                background-color: #313244;
                border-radius: 10px;
            }
            QLabel {
                background-color: transparent;
                font-weight: 500;
            }
            QLabel#header {
                font-size: 18px;
                font-weight: bold;
                color: #89b4fa;
                margin-bottom: 5px;
            }
            QComboBox {
                background-color: #45475a;
                border: 1px solid #585b70;
                border-radius: 6px;
                padding: 6px 10px;
                color: #cdd6f4;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton#colorButton {
                background-color: transparent;
                border: 2px solid #585b70;
                color: #cdd6f4;
            }
            QPushButton#colorButton:hover {
                border: 2px solid #89b4fa;
                background-color: #45475a;
            }
            QPushButton#exitButton {
                background-color: #f38ba8;
                color: #11111b;
            }
            QPushButton#exitButton:hover {
                background-color: #eba0ac;
            }
            QSlider::groove:horizontal {
                border-radius: 4px;
                height: 6px;
                background: #45475a;
            }
            QSlider::handle:horizontal {
                background: #89b4fa;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #b4befe;
            }
            QSlider::sub-page:horizontal {
                background: #89b4fa;
                border-radius: 4px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title_label = QLabel("Crosshair Settings")
        title_label.setObjectName("header")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # ------------------- appearance group -------------------
        appearance_frame = QFrame()
        appearance_layout = QVBoxLayout(appearance_frame)
        appearance_layout.setContentsMargins(15, 15, 15, 15)
        appearance_layout.setSpacing(12)

        # Shape Selection
        shape_layout = QHBoxLayout()
        shape_label = QLabel("Shape:")
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Cross", "Dot", "Cross + Dot", "Circle"])
        self.shape_combo.setCurrentText(self.config["shape"])
        self.shape_combo.currentTextChanged.connect(self.update_shape)
        shape_layout.addWidget(shape_label)
        shape_layout.addWidget(self.shape_combo, 1)
        appearance_layout.addLayout(shape_layout)

        # Color Selection
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        self.color_button = QPushButton()
        self.color_button.setObjectName("colorButton")
        self.color_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_color_button_style(self.config["color"])
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button, 1)
        appearance_layout.addLayout(color_layout)

        main_layout.addWidget(appearance_frame)

        # ------------------- size & geometry group -------------------
        geometry_frame = QFrame()
        geometry_layout = QVBoxLayout(geometry_frame)
        geometry_layout.setContentsMargins(15, 15, 15, 15)
        geometry_layout.setSpacing(10)

        # Size Slider
        geometry_layout.addWidget(QLabel("Size:"))
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.size_slider.setRange(1, 100)
        self.size_slider.setValue(self.config["size"])
        self.size_slider.valueChanged.connect(self.update_size)
        geometry_layout.addWidget(self.size_slider)

        # Thickness Slider
        geometry_layout.addWidget(QLabel("Thickness:"))
        self.thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.thickness_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.thickness_slider.setRange(1, 20)
        self.thickness_slider.setValue(self.config["thickness"])
        self.thickness_slider.valueChanged.connect(self.update_thickness)
        geometry_layout.addWidget(self.thickness_slider)

        # Opacity Slider
        geometry_layout.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self.opacity_slider.setRange(10, 255)
        self.opacity_slider.setValue(self.config["opacity"])
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        geometry_layout.addWidget(self.opacity_slider)

        main_layout.addWidget(geometry_frame)

        # spacer
        main_layout.addStretch()

        # ------------------- buttons group -------------------
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        self.exit_button = QPushButton("Exit App")
        self.exit_button.setObjectName("exitButton")
        self.exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit_button.clicked.connect(self.quit_app)

        self.save_button = QPushButton("Hide Settings")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.clicked.connect(self.hide)

        buttons_layout.addWidget(self.exit_button)
        buttons_layout.addWidget(self.save_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def create_color_icon(self, hex_color):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor(hex_color))
        painter.setPen(Qt.GlobalColor.transparent)
        # Draw rounded rect or circle to represent color
        painter.drawEllipse(1, 1, 18, 18)
        painter.end()
        return QIcon(pixmap)

    def update_color_button_style(self, hex_color):
        self.color_button.setIcon(self.create_color_icon(hex_color))
        self.color_button.setIconSize(QSize(20, 20))
        self.color_button.setText(f"  {hex_color.upper()}")

    def choose_color(self):
        color = QColorDialog.getColor(
            QColor(self.config["color"]), self, "Select Crosshair Color")
        if color.isValid():
            hex_color = color.name()
            self.config["color"] = hex_color
            self.update_color_button_style(hex_color)
            self.apply_settings()

    def update_shape(self, text):
        self.config["shape"] = text
        self.apply_settings()

    def update_size(self, value):
        self.config["size"] = value
        self.apply_settings()

    def update_thickness(self, value):
        self.config["thickness"] = value
        self.apply_settings()

    def update_opacity(self, value):
        self.config["opacity"] = value
        self.apply_settings()

    def apply_settings(self):
        config_manager.save_config(self.config)
        self.overlay.update_settings(self.config)

    def setup_tray_icon(self):
        # Create a simple icon for the tray
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QColor("red"))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawEllipse(16, 16, 32, 32)
        painter.drawLine(32, 0, 32, 64)
        painter.drawLine(0, 32, 64, 32)
        painter.end()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(pixmap))

        # Create tray menu
        tray_menu = QMenu()

        show_action = tray_menu.addAction("Settings")
        show_action.triggered.connect(self.showNormal)

        quit_action = tray_menu.addAction("Exit App")
        quit_action.triggered.connect(self.quit_app)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Double click on tray icon opens settings
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def quit_app(self):
        # Save one last time just in case
        config_manager.save_config(self.config)
        self.app.quit()

    def closeEvent(self, event):
        # Don't close, just hide to tray
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Virtual Crosshair",
            "Running in background. Click system tray icon to open settings or Exit to completely close.",
            QSystemTrayIcon.MessageIcon.Information,
            2000
        )
