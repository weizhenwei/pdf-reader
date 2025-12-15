"""
LLM客户端
支持多种LLM服务（OpenAI、Azure OpenAI、本地模型等）
"""

import os
import json
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """LLM客户端抽象基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            **kwargs: 其他参数
            
        Returns:
            LLM的回复
        """
        pass
    
    @abstractmethod
    def ask(self, question: str, context: Optional[str] = None, **kwargs) -> str:
        """
        简单问答接口
        
        Args:
            question: 用户问题
            context: 上下文信息
            **kwargs: 其他参数
            
        Returns:
            LLM的回复
        """
        pass


class OpenAIClient(LLMClient):
    """OpenAI客户端"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", base_url: Optional[str] = None):
        """
        初始化OpenAI客户端
        
        Args:
            api_key: API密钥
            model: 模型名称
            base_url: API基础URL（可选，用于兼容其他OpenAI格式的API）
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("请安装openai库: pip install openai")
        
        self.model = model
        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """发送聊天请求"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content
    
    def ask(self, question: str, context: Optional[str] = None, **kwargs) -> str:
        """简单问答接口"""
        messages = []
        
        if context:
            messages.append({
                "role": "system",
                "content": f"你是一个专业的PDF文档分析助手。请根据以下文档内容回答用户的问题。\n\n文档内容：\n{context}"
            })
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        return self.chat(messages, **kwargs)


class AnthropicClient(LLMClient):
    """Anthropic Claude客户端"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        """
        初始化Anthropic客户端
        
        Args:
            api_key: API密钥
            model: 模型名称
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("请安装anthropic库: pip install anthropic")
        
        self.model = model
        self.client = Anthropic(api_key=api_key)
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """发送聊天请求"""
        # Claude需要分离system消息
        system_message = None
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        
        params = {
            "model": self.model,
            "messages": user_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
        }
        
        if system_message:
            params["system"] = system_message
        
        response = self.client.messages.create(**params)
        return response.content[0].text
    
    def ask(self, question: str, context: Optional[str] = None, **kwargs) -> str:
        """简单问答接口"""
        messages = []
        
        if context:
            messages.append({
                "role": "system",
                "content": f"你是一个专业的PDF文档分析助手。请根据以下文档内容回答用户的问题。\n\n文档内容：\n{context}"
            })
        
        messages.append({
            "role": "user",
            "content": question
        })
        
        return self.chat(messages, **kwargs)


class LLMClientFactory:
    """LLM客户端工厂"""
    
    @staticmethod
    def create_from_config(config: Dict[str, Any]) -> LLMClient:
        """
        从配置创建LLM客户端
        
        Args:
            config: 配置字典
            
        Returns:
            LLM客户端实例
        """
        provider = config.get("provider", "openai").lower()
        
        if provider == "openai":
            return OpenAIClient(
                api_key=config.get("api_key") or os.getenv("OPENAI_API_KEY"),
                model=config.get("model", "gpt-3.5-turbo"),
                base_url=config.get("base_url")
            )
        elif provider == "anthropic":
            return AnthropicClient(
                api_key=config.get("api_key") or os.getenv("ANTHROPIC_API_KEY"),
                model=config.get("model", "claude-3-sonnet-20240229")
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
    
    @staticmethod
    def create_from_file(config_path: str) -> LLMClient:
        """
        从配置文件创建LLM客户端
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            LLM客户端实例
        """
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return LLMClientFactory.create_from_config(config.get("llm", {}))


if __name__ == "__main__":
    # 测试代码
    print("LLM客户端模块")
    print("支持的提供商: OpenAI, Anthropic")
    print("\n使用示例:")
    print("1. 从配置文件创建: client = LLMClientFactory.create_from_file('config.json')")
    print("2. 直接创建: client = OpenAIClient(api_key='your-key', model='gpt-3.5-turbo')")
    print("3. 问答: answer = client.ask('问题', context='上下文')")
