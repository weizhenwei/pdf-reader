# PDF问答系统

一个基于Python的PDF文档智能问答系统，支持提取PDF文本和表单内容，并通过LLM（大语言模型）回答用户关于PDF内容的问题。

## 功能特性

- ✅ **PDF内容提取**
  - 支持纯文本PDF
  - 支持可填写表格PDF
  - 提取文档元数据
  - 按页提取内容

- ✅ **LLM集成**
  - 支持OpenAI (GPT-3.5/GPT-4)
  - 支持Anthropic (Claude)
  - 支持自定义OpenAI兼容API

- ✅ **智能问答**
  - 基于PDF内容的上下文问答
  - 交互式对话模式
  - 批量问题处理

## 安装

### 1. 克隆或下载项目

```bash
cd d:\pdf-reader
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install pypdf openai anthropic
```

### 3. 配置API密钥

编辑 `config.json` 文件，填入你的API密钥：

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "YOUR_API_KEY_HERE",
    "model": "gpt-3.5-turbo"
  }
}
```

**支持的配置选项：**

- **OpenAI配置**
  ```json
  {
    "llm": {
      "provider": "openai",
      "api_key": "sk-...",
      "model": "gpt-3.5-turbo"
    }
  }
  ```

- **Anthropic配置**
  ```json
  {
    "llm": {
      "provider": "anthropic",
      "api_key": "sk-ant-...",
      "model": "claude-3-sonnet-20240229"
    }
  }
  ```

- **自定义OpenAI兼容API**
  ```json
  {
    "llm": {
      "provider": "openai",
      "api_key": "your-key",
      "model": "your-model",
      "base_url": "https://your-api-endpoint.com/v1"
    }
  }
  ```

## 使用方法

### 1. 交互式问答模式（推荐）

```bash
python pdf_qa_system.py "New Client Risk Review.pdf" -i
```

进入交互模式后，你可以：
- 输入问题进行对话
- 输入 `info` 查看PDF信息
- 输入 `reload` 重新加载PDF
- 输入 `quit` 或 `exit` 退出

### 2. 单次提问

```bash
python pdf_qa_system.py "document.pdf" -q "这个文档的主要内容是什么？"
```

### 3. 查看PDF信息

```bash
python pdf_qa_system.py "document.pdf" --info
```

### 4. 在代码中使用

```python
from pdf_qa_system import PDFQASystem
from llm_client import LLMClientFactory

# 创建LLM客户端
llm_client = LLMClientFactory.create_from_file("config.json")

# 创建问答系统
qa_system = PDFQASystem(llm_client, pdf_path="document.pdf")

# 提问
answer = qa_system.ask("这个文档讲了什么？")
print(answer)

# 批量提问
questions = [
    "文档的主题是什么？",
    "有哪些重要的数据？",
    "结论是什么？"
]
results = qa_system.batch_ask(questions)
```

## 项目结构

```
pdf-reader/
├── pdf_extractor.py      # PDF内容提取器
├── llm_client.py         # LLM客户端（支持多种提供商）
├── pdf_qa_system.py      # 主程序（问答系统）
├── config.json           # 配置文件
├── requirements.txt      # 依赖包列表
├── README.md            # 说明文档
└── New Client Risk Review.pdf  # 示例PDF文件
```

## 模块说明

### pdf_extractor.py

PDF内容提取器，提供以下功能：

- `extract_text()` - 提取所有文本内容
- `extract_form_fields()` - 提取表单字段
- `extract_pages_content()` - 按页提取内容
- `get_formatted_content()` - 获取格式化内容（用于LLM上下文）

### llm_client.py

LLM客户端，支持：

- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- 自定义OpenAI兼容API

### pdf_qa_system.py

主程序，整合PDF提取和LLM问答：

- 加载PDF文件
- 向LLM提问
- 交互式对话
- 批量问题处理

## 示例

### 示例1：分析表单PDF

```bash
python pdf_qa_system.py "New Client Risk Review.pdf" -i
```

```
您的问题: 这个表单中填写的公司名称是什么？
回答: 根据表单内容，公司的法定名称是...

您的问题: 有哪些风险因素被标记了？
回答: 根据表单，以下风险因素被标记：...
```

### 示例2：提取文档摘要

```bash
python pdf_qa_system.py "report.pdf" -q "请总结这份报告的主要内容"
```

### 示例3：批量分析

```python
from pdf_qa_system import PDFQASystem
from llm_client import OpenAIClient

client = OpenAIClient(api_key="your-key")
qa = PDFQASystem(client, "document.pdf")

questions = [
    "文档的作者是谁？",
    "发布日期是什么时候？",
    "主要结论是什么？"
]

results = qa.batch_ask(questions)
for q, a in results.items():
    print(f"Q: {q}\nA: {a}\n")
```

## 注意事项

1. **API密钥安全**：不要将包含真实API密钥的配置文件提交到版本控制系统
2. **内容长度限制**：非常大的PDF可能超过LLM的上下文长度限制
3. **成本控制**：使用付费API时注意控制调用次数和token使用量
4. **PDF格式**：某些复杂格式的PDF可能提取效果不佳

## 故障排除

### 问题1：找不到模块

```bash
pip install pypdf openai anthropic
```

### 问题2：API密钥错误

检查 `config.json` 中的API密钥是否正确

### 问题3：PDF提取失败

确保PDF文件没有加密，且格式正确

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
