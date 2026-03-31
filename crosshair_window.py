from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QGuiApplication


class CrosshairOverlay(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_screen_size)
        # Check every second for resolution changes
        self.update_timer.start(1000)

    def initUI(self):
        # Make the window transparent and borderless
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.Tool  # Hide from taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.center_on_screen()
        self.show()

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen().geometry()
        # Keep window size slightly larger than max crosshair size to allow drawing
        window_size = 200
        self.setGeometry(
            (screen.width() - window_size) // 2,
            (screen.height() - window_size) // 2,
            window_size,
            window_size
        )

    def check_screen_size(self):
        # A simple check to re-center if screen resolution changes
        self.center_on_screen()

    def update_settings(self, new_config):
        self.config = new_config
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(self.config["color"])
        color.setAlpha(self.config["opacity"])

        pen = QPen(color)
        pen.setWidth(self.config["thickness"])
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        center_x = self.width() // 2
        center_y = self.height() // 2
        size = self.config["size"]

        shape = self.config["shape"]

        if shape in ["Cross", "Cross + Dot"]:
            # Draw Horizontal line
            painter.drawLine(center_x - size, center_y,
                             center_x + size, center_y)
            # Draw Vertical line
            painter.drawLine(center_x, center_y - size,
                             center_x, center_y + size)

        if shape in ["Dot", "Cross + Dot"]:
            # Draw a dot in the center
            # Adjust thickness for dot to be visible
            dot_pen = QPen(color)
            dot_thickness = max(2, self.config["thickness"] * 2)
            dot_pen.setWidth(dot_thickness)
            dot_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(dot_pen)
            painter.drawPoint(center_x, center_y)

        if shape == "Circle":
            # Draw a circle
            # Avoid the dot being drawn again by using standard pen
            painter.setPen(pen)
            painter.drawEllipse(center_x - size, center_y -
                                size, size * 2, size * 2)

        painter.end()
