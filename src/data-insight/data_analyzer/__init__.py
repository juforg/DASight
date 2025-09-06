#!/usr/bin/env python3
"""
数据分析模块
负责数据的统计分析、模式识别和洞察生成
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DataAnalyzer:
    """数据分析器，提供各种数据分析功能"""
    
    def __init__(self):
        self.current_data = None
        self.metadata = None
    
    def load_data(self, df: pd.DataFrame, metadata: Dict[str, Any]):
        """加载数据到分析器"""
        self.current_data = df
        self.metadata = metadata
    
    def basic_statistics(self) -> Dict[str, Any]:
        """计算基础统计信息"""
        if self.current_data is None:
            raise ValueError("没有加载数据")
        
        numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
        
        stats = {
            'data_shape': self.current_data.shape,
            'numeric_columns': len(numeric_cols),
            'text_columns': len(self.current_data.columns) - len(numeric_cols),
            'missing_values_total': self.current_data.isnull().sum().sum(),
            'duplicate_rows': self.current_data.duplicated().sum(),
        }
        
        if len(numeric_cols) > 0:
            stats['numeric_summary'] = self.current_data[numeric_cols].describe().to_dict()
        
        return stats
    
    def column_analysis(self, column_name: str) -> Dict[str, Any]:
        """分析特定列的详细信息"""
        if self.current_data is None:
            raise ValueError("没有加载数据")
        
        if column_name not in self.current_data.columns:
            raise ValueError(f"列 '{column_name}' 不存在")
        
        col_data = self.current_data[column_name]
        
        analysis = {
            'column_name': column_name,
            'data_type': str(col_data.dtype),
            'null_count': col_data.isnull().sum(),
            'null_percentage': (col_data.isnull().sum() / len(col_data)) * 100,
            'unique_values': col_data.nunique(),
        }
        
        if pd.api.types.is_numeric_dtype(col_data):
            analysis.update({
                'min': col_data.min(),
                'max': col_data.max(),
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std(),
            })
        else:
            # 分类数据分析
            analysis.update({
                'most_frequent': col_data.mode().iloc[0] if not col_data.mode().empty else None,
                'value_counts': col_data.value_counts().head().to_dict(),
            })
        
        return analysis
    
    def correlation_analysis(self) -> Dict[str, Any]:
        """计算数值列之间的相关性"""
        if self.current_data is None:
            raise ValueError("没有加载数据")
        
        numeric_df = self.current_data.select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {'message': '没有数值列可以计算相关性'}
        
        correlation_matrix = numeric_df.corr()
        
        # 找出强相关性的列对
        strong_correlations = []
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:  # 强相关性阈值
                    strong_correlations.append({
                        'column1': correlation_matrix.columns[i],
                        'column2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        return {
            'correlation_matrix': correlation_matrix.to_dict(),
            'strong_correlations': strong_correlations
        }
    
    def detect_outliers(self, column_name: str) -> Dict[str, Any]:
        """检测指定列的异常值"""
        if self.current_data is None:
            raise ValueError("没有加载数据")
        
        if column_name not in self.current_data.columns:
            raise ValueError(f"列 '{column_name}' 不存在")
        
        col_data = self.current_data[column_name]
        
        if not pd.api.types.is_numeric_dtype(col_data):
            return {'message': f'列 {column_name} 不是数值类型，无法检测异常值'}
        
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        
        return {
            'column_name': column_name,
            'outlier_count': len(outliers),
            'outlier_percentage': (len(outliers) / len(col_data)) * 100,
            'outlier_values': outliers.tolist(),
            'bounds': {
                'lower': lower_bound,
                'upper': upper_bound
            }
        }