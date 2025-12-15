"""
PDF问答系统
整合PDF内容提取和LLM问答功能
"""

import os
import json
import argparse
from typing import Optional, Dict, Any
from pdf_extractor import PDFExtractor
from llm_client import LLMClientFactory, LLMClient


class PDFQASystem:
    """PDF问答系统"""
    
    def __init__(self, llm_client: LLMClient, pdf_path: Optional[str] = None):
        """
        初始化PDF问答系统
        
        Args:
            llm_client: LLM客户端
            pdf_path: PDF文件路径（可选，可以后续加载）
        """
        self.llm_client = llm_client
        self.pdf_path = pdf_path
        self.pdf_content = None
        self.extractor = None
        
        if pdf_path:
            self.load_pdf(pdf_path)
    
    def load_pdf(self, pdf_path: str):
        """
        加载PDF文件
        
        Args:
            pdf_path: PDF文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        self.pdf_path = pdf_path
        self.extractor = PDFExtractor(pdf_path)
        self.pdf_content = self.extractor.get_formatted_content()
        
        print(f"✓ 已加载PDF文件: {pdf_path}")
        print(f"✓ 文档共 {len(self.extractor.reader.pages)} 页")
        print(f"✓ 提取内容长度: {len(self.pdf_content)} 字符\n")
    
    def ask(self, question: str, include_context: bool = True, **kwargs) -> str:
        """
        向LLM提问关于PDF的问题
        
        Args:
            question: 用户问题
            include_context: 是否包含PDF内容作为上下文
            **kwargs: 传递给LLM的其他参数
            
        Returns:
            LLM的回答
        """
        if not self.pdf_content and include_context:
            raise ValueError("请先加载PDF文件")
        
        context = self.pdf_content if include_context else None
        
        print(f"问题: {question}")
        print("正在思考...\n")
        
        answer = self.llm_client.ask(question, context=context, **kwargs)
        
        print(f"回答: {answer}\n")
        return answer
    
    def interactive_mode(self):
        """交互式问答模式"""
        if not self.pdf_content:
            raise ValueError("请先加载PDF文件")
        
        print("=" * 60)
        print("PDF问答系统 - 交互模式")
        print("=" * 60)
        print("输入问题开始对话，输入 'quit' 或 'exit' 退出")
        print("输入 'reload' 重新加载PDF文件")
        print("输入 'info' 查看PDF信息")
        print("-" * 60)
        
        while True:
            try:
                question = input("\n您的问题: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("再见！")
                    break
                
                if question.lower() == 'reload':
                    if self.pdf_path:
                        self.load_pdf(self.pdf_path)
                    else:
                        print("错误: 没有PDF文件路径")
                    continue
                
                if question.lower() == 'info':
                    self.show_pdf_info()
                    continue
                
                answer = self.ask(question)
                
            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"错误: {e}")
    
    def show_pdf_info(self):
        """显示PDF信息"""
        if not self.extractor:
            print("未加载PDF文件")
            return
        
        print("\n" + "=" * 60)
        print("PDF文档信息")
        print("=" * 60)
        
        metadata = self.extractor._extract_metadata()
        if metadata:
            for key, value in metadata.items():
                if value:
                    print(f"{key}: {value}")
        
        print(f"\n总页数: {len(self.extractor.reader.pages)}")
        
        fields = self.extractor.extract_form_fields()
        if fields:
            print(f"表单字段数: {len(fields)}")
        
        print(f"内容长度: {len(self.pdf_content)} 字符")
        print("=" * 60)
    
    def batch_ask(self, questions: list) -> Dict[str, str]:
        """
        批量提问
        
        Args:
            questions: 问题列表
            
        Returns:
            问题和答案的字典
        """
        results = {}
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] ", end="")
            answer = self.ask(question)
            results[question] = answer
        return results


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="PDF问答系统")
    parser.add_argument("pdf_file", nargs="?", help="PDF文件路径")
    parser.add_argument("-q", "--question", help="要提问的问题")
    parser.add_argument("-c", "--config", default="config.json", help="配置文件路径")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    parser.add_argument("--info", action="store_true", help="显示PDF信息")
    
    args = parser.parse_args()
    
    # 加载配置
    try:
        llm_client = LLMClientFactory.create_from_file(args.config)
    except FileNotFoundError:
        print(f"错误: 找不到配置文件 {args.config}")
        print("请创建配置文件或使用 --config 指定配置文件路径")
        return
    except Exception as e:
        print(f"错误: 加载配置失败 - {e}")
        return
    
    # 创建问答系统
    qa_system = PDFQASystem(llm_client)
    
    # 加载PDF
    if args.pdf_file:
        try:
            qa_system.load_pdf(args.pdf_file)
        except Exception as e:
            print(f"错误: {e}")
            return
    
    # 执行操作
    if args.info:
        qa_system.show_pdf_info()
    elif args.question:
        if not qa_system.pdf_content:
            print("错误: 请指定PDF文件")
            return
        qa_system.ask(args.question)
    elif args.interactive:
        if not qa_system.pdf_content:
            print("错误: 请指定PDF文件")
            return
        qa_system.interactive_mode()
    else:
        # 默认进入交互模式
        if qa_system.pdf_content:
            qa_system.interactive_mode()
        else:
            print("使用方法:")
            print(f"  python {os.path.basename(__file__)} <pdf_file> [选项]")
            print("\n选项:")
            print("  -q, --question TEXT    提问问题")
            print("  -i, --interactive      交互模式")
            print("  --info                 显示PDF信息")
            print("  -c, --config FILE      配置文件路径 (默认: config.json)")
            print("\n示例:")
            print(f"  python {os.path.basename(__file__)} document.pdf -i")
            print(f"  python {os.path.basename(__file__)} document.pdf -q '这个文档的主要内容是什么？'")


if __name__ == "__main__":
    main()
