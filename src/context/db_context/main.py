from PySide6.QtSql import QSqlDatabase, QSqlQuery
import logging

logger = logging.getLogger(__name__)

class DBContext:
  """
  DBContext class is responsible for handling the database connection and loading widgets from the database.
  """
  def __init__(self, db_path) -> None:
    self.db_path = db_path
    self.windows = []
    self.conn = None

  def load_conn(self):
      logger.info("Loading connection")
      self.conn = QSqlDatabase.addDatabase("QSQLITE")
      self.conn.setDatabaseName(self.db_path)
      self.conn.open()

  def load_widgets(self, widgets_map) -> None:
    if not self.conn or not self.conn.isOpen():
        self.load_conn()
    
    query = QSqlQuery(self.conn.database())
    query.prepare("SELECT * FROM widgets")
    query.exec()

    while query.next():
      widget_name = query.value(1)
      enabled = bool(query.value(2))
      widget = widgets_map.get(widget_name)
      if enabled and widget:
        current_widget = widget(self)
        self.windows.append(current_widget)
        current_widget.show()

  def save(self):
    pass