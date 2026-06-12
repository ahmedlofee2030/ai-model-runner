from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt6.QtCore import Qt
from app.core.model_loader import ModelLoader

class ModelInfoWidget(QWidget):
    """Display model information"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Inputs section
        inputs_group = QGroupBox("📥 مدخلات النموذج")
        inputs_layout = QVBoxLayout()
        
        self.inputs_table = QTableWidget()
        self.inputs_table.setColumnCount(3)
        self.inputs_table.setHorizontalHeaderLabels(["الاسم", "الشكل", "النوع"])
        self.inputs_table.horizontalHeader().setStretchLastSection(True)
        
        inputs_layout.addWidget(self.inputs_table)
        inputs_group.setLayout(inputs_layout)
        
        # Outputs section
        outputs_group = QGroupBox("📤 مخرجات النموذج")
        outputs_layout = QVBoxLayout()
        
        self.outputs_table = QTableWidget()
        self.outputs_table.setColumnCount(3)
        self.outputs_table.setHorizontalHeaderLabels(["الاسم", "الشكل", "النوع"])
        self.outputs_table.horizontalHeader().setStretchLastSection(True)
        
        outputs_layout.addWidget(self.outputs_table)
        outputs_group.setLayout(outputs_layout)
        
        # Info section
        info_group = QGroupBox("ℹ️ معلومات عامة")
        info_layout = QVBoxLayout()
        
        self.info_label = QLabel("لم يتم تحميل أي نموذج بعد")
        self.info_label.setWordWrap(True)
        
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        
        layout.addWidget(inputs_group)
        layout.addWidget(outputs_group)
        layout.addWidget(info_group)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def update_from_loader(self, loader: ModelLoader):
        """Update display from model loader"""
        info = loader.get_model_info()
        
        if not info:
            self.info_label.setText("لم يتم تحميل أي نموذج بعد")
            return
        
        # Update inputs
        inputs = info.get('inputs', {})
        self.inputs_table.setRowCount(len(inputs.get('names', [])))
        
        for i, (name, shape, dtype) in enumerate(zip(
            inputs.get('names', []),
            inputs.get('shapes', []),
            inputs.get('types', [])
        )):
            self.inputs_table.setItem(i, 0, QTableWidgetItem(name))
            self.inputs_table.setItem(i, 1, QTableWidgetItem(str(shape)))
            self.inputs_table.setItem(i, 2, QTableWidgetItem(str(dtype)))
        
        # Update outputs
        outputs = info.get('outputs', {})
        self.outputs_table.setRowCount(len(outputs.get('names', [])))
        
        for i, (name, shape, dtype) in enumerate(zip(
            outputs.get('names', []),
            outputs.get('shapes', []),
            outputs.get('types', [])
        )):
            self.outputs_table.setItem(i, 0, QTableWidgetItem(name))
            self.outputs_table.setItem(i, 1, QTableWidgetItem(str(shape)))
            self.outputs_table.setItem(i, 2, QTableWidgetItem(str(dtype)))
        
        # Update info
        info_text = f"""✅ تم تحميل النموذج بنجاح
        
📊 الإحصائيات:
• عدد المدخلات: {len(inputs.get('names', []))}
• عدد المخرجات: {len(outputs.get('names', []))}
• حجم المدخلات الكلي: {sum(1 for shape in inputs.get('shapes', []) for s in (shape if isinstance(shape, (list, tuple)) else [shape]))}
        """
        
        self.info_label.setText(info_text)
