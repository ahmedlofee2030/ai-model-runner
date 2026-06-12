from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QScrollArea, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

class ChatMessage(QFrame):
    """Single chat message widget"""
    
    def __init__(self, message: str, is_user: bool = True):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #0d7377 if user else #2d2d2d;
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Sender label
        sender_label = QLabel("أنت" if is_user else "النموذج")
        sender_font = QFont()
        sender_font.setBold(True)
        sender_font.setPointSize(9)
        sender_label.setFont(sender_font)
        sender_label.setStyleSheet(f"color: {'white' if is_user else '#0d7377'};")
        
        # Message text
        text_label = QLabel(message)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: white;")
        text_font = QFont()
        text_font.setPointSize(10)
        text_label.setFont(text_font)
        
        # Time label
        time_label = QLabel(datetime.now().strftime("%H:%M:%S"))
        time_label.setStyleSheet("color: #999999; font-size: 8pt;")
        
        layout.addWidget(sender_label)
        layout.addWidget(text_label)
        layout.addWidget(time_label)
        layout.addSpacing(0)
        
        self.setLayout(layout)

class ChatWidget(QWidget):
    """Chat interface widget"""
    
    send_message = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Chat display area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_container)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_text = QTextEdit()
        self.input_text.setMaximumHeight(80)
        self.input_text.setPlaceholderText("اكتب رسالتك هنا...")
        self.input_text.setAcceptRichText(False)
        
        self.send_btn = QPushButton("إرسال")
        self.send_btn.setMaximumWidth(100)
        self.send_btn.clicked.connect(self.send_message_action)
        
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.send_btn)
        
        layout.addWidget(self.chat_scroll)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
    
    def send_message_action(self):
        message = self.input_text.toPlainText().strip()
        if message:
            self.send_message.emit(message)
            self.add_message(message, True)
            self.input_text.clear()
    
    def add_message(self, message: str, is_user: bool = False):
        """Add message to chat"""
        chat_msg = ChatMessage(message, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, chat_msg)
        self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        )
    
    def clear_chat(self):
        """Clear all messages"""
        while self.chat_layout.count() > 1:
            self.chat_layout.itemAt(0).widget().deleteLater()
