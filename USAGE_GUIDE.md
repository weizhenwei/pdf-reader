# PDF问答系统 - 使用指南

## ✅ 已完成的功能

### 1. PDF内容提取 ✓
- 提取纯文本PDF的内容
- 提取可填写表格PDF的字段和值
- 提取PDF元数据（标题、作者、日期等）
- 按页提取内容
- 格式化输出用于LLM

### 2. LLM集成 ✓
- 支持OpenAI (GPT-3.5/GPT-4)
- 支持Anthropic (Claude)
- 支持自定义OpenAI兼容API（国内API）
- 统一的问答接口

### 3. 智能问答系统 ✓
- 基于PDF内容的上下文问答
- 交互式对话模式
- 批量问题处理
- 命令行工具

## 📦 项目文件说明

### 核心模块
- **pdf_extractor.py** - PDF内容提取器，支持文本和表单
- **llm_client.py** - LLM客户端，支持多种提供商
- **pdf_qa_system.py** - 主程序，整合提取和问答功能

### 配置和依赖
- **config.json** - 配置文件（需要填入API密钥）
- **requirements.txt** - Python依赖包列表

### 测试和示例
- **test_extraction.py** - 测试PDF提取功能
- **examples.py** - 各种使用示例
- **demo.py** - 完整工作流程演示

### 文档
- **README.md** - 完整的项目说明
- **QUICKSTART.md** - 5分钟快速上手指南
- **CONFIG.md** - 详细的配置说明
- **PROJECT_SUMMARY.md** - 项目总结
- **USAGE_GUIDE.md** - 本文件

## 🚀 快速开始（3步）

### 第1步：安装依赖
```bash
pip install pypdf openai
```

### 第2步：配置API密钥
编辑 `config.json`：
```json
{
  "llm": {
    "provider": "openai",
    "api_key": "你的API密钥",
    "model": "gpt-3.5-turbo"
  }
}
```

### 第3步：运行
```bash
# 测试PDF提取（不需要API密钥）
python test_extraction.py

# 运行完整演示
python demo.py

# 交互式问答
python pdf_qa_system.py "New Client Risk Review.pdf" -i
```

## 💻 使用方法

### 方法1：命令行工具

**交互模式（推荐）：**
```bash
python pdf_qa_system.py "document.pdf" -i
```

**单次提问：**
```bash
python pdf_qa_system.py "document.pdf" -q "这个文档讲了什么？"
```

**查看PDF信息：**
```bash
python pdf_qa_system.py "document.pdf" --info
```

### 方法2：在Python代码中使用

**基本用法：**
```python
from pdf_qa_system import PDFQASystem
from llm_client import LLMClientFactory

# 创建客户端
client = LLMClientFactory.create_from_file("config.json")

# 创建问答系统
qa = PDFQASystem(client, "document.pdf")

# 提问
answer = qa.ask("这个文档的主要内容是什么？")
print(answer)
```

**批量提问：**
```python
questions = [
    "文档的主题是什么？",
    "有哪些重要数据？",
    "结论是什么？"
]

results = qa.batch_ask(questions)
for q, a in results.items():
    print(f"Q: {q}\nA: {a}\n")
```

**只提取PDF内容（不使用LLM）：**
```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor("document.pdf")

# 提取文本
text = extractor.extract_text()

# 提取表单字段
fields = extractor.extract_form_fields()

# 获取格式化内容
formatted = extractor.get_formatted_content()
```

## 🔧 配置选项

### 支持的LLM提供商

**1. OpenAI**
```json
{
  "llm": {
    "provider": "openai",
    "api_key": "sk-...",
    "model": "gpt-3.5-turbo"
  }
}
```

**2. Anthropic Claude**
```json
{
  "llm": {
    "provider": "anthropic",
    "api_key": "sk-ant-...",
    "model": "claude-3-sonnet-20240229"
  }
}
```

**3. 国内API（DeepSeek、智谱等）**
```json
{
  "llm": {
    "provider": "openai",
    "api_key": "your-key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
  }
}
```

详细配置说明见 `CONFIG.md`

## 📝 实际应用示例

### 示例1：分析风险评估表单
```bash
python pdf_qa_system.py "New Client Risk Review.pdf" -i
```

