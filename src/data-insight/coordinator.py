#!/usr/bin/env python3
"""
数据洞察协调器 - 统一管理数据分析和图表生成流程
整合basic_analyzer和chart_connector
"""

import os
import json
from typing import Dict, Any, Optional, List
from basic_analyzer import BasicDataAnalyzer
from chart_connector import AntVChartConnector

class DataInsightCoordinator:
    """数据洞察协调器"""
    
    def __init__(self):
        self.analyzer = BasicDataAnalyzer()
        self.chart_connector = AntVChartConnector()
        self.current_file = None
        self.analysis_history = []
    
    def process_file_upload(self, file_path: str) -> Dict[str, Any]:
        """
        处理文件上传
        
        Args:
            file_path: 上传的文件路径
            
        Returns:
            Dict: 处理结果
        """
        try:
            # 加载文件
            file_info = self.analyzer.load_file(file_path)
            
            if file_info.get('error'):
                return file_info
            
            self.current_file = file_path
            
            # 获取统计信息
            stats = self.analyzer.get_summary_statistics()
            
            # 合并结果
            result = {
                'status': 'success',
                'message': '文件处理成功',
                'file_info': file_info,
                'statistics': stats,
                'recommendations': self._generate_recommendations(file_info, stats)
            }
            
            # 记录分析历史
            self.analysis_history.append({
                'action': 'file_upload',
                'file_path': file_path,
                'timestamp': self._get_timestamp(),
                'result': result
            })
            
            return result
            
        except Exception as e:
            error_result = {
                'status': 'error',
                'message': f'文件处理失败: {str(e)}'
            }
            return error_result
    
    def analyze_data(self, query: str) -> Dict[str, Any]:
        """
        分析数据
        
        Args:
            query: 分析查询
            
        Returns:
            Dict: 分析结果
        """
        if not self.current_file:
            return {
                'status': 'error',
                'message': '请先上传数据文件'
            }
        
        try:
            # 执行查询
            query_result = self.analyzer.query_data(query)
            
            # 记录分析历史
            self.analysis_history.append({
                'action': 'data_analysis',
                'query': query,
                'timestamp': self._get_timestamp(),
                'result': query_result
            })
            
            return {
                'status': 'success',
                'query': query,
                'result': query_result,
                'suggestions': self._generate_analysis_suggestions(query_result)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'数据分析失败: {str(e)}'
            }
    
    def generate_chart(self, x_col: str, y_col: str = None, 
                      chart_type: str = 'bar', title: str = None) -> Dict[str, Any]:
        """
        生成图表
        
        Args:
            x_col: X轴列名
            y_col: Y轴列名
            chart_type: 图表类型
            title: 图表标题
            
        Returns:
            Dict: 图表生成结果
        """
        if not self.current_file:
            return {
                'status': 'error',
                'message': '请先上传数据文件'
            }
        
        try:
            # 准备图表数据
            chart_data = self.analyzer.prepare_chart_data(x_col, y_col, chart_type)
            
            if chart_data.get('error'):
                return chart_data
            
            # 设置标题
            if title:
                chart_data['title'] = title
            
            # 生成图表配置
            config_result = self.chart_connector.generate_chart_json(chart_data)
            
            if config_result['status'] != 'success':
                return config_result
            
            # 生成HTML文件
            html_result = self.chart_connector.generate_chart_html(
                config_result['config']
            )
            
            # 合并结果
            result = {
                'status': 'success',
                'message': '图表生成成功',
                'chart_data': chart_data,
                'config_file': config_result['config_file'],
                'html_file': html_result['html_file'],
                'chart_url': html_result['url']
            }
            
            # 记录分析历史
            self.analysis_history.append({
                'action': 'chart_generation',
                'params': {
                    'x_col': x_col,
                    'y_col': y_col,
                    'chart_type': chart_type,
                    'title': title
                },
                'timestamp': self._get_timestamp(),
                'result': result
            })
            
            return result
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'图表生成失败: {str(e)}'
            }
    
    def get_smart_recommendations(self) -> Dict[str, Any]:
        """获取智能推荐"""
        if not self.current_file:
            return {
                'status': 'error',
                'message': '请先上传数据文件'
            }
        
        try:
            # 获取数据信息
            file_info = self.analyzer.file_info
            stats = self.analyzer.get_summary_statistics()
            
            recommendations = {
                'charts': self._recommend_charts(file_info, stats),
                'analysis': self._recommend_analysis(file_info, stats),
                'insights': self._generate_insights(file_info, stats)
            }
            
            return {
                'status': 'success',
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'推荐生成失败: {str(e)}'
            }
    
    def _generate_recommendations(self, file_info: Dict, stats: Dict) -> List[str]:
        """生成分析建议"""
        recommendations = []
        
        # 基于数据特征生成建议
        if file_info.get('shape', {}).get('rows', 0) > 1000:
            recommendations.append("数据量较大，建议先进行数据概览分析")
        
        if stats.get('numeric_statistics'):
            recommendations.append("检测到数值型数据，可以进行统计分析和趋势图表")
        
        if stats.get('text_statistics'):
            recommendations.append("检测到分类数据，可以进行分布分析和饼图展示")
        
        # 检查缺失值
        missing_data = stats.get('missing_values', {})
        high_missing_cols = [
            col for col, info in missing_data.items() 
            if info.get('percentage', 0) > 10
        ]
        if high_missing_cols:
            recommendations.append(f"发现高缺失率字段: {', '.join(high_missing_cols[:3])}")
        
        return recommendations
    
    def _recommend_charts(self, file_info: Dict, stats: Dict) -> List[Dict]:
        """推荐图表类型"""
        charts = []
        columns = file_info.get('columns', [])
        
        numeric_cols = list(stats.get('numeric_statistics', {}).keys())
        text_cols = list(stats.get('text_statistics', {}).keys())
        
        # 推荐柱状图
        if text_cols and numeric_cols:
            charts.append({
                'type': 'bar',
                'title': f'{numeric_cols[0]} by {text_cols[0]}',
                'x_col': text_cols[0],
                'y_col': numeric_cols[0],
                'description': '分类数据的数值比较'
            })
        
        # 推荐饼图
        if text_cols:
            charts.append({
                'type': 'pie',
                'title': f'{text_cols[0]} Distribution',
                'x_col': text_cols[0],
                'description': '分类数据的分布情况'
            })
        
        # 推荐折线图
        if len(numeric_cols) >= 2:
            charts.append({
                'type': 'line',
                'title': f'{numeric_cols[1]} Trend',
                'x_col': numeric_cols[0],
                'y_col': numeric_cols[1],
                'description': '数值趋势变化'
            })
        
        return charts[:5]  # 最多推荐5个图表
    
    def _recommend_analysis(self, file_info: Dict, stats: Dict) -> List[str]:
        """推荐分析查询"""
        analyses = [
            "数据有多少行多少列？",
            "显示所有列名",
            "显示前几行数据",
            "显示统计信息"
        ]
        
        # 基于数据特征添加特定分析
        numeric_cols = list(stats.get('numeric_statistics', {}).keys())
        if numeric_cols:
            analyses.append(f"分析 {numeric_cols[0]} 列的分布情况")
        
        return analyses
    
    def _generate_insights(self, file_info: Dict, stats: Dict) -> List[str]:
        """生成数据洞察"""
        insights = []
        
        # 数据规模洞察
        rows = file_info.get('shape', {}).get('rows', 0)
        cols = file_info.get('shape', {}).get('columns', 0)
        insights.append(f"数据集包含 {rows:,} 行记录和 {cols} 个字段")
        
        # 数据质量洞察
        missing_stats = stats.get('missing_values', {})
        total_missing = sum(info.get('count', 0) for info in missing_stats.values())
        if total_missing > 0:
            insights.append(f"数据集存在 {total_missing:,} 个缺失值")
        
        # 数值特征洞察
        numeric_stats = stats.get('numeric_statistics', {})
        if numeric_stats:
            numeric_count = len(numeric_stats)
            insights.append(f"包含 {numeric_count} 个数值型字段，可进行统计分析")
        
        return insights
    
    def _generate_analysis_suggestions(self, query_result: Dict) -> List[str]:
        """基于查询结果生成建议"""
        suggestions = []
        
        if query_result.get('type') == 'table':
            suggestions.append("可以基于这些数据生成图表")
            suggestions.append("尝试进一步的统计分析")
        
        elif query_result.get('type') == 'info':
            suggestions.append("可以查看具体的数据内容")
            suggestions.append("尝试不同的查询方式")
        
        return suggestions
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_analysis_history(self) -> List[Dict]:
        """获取分析历史"""
        return self.analysis_history
    
    def clear_history(self):
        """清空分析历史"""
        self.analysis_history = []
        self.current_file = None

# 使用示例
if __name__ == "__main__":
    coordinator = DataInsightCoordinator()
    print("数据洞察协调器初始化完成")
    print("支持的功能:")
    print("1. process_file_upload(file_path) - 处理文件上传")
    print("2. analyze_data(query) - 分析数据")
    print("3. generate_chart(x_col, y_col, chart_type) - 生成图表")
    print("4. get_smart_recommendations() - 获取智能推荐")