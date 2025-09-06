#!/usr/bin/env python3
"""
文件处理模块
负责CSV/Excel文件的上传、解析和预处理
"""

import pandas as pd
import os
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class FileHandler:
    """文件处理器，负责文件上传和解析"""
    
    def __init__(self, upload_dir: str = "/Users/songjie/Downloads/DASight/data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """保存上传的文件"""
        file_path = self.upload_dir / filename
        with open(file_path, 'wb') as f:
            f.write(file_content)
        return str(file_path)
    
    def parse_file(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """解析文件并返回DataFrame和元数据"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            metadata = {
                'filename': Path(file_path).name,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'dtypes': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'file_size': os.path.getsize(file_path)
            }
            
            return df, metadata
            
        except Exception as e:
            logger.error(f"文件解析失败: {e}")
            raise
    
    def validate_file(self, file_path: str) -> bool:
        """验证文件格式和大小"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            # 检查文件扩展名
            if path.suffix.lower() not in ['.csv', '.xlsx', '.xls']:
                return False
            
            # 检查文件大小 (限制100MB)
            if path.stat().st_size > 100 * 1024 * 1024:
                return False
                
            return True
        except Exception:
            return False