from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QComboBox, QSpinBox, QCheckBox, QSlider, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from pathlib import Path
import json

class SettingsPanel(QWidget):
    """Application settings panel"""
    
    def __init__(self):
        super().__init__()
        self.config_file = Path("config.json")
        self.settings = self.load_settings()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Model Settings
        model_group = QGroupBox("⚙️ إعدادات النموذج")
        model_layout = QVBoxLayout()
        
        # Provider selection
        provider_layout = QHBoxLayout()
        provider_label = QLabel("مزود الحساب:")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["CPU", "CUDA", "TensorRT"])
        provider_combo_value = self.settings.get('provider', 'CPU')
        self.provider_combo.setCurrentText(provider_combo_value)
        provider_layout.addWidget(provider_label)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        
        # Max history
        history_layout = QHBoxLayout()
        history_label = QLabel("حد أقصى للمحادثة:")
        self.history_spin = QSpinBox()
        self.history_spin.setMinimum(5)
        self.history_spin.setMaximum(100)
        self.history_spin.setValue(self.settings.get('max_history', 20))
        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_spin)
        history_layout.addStretch()
        
        model_layout.addLayout(provider_layout)
        model_layout.addLayout(history_layout)
        model_group.setLayout(model_layout)
        
        # Display Settings
        display_group = QGroupBox("🎨 إعدادات العرض")
        display_layout = QVBoxLayout()
        
        # Font size
        font_layout = QHBoxLayout()
        font_label = QLabel("حجم الخط:")
        self.font_spin = QSpinBox()
        self.font_spin.setMinimum(8)
        self.font_spin.setMaximum(20)
        self.font_spin.setValue(self.settings.get('font_size', 11))
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_spin)
        font_layout.addStretch()
        
        # Dark mode
        self.dark_mode_check = QCheckBox("الوضع الداكن")
        self.dark_mode_check.setChecked(self.settings.get('dark_mode', True))
        
        display_layout.addLayout(font_layout)
        display_layout.addWidget(self.dark_mode_check)
        display_group.setLayout(display_layout)
        
        # Performance Settings
        perf_group = QGroupBox("⚡ إعدادات الأداء")
        perf_layout = QVBoxLayout()
        
        # Thread count
        threads_layout = QHBoxLayout()
        threads_label = QLabel("عدد المعالجات:")
        self.threads_spin = QSpinBox()
        self.threads_spin.setMinimum(1)
        self.threads_spin.setMaximum(16)
        self.threads_spin.setValue(self.settings.get('num_threads', 4))
        threads_layout.addWidget(threads_label)
        threads_layout.addWidget(self.threads_spin)
        threads_layout.addStretch()
        
        # Optimization
        self.optimization_check = QCheckBox("تفعيل التحسين")
        self.optimization_check.setChecked(self.settings.get('optimization', True))
        
        perf_layout.addLayout(threads_layout)
        perf_layout.addWidget(self.optimization_check)
        perf_group.setLayout(perf_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 حفظ الإعدادات")
        save_btn.clicked.connect(self.save_settings)
        
        reset_btn = QPushButton("🔄 إعادة تعيين")
        reset_btn.clicked.connect(self.reset_settings)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        button_layout.addStretch()
        
        # Main layout
        layout.addWidget(model_group)
        layout.addWidget(display_group)
        layout.addWidget(perf_group)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_settings(self) -> dict:
        """Load settings from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'provider': 'CPU',
            'max_history': 20,
            'font_size': 11,
            'dark_mode': True,
            'num_threads': 4,
            'optimization': True
        }
    
    def save_settings(self):
        """Save settings to file"""
        settings = {
            'provider': self.provider_combo.currentText(),
            'max_history': self.history_spin.value(),
            'font_size': self.font_spin.value(),
            'dark_mode': self.dark_mode_check.isChecked(),
            'num_threads': self.threads_spin.value(),
            'optimization': self.optimization_check.isChecked()
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "نجاح", "تم حفظ الإعدادات بنجاح!")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل حفظ الإعدادات: {str(e)}")
    
    def reset_settings(self):
        """Reset to default settings"""
        reply = QMessageBox.question(self, "تأكيد", "هل تريد إعادة تعيين الإعدادات للقيم الافتراضية؟")
        if reply == QMessageBox.StandardButton.Yes:
            self.config_file.unlink(missing_ok=True)
            self.settings = self.load_settings()
            # Reload UI
            self.provider_combo.setCurrentText(self.settings.get('provider', 'CPU'))
            self.history_spin.setValue(self.settings.get('max_history', 20))
            self.font_spin.setValue(self.settings.get('font_size', 11))
            self.dark_mode_check.setChecked(self.settings.get('dark_mode', True))
            self.threads_spin.setValue(self.settings.get('num_threads', 4))
            self.optimization_check.setChecked(self.settings.get('optimization', True))
            QMessageBox.information(self, "نجاح", "تم إعادة تعيين الإعدادات!")
    
    def get_settings(self) -> dict:
        """Get current settings"""
        return {
            'provider': self.provider_combo.currentText(),
            'max_history': self.history_spin.value(),
            'font_size': self.font_spin.value(),
            'dark_mode': self.dark_mode_check.isChecked(),
            'num_threads': self.threads_spin.value(),
            'optimization': self.optimization_check.isChecked()
        }
