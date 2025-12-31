"""
Views package
"""
from . import home
from . import single_prediction
from . import model_performance
from . import shap_analysis
from . import data_visualization
from . import batch_prediction
from . import model_comparison

__all__ = [
    'home',
    'single_prediction',
    'model_performance',
    'shap_analysis',
    'data_visualization',
    'batch_prediction',
    'model_comparison'
]
