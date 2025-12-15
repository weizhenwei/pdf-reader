# 配置说明

## 配置文件：config.json

这个文件包含了LLM API的配置信息。

### OpenAI配置示例

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "sk-your-openai-api-key-here",
    "model": "gpt-3.5-turbo",
    "base_url": null
  },
  "pdf": {
    "default_file": "New Client Risk Review.pdf"
  },
  "settings": {
    "max_tokens": 8192,
    "temperature": 0.7
  }
}
```

### Anthropic (Claude) 配置示例

```json
{
  "llm": {
    "provider": "anthropic",
    "api_key": "sk-ant-your-anthropic-api-key-here",
    "model": "claude-3-sonnet-20240229"
  },
  "pdf": {
    "default_file": "New Client Risk Review.pdf"
  },
  "settings": {
    "max_tokens": 4096,
    "temperature": 0.7
  }
}
```

### 使用国内API（如DeepSeek、智谱等）

很多国内的LLM服务提供OpenAI兼容的API，可以这样配置：

```json
{
  "llm": {
    "provider": "openai",
    "api_key": "your-api-key",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1"
  },
  "pdf": {
    "default_file": "New Client Risk Review.pdf"
  },
  "settings": {
    "max_tokens": 4096,
    "temperature": 0.7
  }
}
```

## 环境变量方式

你也可以使用环境变量来配置API密钥，这样更安全：

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

### Windows (CMD)
```cmd
set OPENAI_API_KEY=your-api-key
```

### Linux/Mac
```bash
export OPENAI_API_KEY="your-api-key"
```

然后在config.json中不需要填写api_key字段：

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-3.5-turbo"
  }
}
```

## 参数说明

### provider
- `openai` - 使用OpenAI或兼容OpenAI的API
- `anthropic` - 使用Anthropic Claude

### model
常用模型：
- OpenAI: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- Anthropic: `claude-3-sonnet-20240229`, `claude-3-opus-20240229`
- DeepSeek: `deepseek-chat`
- 智谱: `glm-4`

### base_url
自定义API端点，用于：
- 使用代理服务
- 使用国内API服务
- 使用本地部署的模型

### max_tokens
最大生成token数，默认4096

### temperature
温度参数（0-1），控制输出的随机性：
- 0.0 - 更确定性，适合事实性问答
- 0.7 - 平衡（默认）
- 1.0 - 更有创造性
