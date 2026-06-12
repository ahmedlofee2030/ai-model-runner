import onnxruntime as rt
import numpy as np
import ctypes
import os
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """Load and manage ONNX models and DLL files"""
    
    def __init__(self):
        self.session = None
        self.model_path = None
        self.dll_functions = {}
        self.model_info = {}
        
    def load_onnx_model(self, model_path: str) -> bool:
        """Load ONNX model and get session"""
        try:
            if not os.path.exists(model_path):
                logger.error(f"Model not found: {model_path}")
                return False
            
            # Create ONNX Runtime session
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            self.session = rt.InferenceSession(model_path, providers=providers)
            self.model_path = model_path
            
            # Get model information
            self._extract_model_info()
            logger.info(f"Model loaded successfully: {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading ONNX model: {str(e)}")
            return False
    
    def load_dll(self, dll_path: str, function_names: list = None) -> bool:
        """Load DLL file and extract functions"""
        try:
            if not os.path.exists(dll_path):
                logger.error(f"DLL not found: {dll_path}")
                return False
            
            # Load DLL
            dll = ctypes.CDLL(dll_path)
            dll_name = Path(dll_path).stem
            self.dll_functions[dll_name] = {
                'handle': dll,
                'functions': {},
                'path': dll_path
            }
            
            # Extract specified functions
            if function_names:
                for func_name in function_names:
                    try:
                        func = getattr(dll, func_name)
                        self.dll_functions[dll_name]['functions'][func_name] = func
                    except AttributeError:
                        logger.warning(f"Function {func_name} not found in {dll_name}")
            
            logger.info(f"DLL loaded successfully: {dll_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading DLL: {str(e)}")
            return False
    
    def _extract_model_info(self):
        """Extract input and output information from model"""
        if not self.session:
            return
        
        try:
            # Get input info
            input_names = [input.name for input in self.session.get_inputs()]
            input_shapes = [input.shape for input in self.session.get_inputs()]
            input_types = [input.type for input in self.session.get_inputs()]
            
            # Get output info
            output_names = [output.name for output in self.session.get_outputs()]
            output_shapes = [output.shape for output in self.session.get_outputs()]
            output_types = [output.type for output in self.session.get_outputs()]
            
            self.model_info = {
                'inputs': {
                    'names': input_names,
                    'shapes': input_shapes,
                    'types': input_types
                },
                'outputs': {
                    'names': output_names,
                    'shapes': output_shapes,
                    'types': output_types
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting model info: {str(e)}")
    
    def run_inference(self, inputs: Dict[str, np.ndarray]) -> Optional[Dict]:
        """Run inference on loaded model"""
        try:
            if not self.session:
                logger.error("No model loaded")
                return None
            
            output = self.session.run(None, inputs)
            
            # Create output dictionary
            output_dict = {}
            for i, name in enumerate(self.model_info['outputs']['names']):
                output_dict[name] = output[i]
            
            return output_dict
            
        except Exception as e:
            logger.error(f"Error during inference: {str(e)}")
            return None
    
    def get_model_info(self) -> Dict:
        """Get loaded model information"""
        return self.model_info
    
    def get_dll_functions(self, dll_name: str) -> Dict:
        """Get functions from loaded DLL"""
        if dll_name in self.dll_functions:
            return self.dll_functions[dll_name]['functions']
        return {}
    
    def call_dll_function(self, dll_name: str, func_name: str, *args, **kwargs) -> Any:
        """Call function from loaded DLL"""
        try:
            if dll_name not in self.dll_functions:
                logger.error(f"DLL {dll_name} not loaded")
                return None
            
            if func_name not in self.dll_functions[dll_name]['functions']:
                logger.error(f"Function {func_name} not found in {dll_name}")
                return None
            
            func = self.dll_functions[dll_name]['functions'][func_name]
            return func(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error calling DLL function: {str(e)}")
            return None
    
    def unload_all(self):
        """Unload all models and DLLs"""
        self.session = None
        self.model_path = None
        self.dll_functions = {}
        self.model_info = {}
        logger.info("All models unloaded")
