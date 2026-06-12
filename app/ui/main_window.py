from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QStatusBar, QMenuBar, QMenu, QMessageBox, QFileDialog, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject
from PyQt6.QtGui import QIcon, QFont
from pathlib import Path
import logging
import sys

from app.core.model_loader import ModelLoader
from app.core.chat_engine import ChatEngine
from app.ui.styles import DARK_STYLESHEET
from app.ui.chat_widget import ChatWidget
from app.ui.model_manager import ModelManager
from app.ui.settings_panel import SettingsPanel
from app.ui.model_info import ModelInfoWidget

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InferenceWorker(QObject):
    """Worker thread for model inference"""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str)
    
    def __init__(self, chat_engine, message):
        super().__init__()
        self.chat_engine = chat_engine
        self.message = message
    
    def run(self):
        try:
            response, success = self.chat_engine.process_message(self.message)
            self.result.emit(response)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.model_loader = ModelLoader()
        self.chat_engine = ChatEngine(self.model_loader)
        self.worker_thread = None
        self.init_ui()
        self.setup_menu()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("AI Model Runner - واجهة تشغيل النماذج الذكية")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Tabs
        tabs = QTabWidget()
        
        # Chat Tab
        self.chat_widget = ChatWidget()
        self.chat_widget.send_message.connect(self.on_send_message)
        tabs.addTab(self.chat_widget, "💬 الدردشة")
        
        # Model Manager Tab
        self.model_manager = ModelManager()
        self.model_manager.model_loaded.connect(self.on_model_loaded)
        self.model_manager.dll_loaded.connect(self.on_dll_loaded)
        tabs.addTab(self.model_manager, "📦 إدارة النماذج")
        
        # Model Info Tab
        self.model_info = ModelInfoWidget()
        tabs.addTab(self.model_info, "📊 معلومات النموذج")
        
        # Settings Tab
        self.settings_panel = SettingsPanel()
        tabs.addTab(self.settings_panel, "⚙️ الإعدادات")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage("جاهز للاستخدام ✅")
        
        # Progress bar in status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(300)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.setVisible(False)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("📁 ملف")
        
        load_model_action = file_menu.addAction("فتح نموذج ONNX")
        load_model_action.triggered.connect(self.on_load_model)
        
        load_dll_action = file_menu.addAction("فتح ملف DLL")
        load_dll_action.triggered.connect(self.on_load_dll)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("خروج")
        exit_action.triggered.connect(self.close)
        
        # Edit menu
        edit_menu = menubar.addMenu("✏️ تعديل")
        
        clear_action = edit_menu.addAction("مسح المحادثة")
        clear_action.triggered.connect(self.on_clear_chat)
        
        export_action = edit_menu.addAction("تصدير المحادثة")
        export_action.triggered.connect(self.on_export_chat)
        
        # Help menu
        help_menu = menubar.addMenu("❓ مساعدة")
        
        about_action = help_menu.addAction("حول التطبيق")
        about_action.triggered.connect(self.on_about)
    
    def apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet(DARK_STYLESHEET)
    
    def on_load_model(self):
        """Load ONNX model"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر نموذج ONNX", "", 
            "ONNX Models (*.onnx);;All Files (*)"
        )
        
        if file_path:
            success = self.model_loader.load_onnx_model(file_path)
            if success:
                self.statusBar().showMessage(f"✅ تم تحميل النموذج: {Path(file_path).name}")
                self.model_info.update_from_loader(self.model_loader)
                QMessageBox.information(self, "نجاح", f"تم تحميل النموذج بنجاح!")
            else:
                self.statusBar().showMessage("❌ فشل تحميل النموذج")
                QMessageBox.critical(self, "خطأ", "فشل تحميل النموذج. تأكد من صحة الملف.")
    
    def on_load_dll(self):
        """Load DLL file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف DLL", "", 
            "DLL Files (*.dll);;All Files (*)"
        )
        
        if file_path:
            success = self.model_loader.load_dll(file_path)
            if success:
                self.statusBar().showMessage(f"✅ تم تحميل الملف: {Path(file_path).name}")
                QMessageBox.information(self, "نجاح", f"تم تحميل الملف بنجاح!")
            else:
                self.statusBar().showMessage("❌ فشل تحميل الملف")
                QMessageBox.critical(self, "خطأ", "فشل تحميل الملف. تأكد من صحة الملف.")
    
    def on_model_loaded(self, model_path: str):
        """Handle model loaded signal"""
        success = self.model_loader.load_onnx_model(model_path)
        if success:
            self.statusBar().showMessage(f"✅ تم تحميل النموذج: {Path(model_path).name}")
            self.model_info.update_from_loader(self.model_loader)
    
    def on_dll_loaded(self, dll_path: str):
        """Handle DLL loaded signal"""
        success = self.model_loader.load_dll(dll_path)
        if success:
            self.statusBar().showMessage(f"✅ تم تحميل DLL: {Path(dll_path).name}")
    
    def on_send_message(self, message: str):
        """Handle message send"""
        if not self.model_loader.session:
            QMessageBox.warning(self, "تحذير", "الرجاء تحميل نموذج أولاً!")
            return
        
        self.progress_bar.setVisible(True)
        self.statusBar().showMessage("⏳ جاري المعالجة...")
        
        # Run inference in worker thread
        self.worker_thread = QThread()
        self.worker = InferenceWorker(self.chat_engine, message)
        self.worker.moveToThread(self.worker_thread)
        
        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.result.connect(self.on_inference_result)
        self.worker.error.connect(self.on_inference_error)
        
        self.worker_thread.start()
    
    def on_inference_result(self, result: str):
        """Handle inference result"""
        self.chat_widget.add_message(result, False)
        self.statusBar().showMessage("✅ تم المعالجة بنجاح")
        self.progress_bar.setVisible(False)
    
    def on_inference_error(self, error: str):
        """Handle inference error"""
        self.chat_widget.add_message(f"❌ خطأ: {error}", False)
        self.statusBar().showMessage(f"❌ خطأ: {error}")
        self.progress_bar.setVisible(False)
    
    def on_clear_chat(self):
        """Clear chat"""
        reply = QMessageBox.question(self, "تأكيد", "هل تريد مسح جميع الرسائل؟")
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_widget.clear_chat()
            self.chat_engine.clear_history()
            self.statusBar().showMessage("تم مسح المحادثة ✅")
    
    def on_export_chat(self):
        """Export chat history"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "حفظ المحادثة", "", "JSON Files (*.json);;Text Files (*.txt)"
        )
        
        if file_path:
            if file_path.endswith('.json'):
                success = self.chat_engine.export_history(file_path)
            else:
                # Export as text
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        for msg in self.chat_engine.get_history():
                            f.write(f"{msg['role'].upper()}: {msg['content']}\n\n")
                    success = True
                except:
                    success = False
            
            if success:
                QMessageBox.information(self, "نجاح", f"تم حفظ المحادثة في:\n{file_path}")
            else:
                QMessageBox.critical(self, "خطأ", "فشل حفظ المحادثة")
    
    def on_about(self):
        """Show about dialog"""
        QMessageBox.information(
            self,
            "حول التطبيق",
            "AI Model Runner v1.0.0\n\n"
            "تطبيق احترافي لتشغيل نماذج ONNX ودعم ملفات DLL\n\n"
            "المميزات:\n"
            "✅ دعم جميع أنواع نماذج ONNX\n"
            "✅ دعم ملفات DLL\n"
            "✅ واجهة دردشة احترافية\n"
            "✅ معلومات تفصيلية عن النموذج\n"
            "✅ تصدير المحادثات\n\n"
            "تطوير: Ahmed Lofee"
        )
    
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(
            self, 'تأكيد', 'هل تريد إغلاق التطبيق؟'
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
