from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu, QCheckBox, QStyledItemDelegate, QMainWindow, QWidget, QTableView, QLabel, QVBoxLayout, QTableWidgetItem, QCheckBox, QTableWidget, QPushButton, QHeaderView
from PySide6.QtGui import QMouseEvent, QAction

class WeatherWidget(QWidget):
    """
    A Custom widget to display weather information."""
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.drag_start_position = None
        self.build_ui()
    
    def _close(self):
        self.close()    
    
    def _build_right_click_menu(self):
        self.menu = QMenu()
        self.action = QAction("Close", self)
        self.action.triggered.connect(self._close)
        self.menu.addAction(self.action)
    
    def build_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Weather")
        self.layout.addWidget(self.label)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["City", "Temperature"])
        self.table.setRowCount(3)
        self.table.setItem(0, 0, QTableWidgetItem("New York"))
        self.table.setItem(0, 1, QTableWidgetItem("72°F"))
        self.table.setItem(1, 0, QTableWidgetItem("London"))
        self.table.setItem(1, 1, QTableWidgetItem("65°F"))
        self.table.setItem(2, 0, QTableWidgetItem("Tokyo"))
        self.table.setItem(2, 1, QTableWidgetItem("80°F"))
        self.layout.addWidget(self.table)
        self._build_right_click_menu()
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        
        if event.button() == Qt.RightButton:
            self.menu.exec(event.globalPos())
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggable and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.draggable = False
            event.accept()