from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, 
    QListWidgetItem, QLabel, QGroupBox, QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtCore import pyqtSignal, Qt
from pathlib import Path
import os

class ModelManager(QWidget):
    """Model and DLL management widget"""
    
    model_loaded = pyqtSignal(str)
    dll_loaded = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.models_dir = Path("models")
        self.dlls_dir = Path("dlls")
        self.models_dir.mkdir(exist_ok=True)
        self.dlls_dir.mkdir(exist_ok=True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # ONNX Models Section
        models_group = QGroupBox("نماذج ONNX")
        models_layout = QVBoxLayout()
        
        self.models_list = QListWidget()
        self.refresh_models_list()
        
        models_btn_layout = QHBoxLayout()
        
        load_model_btn = QPushButton("📁 تحميل نموذج ONNX")
        load_model_btn.clicked.connect(self.load_onnx_model)
        
        refresh_models_btn = QPushButton("🔄 تحديث")
        refresh_models_btn.clicked.connect(self.refresh_models_list)
        
        models_btn_layout.addWidget(load_model_btn)
        models_btn_layout.addWidget(refresh_models_btn)
        
        models_layout.addWidget(QLabel("النماذج المتاحة:"))
        models_layout.addWidget(self.models_list)
        models_layout.addLayout(models_btn_layout)
        
        models_group.setLayout(models_layout)
        
        # DLL Files Section
        dlls_group = QGroupBox("ملفات DLL")
        dlls_layout = QVBoxLayout()
        
        self.dlls_list = QListWidget()
        self.refresh_dlls_list()
        
        dlls_btn_layout = QHBoxLayout()
        
        load_dll_btn = QPushButton("📁 تحميل ملف DLL")
        load_dll_btn.clicked.connect(self.load_dll_file)
        
        refresh_dlls_btn = QPushButton("🔄 تحديث")
        refresh_dlls_btn.clicked.connect(self.refresh_dlls_list)
        
        dlls_btn_layout.addWidget(load_dll_btn)
        dlls_btn_layout.addWidget(refresh_dlls_btn)
        
        dlls_layout.addWidget(QLabel("ملفات DLL المتاحة:"))
        dlls_layout.addWidget(self.dlls_list)
        dlls_layout.addLayout(dlls_btn_layout)
        
        dlls_group.setLayout(dlls_layout)
        
        layout.addWidget(models_group)
        layout.addWidget(dlls_group)
        
        self.setLayout(layout)
    
    def load_onnx_model(self):
        """Load ONNX model file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر نموذج ONNX", str(self.models_dir), 
            "ONNX Models (*.onnx);;All Files (*)"
        )
        
        if file_path:
            try:
                dest_path = self.models_dir / Path(file_path).name
                if not dest_path.exists():
                    import shutil
                    shutil.copy(file_path, dest_path)
                    QMessageBox.information(self, "نجاح", f"تم تحميل النموذج: {Path(file_path).name}")
                    self.refresh_models_list()
                    self.model_loaded.emit(str(dest_path))
                else:
                    QMessageBox.warning(self, "تحذير", "النموذج موجود بالفعل")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل تحميل النموذج: {str(e)}")
    
    def load_dll_file(self):
        """Load DLL file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف DLL", str(self.dlls_dir), 
            "DLL Files (*.dll);;All Files (*)"
        )
        
        if file_path:
            try:
                dest_path = self.dlls_dir / Path(file_path).name
                if not dest_path.exists():
                    import shutil
                    shutil.copy(file_path, dest_path)
                    QMessageBox.information(self, "نجاح", f"تم تحميل الملف: {Path(file_path).name}")
                    self.refresh_dlls_list()
                    self.dll_loaded.emit(str(dest_path))
                else:
                    QMessageBox.warning(self, "تحذير", "الملف موجود بالفعل")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل تحميل الملف: {str(e)}")
    
    def refresh_models_list(self):
        """Refresh ONNX models list"""
        self.models_list.clear()
        if self.models_dir.exists():
            for file in self.models_dir.glob("*.onnx"):
                item = QListWidgetItem(f"📦 {file.name}")
                item.setData(Qt.ItemDataRole.UserRole, str(file))
                self.models_list.addItem(item)
    
    def refresh_dlls_list(self):
        """Refresh DLL files list"""
        self.dlls_list.clear()
        if self.dlls_dir.exists():
            for file in self.dlls_dir.glob("*.dll"):
                item = QListWidgetItem(f"⚙️ {file.name}")
                item.setData(Qt.ItemDataRole.UserRole, str(file))
                self.dlls_list.addItem(item)
    
    def get_selected_model(self) -> str:
        """Get selected ONNX model path"""
        if self.models_list.currentItem():
            return self.models_list.currentItem().data(Qt.ItemDataRole.UserRole)
        return None
    
    def get_selected_dll(self) -> str:
        """Get selected DLL path"""
        if self.dlls_list.currentItem():
            return self.dlls_list.currentItem().data(Qt.ItemDataRole.UserRole)
        return None
