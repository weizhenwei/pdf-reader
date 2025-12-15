# 快速开始指南

## 5分钟快速上手

### 第1步：安装依赖

```bash
pip install pypdf openai
```

### 第2步：配置API密钥

编辑 `config.json` 文件：

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "你的API密钥",
    "model": "gpt-3.5-turbo"
  }
}
```

**获取API密钥：**
- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com/
- 智谱AI: https://open.bigmodel.cn/

### 第3步：运行测试

测试PDF提取功能（不需要API密钥）：

```bash
python test_extraction.py
```

### 第4步：开始问答

```bash
python pdf_qa_system.py "New Client Risk Review.pdf" -i
```

进入交互模式后，输入你的问题即可！

## 常用命令

### 1. 交互式问答
```bash
python pdf_qa_system.py "your_document.pdf" -i
```

### 2. 单次提问
```bash
python pdf_qa_system.py "your_document.pdf" -q "这个文档讲了什么？"
```

### 3. 查看PDF信息
```bash
python pdf_qa_system.py "your_document.pdf" --info
```

### 4. 测试PDF提取
```bash
python test_extraction.py
```

### 5. 查看示例
```bash
python examples.py
```

## 在代码中使用

### 最简单的用法

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

### 批量提问

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

### 只提取PDF内容（不使用LLM）

```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor("document.pdf")

# 提取文本
text = extractor.extract_text()
print(text)

# 提取表单字段
fields = extractor.extract_form_fields()
print(fields)

# 获取格式化内容
formatted = extractor.get_formatted_content()
print(formatted)
```

## 常见问题

### Q: 我没有OpenAI API密钥怎么办？

A: 你可以使用国内的API服务，如：
- DeepSeek (https://platform.deepseek.com/)
- 智谱AI (https://open.bigmodel.cn/)
- 阿里云通义千问
- 百度文心一言

配置方法见 `CONFIG.md`

### Q: PDF提取的内容不完整怎么办？

A: 某些PDF格式可能比较复杂，可以尝试：
1. 使用其他工具转换PDF格式
2. 检查PDF是否加密
3. 查看 `pdf_content_test.json` 了解提取的详细内容

### Q: 如何控制成本？

A: 
1. 使用更便宜的模型（如gpt-3.5-turbo）
2. 减少上下文长度
3. 使用国内API（通常更便宜）
4. 只在必要时包含PDF内容

### Q: 支持哪些PDF格式？

A: 支持：
- ✅ 纯文本PDF
- ✅ 可填写表格PDF
- ✅ 混合内容PDF
- ❌ 扫描版PDF（需要OCR）
- ❌ 加密PDF

## 下一步

- 查看 `README.md` 了解完整功能
- 查看 `examples.py` 学习更多用法
- 查看 `CONFIG.md` 了解配置选项
- 修改代码以适应你的需求

## 需要帮助？

如果遇到问题，请检查：
1. Python版本（建议3.8+）
2. 依赖包是否正确安装
3. API密钥是否正确配置
4. PDF文件是否存在且可读
