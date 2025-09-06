#!/usr/bin/env python3
"""
数据洞察助手 - 文件处理模块
负责CSV/Excel文件的上传、解析和预处理
"""

from .file_handler import FileHandler
from .data_analyzer import DataAnalyzer  
from .visualization import ChartGenerator
from .chat_interface import ChatInterface

__all__ = [
    'FileHandler',
    'DataAnalyzer', 
    'ChartGenerator',
    'ChatInterface'
]

__version__ = "1.0.0"
__author__ = "DASight Team"
__description__ = "数据洞察助手核心模块"