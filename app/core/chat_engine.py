import numpy as np
from typing import Optional, Dict, List, Tuple
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatEngine:
    """Chat engine that works with ONNX models"""
    
    def __init__(self, model_loader):
        self.model_loader = model_loader
        self.conversation_history = []
        self.max_history = 20
        
    def process_message(self, user_message: str) -> Tuple[str, bool]:
        """Process user message and generate response"""
        try:
            # Add to history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now()
            })
            
            # Check if model is loaded
            if not self.model_loader.session:
                response = "❌ لا توجد نماذج محملة. الرجاء تحميل نموذج ONNX أولاً."
                return response, False
            
            # Get model info
            model_info = self.model_loader.get_model_info()
            
            # Prepare input based on model type
            response, success = self._generate_response(user_message, model_info)
            
            # Add to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            # Keep history size limited
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            return response, success
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return f"❌ خطأ: {str(e)}", False
    
    def _generate_response(self, user_message: str, model_info: Dict) -> Tuple[str, bool]:
        """Generate response using ONNX model"""
        try:
            # Prepare input based on model input shapes
            inputs = self._prepare_inputs(user_message, model_info)
            
            if inputs is None:
                return "❌ فشل في تحضير المدخلات", False
            
            # Run inference
            output = self.model_loader.run_inference(inputs)
            
            if output is None:
                return "❌ فشل في تشغيل الاستدلال", False
            
            # Process output
            response = self._process_output(output, model_info)
            
            return response, True
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"❌ خطأ في التوليد: {str(e)}", False
    
    def _prepare_inputs(self, user_message: str, model_info: Dict) -> Optional[Dict]:
        """Prepare inputs for model based on input shapes"""
        try:
            inputs = {}
            input_names = model_info.get('inputs', {}).get('names', [])
            input_shapes = model_info.get('inputs', {}).get('shapes', [])
            
            if not input_names:
                return None
            
            # Create dummy input matching first input shape
            for name, shape in zip(input_names, input_shapes):
                # Handle dynamic shapes
                if isinstance(shape, (list, tuple)):
                    shape = list(shape)
                    # Replace -1 or None with 1 for dynamic dimensions
                    shape = [1 if (s == -1 or s is None) else s for s in shape]
                else:
                    shape = [1]
                
                # Create input based on shape
                try:
                    inputs[name] = np.random.randn(*shape).astype(np.float32)
                except:
                    inputs[name] = np.array([[1.0]], dtype=np.float32)
            
            return inputs
            
        except Exception as e:
            logger.error(f"Error preparing inputs: {str(e)}")
            return None
    
    def _process_output(self, output: Dict, model_info: Dict) -> str:
        """Process model output into readable response"""
        try:
            response_parts = []
            
            for output_name, output_value in output.items():
                if isinstance(output_value, np.ndarray):
                    # Get shape and type info
                    shape = output_value.shape
                    dtype = output_value.dtype
                    
                    # Create readable output
                    if output_value.size <= 10:
                        # Small outputs - show all values
                        values_str = ', '.join([f"{v:.4f}" for v in output_value.flatten()])
                        response_parts.append(f"📊 {output_name}: [{values_str}]")
                    else:
                        # Large outputs - show statistics
                        response_parts.append(f"📊 {output_name}:")
                        response_parts.append(f"  الشكل: {shape}")
                        response_parts.append(f"  النوع: {dtype}")
                        response_parts.append(f"  الحد الأدنى: {output_value.min():.4f}")
                        response_parts.append(f"  الحد الأقصى: {output_value.max():.4f}")
                        response_parts.append(f"  المتوسط: {output_value.mean():.4f}")
            
            if response_parts:
                return "\n".join(response_parts)
            else:
                return "✅ تم التشغيل بنجاح"
            
        except Exception as e:
            logger.error(f"Error processing output: {str(e)}")
            return f"❌ خطأ في معالجة المخرجات: {str(e)}"
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def export_history(self, filepath: str):
        """Export conversation history to file"""
        try:
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2, default=str)
            logger.info(f"History exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error exporting history: {str(e)}")
            return False