```
您的问题: 这个表单的主要目的是什么？
回答: 这是一个新客户风险审查问卷，主要用于评估...

您的问题: 公司名称是什么？
回答: 根据表单，公司的法定名称是 Moxo...

您的问题: 有哪些风险因素被标记了？
回答: 根据表单，以下风险因素被标记：
1. 员工处理危险材料
2. 工作场所有职业病危害
...
```

### 示例2：批量分析多个问题
```python
from pdf_qa_system import PDFQASystem
from llm_client import LLMClientFactory

client = LLMClientFactory.create_from_file("config.json")
qa = PDFQASystem(client, "New Client Risk Review.pdf")

questions = [
    "这是什么类型的文档？",
    "文档中包含哪些主要部分？",
    "有哪些需要填写的关键字段？",
    "是否有任何风险警告？"
]

results = qa.batch_ask(questions)

# 保存结果
import json
with open("analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### 示例3：提取表单数据
```python
from pdf_extractor import PDFExtractor
import json

extractor = PDFExtractor("New Client Risk Review.pdf")

# 提取所有表单字段
fields = extractor.extract_form_fields()

# 筛选有值的字段
filled_fields = {k: v for k, v in fields.items() if v and v != "/Off"}

print(f"已填写的字段数: {len(filled_fields)}")
for name, value in filled_fields.items():
    print(f"{name}: {value}")

# 保存为JSON
with open("form_data.json", "w", encoding="utf-8") as f:
    json.dump(filled_fields, f, ensure_ascii=False, indent=2)
```

## 🎯 最佳实践

### 1. 成本控制
- 使用 `gpt-3.5-turbo` 而不是 `gpt-4`（更便宜）
- 考虑使用国内API（通常更便宜）
- 只在必要时包含完整PDF内容

### 2. 提高准确性
- 提供清晰、具体的问题
- 对于复杂问题，可以分步提问
- 使用更高级的模型（如gpt-4）

### 3. 处理大型PDF
- 对于超大PDF，考虑分页处理
- 使用RAG（检索增强生成）技术
- 提取关键部分而不是全部内容

### 4. 安全性
- 不要将API密钥提交到版本控制
- 使用环境变量存储敏感信息
- 注意PDF内容的隐私性

## ❓ 常见问题

### Q1: 如何获取API密钥？
**A:** 
- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com/
- 智谱AI: https://open.bigmodel.cn/

### Q2: 支持哪些PDF格式？
**A:**
- ✅ 纯文本PDF
- ✅ 可填写表格PDF
- ✅ 混合内容PDF
- ❌ 扫描版PDF（需要OCR）
- ❌ 加密PDF（需要先解密）

### Q3: PDF提取的内容不完整怎么办？
**A:**
1. 检查 `pdf_content_test.json` 查看实际提取的内容
2. 某些复杂格式的PDF可能提取效果不佳
3. 可以尝试使用其他工具转换PDF格式

### Q4: 如何使用国内API？
**A:** 在 `config.json` 中配置 `base_url`：
```json
{
  "llm": {
    "provider": "openai",
    "api_key": "your-key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
  }
}
```

### Q5: 如何控制成本？
**A:**
1. 使用更便宜的模型（gpt-3.5-turbo）
2. 使用国内API（通常更便宜）
3. 减少不必要的API调用
4. 缓存常见问题的答案

## 📚 进一步学习

### 推荐阅读
1. **README.md** - 完整的项目说明
2. **QUICKSTART.md** - 快速上手指南
3. **CONFIG.md** - 配置详解
4. **PROJECT_SUMMARY.md** - 项目总结

### 示例代码
- **test_extraction.py** - PDF提取测试
- **examples.py** - 各种使用示例
- **demo.py** - 完整工作流程

### 扩展阅读
- PyPDF文档: https://pypdf.readthedocs.io/
- OpenAI API文档: https://platform.openai.com/docs
- Anthropic API文档: https://docs.anthropic.com/

## 🆘 获取帮助

如果遇到问题：
1. 查看文档（README.md, QUICKSTART.md等）
2. 运行测试脚本（test_extraction.py, demo.py）
3. 检查配置文件（config.json）
4. 查看错误信息和日志

## 📞 联系方式

如有问题或建议，欢迎提交Issue！

---

**最后更新：** 2025-12-15
**版本：** 1.0.0
