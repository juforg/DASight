# 数据洞察助手项目修改计划

## 项目概述
将当前的AI对话机器人demo改造为专业的数据洞察助手，基于NVIDIA NeMo Agent Toolkit构建，专门用于CSV/Excel文件的智能分析和可视化。

## 核心改造目标
从通用对话机器人转换为专业数据分析工具，提供文件上传、自动数据探索、对话式查询、智能可视化等功能。

## 修改计划阶段

### 第一阶段：基础架构调整
#### 1.1 项目配置更新
- [x] 更新项目名称和描述
- [x] 修改配置文件，调整工具链配置
- [x] 更新依赖包，添加数据处理相关库

#### 1.2 MCP服务集成准备
- [ ] 添加 @reading-plus-ai/mcp-server-data-exploration 服务配置
- [ ] 添加 @hustcc/mcp-echarts 服务配置
- [ ] 配置MCP服务器连接和认证

#### 1.3 前端界面基础调整 (对应优先级1-1)
- [x] 修改页面标题为"数据洞察助手"
- [x] 添加"文件上传"按钮到主界面
- [x] 修改欢迎消息突出数据分析功能
- [x] 调整页面配色体现数据分析主题

### 第二阶段：文件处理功能
#### 2.1 文件上传组件 (对应优先级1-2、2-1)
- [ ] 创建文件上传接口和组件，支持CSV/Excel格式
- [ ] 添加文件格式验证和大小限制
- [ ] 添加上传状态显示
- [ ] 上传成功后自动触发数据预览

#### 2.2 数据解析服务
- [ ] 集成数据解析库 (pandas, openpyxl等)
- [ ] 实现文件编码自动检测
- [ ] 添加数据类型识别和验证

#### 2.3 数据预览界面
- [ ] 创建数据表格预览组件
- [ ] 显示数据摘要信息 (行数、列数、字段类型)
- [ ] 提供数据校正选项

### 第三阶段：数据探索功能
#### 3.1 自动数据分析
- [ ] 集成 @reading-plus-ai/mcp-server-data-exploration
- [ ] 实现基础统计量计算
- [ ] 添加异常值检测功能
- [ ] 实现字段相关性分析

#### 3.2 智能洞察生成
- [ ] 基于分析结果生成自动洞察报告
- [ ] 实现数据模式识别
- [ ] 添加趋势分析功能

#### 3.3 对话式查询 (对应优先级1-3、2-2)
- [ ] 新增data_analysis工具到配置文件
- [ ] 扩展现有对话功能，专注数据查询
- [ ] 实现自然语言到SQL/数据操作的转换
- [ ] 实现"数据有多少行/列"查询
- [ ] 实现"显示字段列表"功能
- [ ] 实现基础统计查询(均值、最大值、最小值)
- [ ] 实现"某列的分布情况"查询
- [ ] 添加上下文相关的数据问答
- [ ] 添加数据状态管理，记录当前加载的数据
- [ ] 优化回答格式，使用表格显示统计结果
- [ ] 添加常用查询示例提示
- [ ] 错误处理和友好提示

### 第四阶段：可视化功能
#### 4.1 ECharts集成 (对应优先级1-4)
- [ ] 集成 @hustcc/mcp-echarts 服务
- [ ] 安装matplotlib或plotly库
- [ ] 实现基础图表类型 (柱状图、折线图、饼图等)
- [ ] 图表通过聊天界面展示(base64编码)

#### 4.2 智能图表推荐 (对应优先级2-3)
- [ ] 基于数据类型推荐合适图表
- [ ] 支持"给我画个XX图"的自然语言指令
- [ ] 图表添加标题和轴标签
- [ ] 实现图表自动配置
- [ ] 支持不同字段的图表生成
- [ ] 添加多图表组合功能

#### 4.3 高级可视化
- [ ] 实现散点图、热力图等高级图表
- [ ] 添加图表自定义配置界面
- [ ] 添加图表交互功能
- [ ] 支持图表导出功能

### 第五阶段：高级功能 (对应优先级3-1)
#### 5.1 数据处理工具
- [ ] 添加数据清洗功能
- [ ] 实现数据转换和计算
- [ ] 支持数据筛选和分组
- [ ] 数据清洗建议

#### 5.2 分析历史管理
- [ ] 实现分析项目保存
- [ ] 添加历史记录管理
- [ ] 支持分析结果导出

#### 5.3 扩展分析功能
- [ ] 集成机器学习模型
- [ ] 添加预测分析功能
- [ ] 支持多数据源对比
- [ ] 相关性分析功能
- [ ] 趋势分析

### 第六阶段：优化和完善 (对应优先级3-2、3-3)
#### 6.1 性能优化
- [ ] 优化大文件处理性能
- [ ] 实现数据分页和懒加载
- [ ] 添加处理进度显示
- [ ] 大文件分块处理
- [ ] 图表渲染优化
- [ ] 缓存机制

