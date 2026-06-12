import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    # Create necessary directories
    Path("models").mkdir(exist_ok=True)
    Path("dlls").mkdir(exist_ok=True)
    Path("temp").mkdir(exist_ok=True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("AI Model Runner")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
