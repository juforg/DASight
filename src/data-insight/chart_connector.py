#!/usr/bin/env python3
"""
AntV 图表连接器 - 连接@antv/mcp-server-chart服务
"""

import json
import subprocess
import tempfile
import os
from typing import Dict, Any, Optional

class AntVChartConnector:
    """AntV MCP图表服务连接器"""
    
    def __init__(self):
        self.server_cmd = ["npx", "@antv/mcp-server-chart"]
        self.charts_dir = "charts"
        self._ensure_charts_dir()
    
    def _ensure_charts_dir(self):
        """确保图表目录存在"""
        if not os.path.exists(self.charts_dir):
            os.makedirs(self.charts_dir)
    
    def test_connection(self) -> Dict[str, Any]:
        """测试MCP服务连接"""
        try:
            result = subprocess.run(
                self.server_cmd + ["--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'AntV MCP服务连接正常',
                    'help_output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': 'AntV MCP服务连接失败',
                    'error': result.stderr
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'连接测试失败: {str(e)}'
            }
    
    def generate_chart_json(self, chart_data: Dict[str, Any], 
                           output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        生成图表配置JSON
        
        Args:
            chart_data: 图表数据配置
            output_file: 输出文件名（可选）
            
        Returns:
            Dict: 生成结果
        """
        try:
            if output_file is None:
                output_file = f"chart_{hash(str(chart_data)) % 10000}.json"
            
            output_path = os.path.join(self.charts_dir, output_file)
            
            # 转换为AntV G2格式
            antv_config = self._convert_to_antv_format(chart_data)
            
            # 保存配置文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(antv_config, f, indent=2, ensure_ascii=False)
            
            return {
                'status': 'success',
                'message': '图表配置生成成功',
                'config_file': output_path,
                'config': antv_config
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'图表配置生成失败: {str(e)}'
            }
    
    def _convert_to_antv_format(self, chart_data: Dict[str, Any]) -> Dict[str, Any]:
        """将通用图表数据转换为AntV G2格式"""
        
        chart_type = chart_data.get('type', 'bar')
        title = chart_data.get('title', '数据图表')
        data = chart_data.get('data', {})
        
        if chart_type == 'bar':
            # 柱状图配置
            labels = data.get('labels', [])
            values = data.get('datasets', [{}])[0].get('data', [])
            
            # 转换为AntV数据格式
            antv_data = [
                {'category': label, 'value': value}
                for label, value in zip(labels, values)
            ]
            
            return {
                'type': 'view',
                'data': antv_data,
                'encode': {
                    'x': 'category',
                    'y': 'value'
                },
                'coordinate': {'type': 'rect'},
                'geometry': {
                    'type': 'interval'
                },
                'style': {
                    'fill': '#1890ff'
                },
                'title': {
                    'text': title
                },
                'axis': {
                    'x': {'title': {'text': '类别'}},
                    'y': {'title': {'text': '数值'}}
                }
            }
        
        elif chart_type == 'line':
            # 折线图配置
            labels = data.get('labels', [])
            values = data.get('datasets', [{}])[0].get('data', [])
            
            antv_data = [
                {'x': label, 'y': value}
                for label, value in zip(labels, values)
            ]
            
            return {
                'type': 'view',
                'data': antv_data,
                'encode': {
                    'x': 'x',
                    'y': 'y'
                },
                'coordinate': {'type': 'rect'},
                'geometry': {
                    'type': 'line'
                },
                'style': {
                    'stroke': '#1890ff',
                    'lineWidth': 2
                },
                'title': {
                    'text': title
                }
            }
        
        elif chart_type == 'pie':
            # 饼图配置
            labels = data.get('labels', [])
            values = data.get('datasets', [{}])[0].get('data', [])
            
            antv_data = [
                {'category': label, 'value': value}
                for label, value in zip(labels, values)
            ]
            
            return {
                'type': 'view',
                'data': antv_data,
                'coordinate': {'type': 'theta'},
                'geometry': {
                    'type': 'interval',
                    'position': 'value',
                    'color': 'category'
                },
                'title': {
                    'text': title
                }
            }
        
        elif chart_type == 'scatter':
            # 散点图配置
            scatter_data = data.get('datasets', [{}])[0].get('data', [])
            
            antv_data = [
                {'x': point.get('x', 0), 'y': point.get('y', 0)}
                for point in scatter_data
            ]
            
            return {
                'type': 'view',
                'data': antv_data,
                'encode': {
                    'x': 'x',
                    'y': 'y'
                },
                'coordinate': {'type': 'rect'},
                'geometry': {
                    'type': 'point'
                },
                'style': {
                    'fill': '#1890ff',
                    'r': 4
                },
                'title': {
                    'text': title
                }
            }
        
        else:
            # 默认配置
            return {
                'type': 'view',
                'title': {
                    'text': f'不支持的图表类型: {chart_type}'
                }
            }
    
    def generate_chart_html(self, chart_config: Dict[str, Any], 
                           output_file: Optional[str] = None) -> Dict[str, Any]:
        """
        生成图表HTML文件
        
        Args:
            chart_config: 图表配置
            output_file: 输出文件名
            
        Returns:
            Dict: 生成结果
        """
        try:
            if output_file is None:
                output_file = f"chart_{hash(str(chart_config)) % 10000}.html"
            
            output_path = os.path.join(self.charts_dir, output_file)
            
            # 生成HTML模板
            html_content = self._generate_html_template(chart_config)
            
            # 保存HTML文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                'status': 'success',
                'message': '图表HTML生成成功',
                'html_file': output_path,
                'url': f'file://{os.path.abspath(output_path)}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'图表HTML生成失败: {str(e)}'
            }
    
    def _generate_html_template(self, chart_config: Dict[str, Any]) -> str:
        """生成HTML模板"""
        
        config_json = json.dumps(chart_config, ensure_ascii=False, indent=2)
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chart_config.get('title', {}).get('text', '数据图表')}</title>
    <script src="https://unpkg.com/@antv/g2@5"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 1200px;
            margin: 0 auto;
        }}
        #chart {{
            width: 100%;
            height: 400px;
        }}
        .title {{
            text-align: center;
            margin-bottom: 20px;
            color: #333;
            font-size: 18px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div class="title">{chart_config.get('title', {}).get('text', '数据图表')}</div>
        <div id="chart"></div>
    </div>

    <script>
        try {{
            const chartConfig = {config_json};
            const chart = new G2.Chart({{
                container: 'chart',
                autoFit: true,
                height: 400
            }});
            
            chart.data(chartConfig.data || []);
            
            if (chartConfig.encode) {{
                chart.encode('x', chartConfig.encode.x);
                chart.encode('y', chartConfig.encode.y);
            }}
            
            if (chartConfig.coordinate) {{
                chart.coordinate(chartConfig.coordinate);
            }}
            
            if (chartConfig.geometry) {{
                const mark = chart.interval();
                if (chartConfig.geometry.type === 'line') {{
                    mark = chart.line();
                }} else if (chartConfig.geometry.type === 'point') {{
                    mark = chart.point();
                }}
                
                if (chartConfig.style) {{
                    mark.style(chartConfig.style);
                }}
            }}
            
            chart.render();
            
        }} catch (error) {{
            console.error('图表渲染错误:', error);
            document.getElementById('chart').innerHTML = 
                '<div style="text-align: center; color: red; padding: 50px;">图表渲染失败: ' + error.message + '</div>';
        }}
    </script>
</body>
</html>
        """
        
        return html_template.strip()

# 使用示例
if __name__ == "__main__":
    connector = AntVChartConnector()
    
    # 测试连接
    print("测试AntV MCP服务连接...")
    result = connector.test_connection()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 测试图表生成
    sample_data = {
        'type': 'bar',
        'title': '销售数据',
        'data': {
            'labels': ['产品A', '产品B', '产品C', '产品D'],
            'datasets': [{
                'data': [120, 190, 300, 500]
            }]
        }
    }
    
    print("\\n生成示例图表...")
    config_result = connector.generate_chart_json(sample_data)
    print(json.dumps(config_result, indent=2, ensure_ascii=False))
    
    if config_result['status'] == 'success':
        html_result = connector.generate_chart_html(config_result['config'])
        print(json.dumps(html_result, indent=2, ensure_ascii=False))