#### 6.2 用户体验优化
- [ ] 完善错误处理和提示
- [ ] 添加操作引导和帮助
- [ ] 优化响应式设计
- [ ] 图表样式优化
- [ ] 动画效果添加

#### 6.3 演示准备 (对应优先级2-4)
- [ ] 准备3个不同类型的演示CSV文件
- [ ] 设计演示脚本和对话流程
- [ ] 测试完整演示流程
- [ ] 拍摄关键功能截图
- [ ] 录制完整功能演示视频 (3-5分钟)

## 技术栈调整

### 新增依赖
```yaml
# Python 后端
pandas: 数据处理
openpyxl: Excel文件处理
numpy: 数值计算
scikit-learn: 机器学习 (可选)

# MCP 服务
@reading-plus-ai/mcp-server-data-exploration: 数据探索
@hustcc/mcp-echarts: 数据可视化

# 前端 (如需要)
react-dropzone: 文件上传
antd-table: 数据表格显示
```

### 配置文件调整
```yaml
# configs/data_insight_config.yml
tools:
  - data_exploration
  - echarts_visualization
  - file_upload
  - data_analysis

mcp_servers:
  data_exploration:
    command: "npx"
    args: ["@reading-plus-ai/mcp-server-data-exploration"]
  
  echarts:
    command: "npx" 
    args: ["@hustcc/mcp-echarts"]
```

## 目录结构调整

```
DASight/
├── NeMo-Agent-Toolkit/         # 核心框架 (保持)
├── external/                   # 外部模块
│   └── data-insight-ui/        # 重命名和定制UI
├── src/
│   ├── aiq/                    # 原AIQ核心
│   └── data-insight/           # 新增数据洞察模块
│       ├── file_handler/       # 文件处理
│       ├── data_analyzer/      # 数据分析
│       ├── visualization/      # 可视化
│       └── chat_interface/     # 对话接口
├── configs/
│   └── data_insight_config.yml # 新配置文件
├── data/                       # 新增数据存储目录
│   ├── uploads/                # 上传文件
│   ├── processed/              # 处理后数据
│   └── exports/                # 导出结果
└── docs/                       # 更新文档
    ├── user_guide.md          # 用户指南
    ├── api_reference.md       # API参考
    └── development.md         # 开发指南
```

## 成功指标

### 功能指标
- [ ] 支持主流CSV/Excel格式文件上传
- [ ] 实现基础数据统计和分析
- [ ] 提供至少5种常用图表类型
- [ ] 支持自然语言数据查询

### 性能指标
- [ ] 支持100MB以内文件快速处理
- [ ] 图表渲染时间 < 3秒
- [ ] 对话响应时间 < 2秒

### 用户体验指标
- [ ] 界面直观易用，无需培训即可上手
- [ ] 错误提示清晰明确
- [ ] 支持完整的分析工作流

## 🔧 推荐MCP服务和工具分析

### 核心数据处理服务

#### 1. @antv/mcp-server-chart (重点推荐)
**功能**: 基于AntV的强大图表生成服务
- 支持25+种图表类型（柱状图、折线图、饼图、散点图、热力图、雷达图、思维导图、网络图等）
- TypeScript实现，性能优秀
- 与现有计划中的@hustcc/mcp-echarts形成互补
- 安装：`npm install -g @antv/mcp-server-chart`

#### 2. @yzfly/mcp-excel-server (重点推荐)
**功能**: 专业Excel文件处理服务
- 支持Excel文件的创建、读取、修改
- 无需Microsoft Excel环境
- 自然语言交互Excel操作
- 数据分析和可视化能力

#### 3. marlonluo2018/pandas-mcp-server (核心推荐)
**功能**: 基于pandas的综合数据分析服务
- 标准化的pandas代码执行工作流
- CSV文件处理和数据操作
- 统计分析和数据转换
- 交互式图表生成
- 与现有@reading-plus-ai/mcp-server-data-exploration互补

#### 4. falahgs/mcp-csv-analysis-with-gemini-ai
**功能**: 基于Gemini AI的CSV高级分析
- 高级CSV分析能力
- AI驱动的数据洞察生成
- 思维生成和分析报告

### 辅助工具服务

#### 5. ChatExcel MCP Server
**功能**: Excel数据的对话式分析
- 智能Excel数据处理
- 可视化和分析一体化
- 适合复杂Excel文件处理

#### 6. Vibe Data Analysis MCP Server
**功能**: 数据预处理和分析
- CSV数据预处理工具
- 统计分析功能
- 图表生成能力

## 🚀 具体实现思路

### 阶段1: 核心MCP服务集成 (第1天)

