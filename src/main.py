import sys
import logging

from PySide6.QtWidgets import QApplication, QCheckBox, QStyledItemDelegate, QMainWindow, QWidget, QTableView, QLabel, QVBoxLayout, QTableWidgetItem, QCheckBox, QTableWidget, QPushButton, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel


from context.db_context import DBContext
from widgets.weather import WeatherWidget

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WIDGETS = {
    "weather": WeatherWidget
}

class MainWindow(QMainWindow):
    """
    Main Window to manage widgets."""
    def __init__(self, ctx) -> None:
        super().__init__()
        self.build_ui()
    
    def _build_table(self):
        self.model = QSqlTableModel(self)
        self.model.setTable("widgets")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "name")
        self.model.setHeaderData(2, Qt.Horizontal, "enabled")
        self.model.setHeaderData(3, Qt.Horizontal, "createdAt")
        self.model.setHeaderData(4, Qt.Horizontal, "updatedAt")
        self.model.select()
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()

    def build_ui(self):
        logger.info("Building UI")
        self.setWindowTitle("Widgets")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self._build_table()
        self.setCentralWidget(self.table_view)
        self.setLayout(self.layout)

if __name__ == "__main__":
    context = DBContext("./database/main.sqlite")
    app = QApplication()
    context.load_conn()
    w = MainWindow(context)
    w.show()
    context.load_widgets(WIDGETS)
    sys.exit(app.exec())
