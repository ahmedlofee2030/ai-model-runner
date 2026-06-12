# Professional Dark Theme Stylesheet

DARK_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QLineEdit, QTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 5px;
    padding: 8px;
    font-size: 11pt;
}

QLineEdit:focus, QTextEdit:focus {
    border: 2px solid #0d7377;
    background-color: #252525;
}

QPushButton {
    background-color: #0d7377;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 20px;
    font-size: 11pt;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #14a085;
}

QPushButton:pressed {
    background-color: #0a5c66;
}

QListWidget, QTableWidget {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    gridline-color: #404040;
}

QListWidget::item:selected, QTableWidget::item:selected {
    background-color: #0d7377;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #404040;
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background-color: #0d7377;
}

QLabel {
    color: #ffffff;
}

QGroupBox {
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 5px;
    margin-top: 8px;
    padding-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}

QTabWidget::pane {
    border: 1px solid #404040;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px 20px;
    margin-right: 2px;
    border: 1px solid #404040;
}

QTabBar::tab:selected {
    background-color: #0d7377;
    border: 1px solid #0d7377;
}

QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 5px;
    padding: 5px;
}

QComboBox:focus {
    border: 2px solid #0d7377;
}

QComboBox::drop-down {
    border: none;
    background-color: #0d7377;
    border-radius: 3px;
    margin-right: 2px;
}

QProgressBar {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 5px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0d7377;
    border-radius: 3px;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-top: 1px solid #404040;
}
"""