#### 1.1 优先级调整的MCP服务配置
```yaml
# configs/hackathon_config.yml 更新
mcp_servers:
  # 核心数据处理
  pandas_server:
    command: "python"
    args: ["-m", "pandas_mcp_server"]
    
  # 强化图表生成 (替代原echarts方案)
  antv_charts:
    command: "npx"
    args: ["@antv/mcp-server-chart"]
    
  # Excel专业处理
  excel_handler:
    command: "npx"
    args: ["@yzfly/mcp-excel-server"]
    
  # 保留原有数据探索
  data_exploration:
    command: "npx"
    args: ["@reading-plus-ai/mcp-server-data-exploration"]
```

#### 1.2 快速部署策略
```bash
# 一键安装所有MCP服务
npm install -g @antv/mcp-server-chart
npm install -g @yzfly/mcp-excel-server
pip install pandas-mcp-server
npm install -g @reading-plus-ai/mcp-server-data-exploration
```

### 阶段2: 前端界面快速改造 (第1-2天)

#### 2.1 文件上传组件优化
- 支持拖拽上传CSV/Excel文件
- 实时文件预览（前10行数据）
- 上传进度和状态显示
- 自动触发pandas-mcp-server的数据加载

#### 2.2 对话增强策略
```typescript
// 预设数据分析相关的快捷问题
const DATA_ANALYSIS_PROMPTS = [
  "数据有多少行多少列？",
  "显示所有字段的基本统计信息",
  "帮我画个销售额的柱状图",
  "分析数据中的异常值",
  "显示字段之间的相关性"
];
```

### 阶段3: 核心分析流程实现 (第2-3天)

#### 3.1 智能分析工作流
```python
# 基于pandas-mcp-server的分析流程
1. 文件上传 → pandas.read_csv()/read_excel()
2. 数据探索 → df.info(), df.describe(), df.head()
3. 用户查询 → 自然语言转pandas代码
4. 图表生成 → 调用@antv/mcp-server-chart
5. 结果展示 → 表格 + 图表 + 文字洞察
```

#### 3.2 图表类型智能推荐
```javascript
// 基于数据类型自动推荐图表
const CHART_RECOMMENDATIONS = {
  numerical_single: ["histogram", "box_plot"],
  numerical_double: ["scatter_plot", "line_chart"],
  categorical: ["bar_chart", "pie_chart"],
  time_series: ["line_chart", "area_chart"],
  correlation: ["heatmap", "scatter_matrix"]
};
```

### 阶段4: 演示准备优化 (第3-4天)

#### 4.1 演示数据准备
```csv
# sales_data.csv (销售演示数据)
product,sales_amount,region,month
产品A,15000,北京,2024-01
产品B,22000,上海,2024-01
...

# user_behavior.csv (用户行为数据)
user_id,age,active_hours,region
001,25,3.5,北京
002,32,5.2,上海
...
```

#### 4.2 关键功能测试脚本
```bash
#!/bin/bash
# 自动化测试脚本
echo "测试文件上传功能..."
curl -X POST -F "file=@sales_data.csv" http://localhost:8001/upload

echo "测试数据分析对话..."
curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"数据有多少行多少列？"}' \
  http://localhost:8001/chat
```

## 🎯 优化建议

### 技术选型优化
1. **替换echarts方案**: 使用`@antv/mcp-server-chart`替代原`@hustcc/mcp-echarts`，功能更强大
2. **增强Excel支持**: 添加`@yzfly/mcp-excel-server`专门处理Excel文件
3. **强化数据处理**: 集成`pandas-mcp-server`作为核心数据处理引擎

### 开发效率提升
1. **MCP服务并行开发**: 同时配置多个MCP服务，避免单点依赖
2. **模块化设计**: 文件处理、数据分析、图表生成独立模块
3. **快速验证**: 每个功能模块完成后立即测试验证

## 📊 关键演示场景

### 场景1: 销售数据分析 (2分钟)
1. 上传sales_data.csv文件
2. 询问"数据有多少行多少列？"
3. 询问"各产品的销售额是多少？"
4. 要求"画个销售额柱状图"

### 场景2: 用户行为分析 (2分钟)
1. 上传user_behavior.csv文件
2. 询问"用户年龄分布情况"
3. 要求"显示年龄分布饼图"
4. 询问"平均活跃时长是多少？"

### 场景3: 综合分析展示 (1分钟)
1. 快速展示折线图功能
2. 展示数据统计结果表格
3. 演示自然语言交互效果

## 🎬 交付清单

### 必须交付 (P1)
- [ ] 可运行的数据洞察助手demo
- [ ] 文件上传功能截图
- [ ] 数据分析对话截图
- [ ] 3种图表生成截图
- [ ] 完整功能演示视频 (3-5分钟)
