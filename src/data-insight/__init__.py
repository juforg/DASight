#!/usr/bin/env python3
"""
数据洞察助手 - 数据分析模块
包含基础分析、图表生成和流程协调功能
"""

from .basic_analyzer import BasicDataAnalyzer
from .chart_connector import AntVChartConnector
from .coordinator import DataInsightCoordinator

__all__ = [
    'BasicDataAnalyzer',
    'AntVChartConnector', 
    'DataInsightCoordinator'
]

__version__ = "1.0.0"
__author__ = "DASight Team"
__description__ = "数据洞察助手核心分析模块"