#!/usr/bin/env python3
"""
基础数据分析器 - 用于快速数据处理和分析
为MCP服务集成做准备
"""

import pandas as pd
import numpy as np
import json
import os
from typing import Dict, List, Any, Optional

class BasicDataAnalyzer:
    """基础数据分析器"""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_path: Optional[str] = None
        self.file_info: Dict = {}
    
    def load_file(self, file_path: str) -> Dict[str, Any]:
        """
        加载CSV/Excel文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 包含文件基本信息的字典
        """
        self.file_path = file_path
        
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 根据文件扩展名加载
            if file_path.lower().endswith('.csv'):
                # 尝试不同编码
                encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
                for encoding in encodings:
                    try:
                        self.df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("无法识别CSV文件编码")
                    
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                # Excel文件处理，尝试多种引擎
                engines = ['openpyxl', 'xlrd', None]  # None表示自动选择
                last_error = None
                
                for engine in engines:
                    try:
                        if engine is None:
                            self.df = pd.read_excel(file_path)
                        else:
                            self.df = pd.read_excel(file_path, engine=engine)
                        break  # 成功读取，跳出循环
                    except Exception as e:
                        last_error = e
                        continue
                else:
                    # 所有引擎都失败了
                    raise ValueError(f"无法读取Excel文件，尝试的引擎都失败了。最后的错误: {str(last_error)}")
            else:
                raise ValueError("不支持的文件格式，仅支持CSV和Excel文件")
            
            # 获取文件基本信息
            self.file_info = self._get_file_info()
            return self.file_info
            
        except Exception as e:
            error_info = {
                'error': True,
                'message': f"文件加载失败: {str(e)}",
                'file_path': file_path
            }
            return error_info
    
    def _get_file_info(self) -> Dict[str, Any]:
        """获取文件基本信息"""
        if self.df is None:
            return {'error': True, 'message': '没有加载数据'}
        
        # 文件基本信息
        file_stats = os.stat(self.file_path)
        
        # 数据基本信息
        basic_info = {
            'file_name': os.path.basename(self.file_path),
            'file_size': f"{file_stats.st_size / 1024 / 1024:.2f} MB",
            'shape': {
                'rows': int(self.df.shape[0]),
                'columns': int(self.df.shape[1])
            },
            'columns': list(self.df.columns),
            'dtypes': {col: str(dtype) for col, dtype in self.df.dtypes.items()},
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
        
        # 数据预览
        basic_info['preview'] = {
            'head': self.df.head(5).fillna('NULL').to_dict(orient='records'),
            'tail': self.df.tail(5).fillna('NULL').to_dict(orient='records')
        }
        
        return basic_info
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """获取汇总统计信息"""
        if self.df is None:
            return {'error': True, 'message': '没有加载数据'}
        
        try:
            # 数值型列统计
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            numeric_stats = {}
            
            if len(numeric_cols) > 0:
                desc = self.df[numeric_cols].describe()
                numeric_stats = desc.fillna(0).to_dict()
            
            # 文本型列统计
            text_cols = self.df.select_dtypes(include=['object']).columns
            text_stats = {}
            
            for col in text_cols:
                text_stats[col] = {
                    'unique_count': int(self.df[col].nunique()),
                    'most_frequent': str(self.df[col].mode().iloc[0]) if not self.df[col].mode().empty else 'N/A',
                    'null_count': int(self.df[col].isnull().sum())
                }
            
            # 缺失值统计
            missing_stats = {
                col: {
                    'count': int(self.df[col].isnull().sum()),
                    'percentage': round(self.df[col].isnull().sum() / len(self.df) * 100, 2)
                }
                for col in self.df.columns
            }
            
            return {
                'numeric_statistics': numeric_stats,
                'text_statistics': text_stats,
                'missing_values': missing_stats,
                'total_rows': int(len(self.df)),
                'total_columns': int(len(self.df.columns))
            }
            
        except Exception as e:
            return {'error': True, 'message': f"统计计算失败: {str(e)}"}
    
    def prepare_chart_data(self, x_col: str, y_col: str = None, chart_type: str = 'bar', 
                          limit: int = 20) -> Dict[str, Any]:
        """
        准备图表数据
        
        Args:
            x_col: X轴列名
            y_col: Y轴列名（可选）
            chart_type: 图表类型 ('bar', 'line', 'pie', 'scatter')
            limit: 数据点限制
            
        Returns:
            Dict: 图表数据
        """
        if self.df is None:
            return {'error': True, 'message': '没有加载数据'}
        
        if x_col not in self.df.columns:
            return {'error': True, 'message': f'列 {x_col} 不存在'}
        
        try:
            if chart_type == 'bar':
                # 柱状图：分组统计
                if y_col and y_col in self.df.columns:
                    # 有Y轴：按X分组求Y的和
                    data = self.df.groupby(x_col)[y_col].sum().reset_index()
                    data = data.head(limit)
                else:
                    # 无Y轴：按X分组计数
                    data = self.df[x_col].value_counts().head(limit).reset_index()
                    data.columns = [x_col, 'count']
                    y_col = 'count'
                
                return {
                    'type': 'bar',
                    'data': {
                        'labels': data[x_col].astype(str).tolist(),
                        'datasets': [{
                            'label': y_col or 'Count',
                            'data': data[y_col].tolist()
                        }]
                    },
                    'title': f'{y_col or "Count"} by {x_col}'
                }
            
            elif chart_type == 'line':
                # 折线图：需要数值型数据
                if y_col and y_col in self.df.columns:
                    data = self.df[[x_col, y_col]].head(limit)
                    return {
                        'type': 'line',
                        'data': {
                            'labels': data[x_col].astype(str).tolist(),
                            'datasets': [{
                                'label': y_col,
                                'data': data[y_col].tolist()
                            }]
                        },
                        'title': f'{y_col} Trend by {x_col}'
                    }
                else:
                    return {'error': True, 'message': '折线图需要指定Y轴列'}
            
            elif chart_type == 'pie':
                # 饼图：按类别分组
                data = self.df[x_col].value_counts().head(limit)
                return {
                    'type': 'pie',
                    'data': {
                        'labels': data.index.astype(str).tolist(),
                        'datasets': [{
                            'data': data.values.tolist()
                        }]
                    },
                    'title': f'Distribution of {x_col}'
                }
            
            elif chart_type == 'scatter':
                # 散点图：需要两个数值列
                if y_col and y_col in self.df.columns:
                    data = self.df[[x_col, y_col]].head(limit)
                    return {
                        'type': 'scatter',
                        'data': {
                            'datasets': [{
                                'label': f'{x_col} vs {y_col}',
                                'data': [
                                    {'x': row[x_col], 'y': row[y_col]} 
                                    for _, row in data.iterrows()
                                ]
                            }]
                        },
                        'title': f'{x_col} vs {y_col}'
                    }
                else:
                    return {'error': True, 'message': '散点图需要指定Y轴列'}
            
            else:
                return {'error': True, 'message': f'不支持的图表类型: {chart_type}'}
                
        except Exception as e:
            return {'error': True, 'message': f'图表数据准备失败: {str(e)}'}
    
    def query_data(self, query: str) -> Dict[str, Any]:
        """
        简单的数据查询
        
        Args:
            query: 查询字符串（简化版SQL-like语法）
            
        Returns:
            Dict: 查询结果
        """
        if self.df is None:
            return {'error': True, 'message': '没有加载数据'}
        
        try:
            # 简单的查询解析
            query = query.lower().strip()
            
            if 'shape' in query or '多少行' in query or '多少列' in query:
                return {
                    'type': 'info',
                    'result': f"数据有 {self.df.shape[0]} 行，{self.df.shape[1]} 列"
                }
            
            elif 'columns' in query or '列名' in query or '字段' in query:
                return {
                    'type': 'list',
                    'result': f"列名: {', '.join(self.df.columns)}"
                }
            
            elif 'head' in query or '前几行' in query:
                return {
                    'type': 'table',
                    'result': self.df.head().fillna('NULL').to_dict(orient='records')
                }
            
            elif 'describe' in query or '统计' in query:
                desc = self.df.describe()
                return {
                    'type': 'table',
                    'result': desc.fillna(0).to_dict()
                }
            
            else:
                return {
                    'type': 'info', 
                    'result': '支持的查询: shape, columns, head, describe'
                }
                
        except Exception as e:
            return {'error': True, 'message': f'查询失败: {str(e)}'}

# 使用示例
if __name__ == "__main__":
    analyzer = BasicDataAnalyzer()
    
    # 测试基本功能
    print("数据分析器初始化完成")
    print("支持的功能:")
    print("1. load_file(file_path) - 加载数据文件")
    print("2. get_summary_statistics() - 获取统计信息")
    print("3. prepare_chart_data(x_col, y_col, chart_type) - 准备图表数据")
    print("4. query_data(query) - 简单数据查询")