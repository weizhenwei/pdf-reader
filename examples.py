"""
示例脚本：演示PDF问答系统的各种用法
"""

from pdf_qa_system import PDFQASystem
from llm_client import OpenAIClient, LLMClientFactory
import json


def example_1_basic_usage():
    """示例1：基本用法"""
    print("=" * 60)
    print("示例1：基本用法")
    print("=" * 60)
    
    # 方式1：从配置文件创建
    try:
        llm_client = LLMClientFactory.create_from_file("config.json")
        qa_system = PDFQASystem(llm_client, "New Client Risk Review.pdf")
        
        # 提问
        answer = qa_system.ask("这个PDF文档的主要内容是什么？")
        print(f"回答: {answer}")
        
    except FileNotFoundError as e:
        print(f"错误: {e}")
        print("请先配置 config.json 文件")


def example_2_direct_client():
    """示例2：直接创建客户端"""
    print("\n" + "=" * 60)
    print("示例2：直接创建OpenAI客户端")
    print("=" * 60)
    
    # 直接创建OpenAI客户端（需要API密钥）
    # api_key = "your-api-key-here"
    # llm_client = OpenAIClient(api_key=api_key, model="gpt-3.5-turbo")
    # qa_system = PDFQASystem(llm_client, "New Client Risk Review.pdf")
    # answer = qa_system.ask("文档中有哪些表单字段？")
    
    print("提示: 取消注释上面的代码并填入你的API密钥来运行此示例")


def example_3_batch_questions():
    """示例3：批量提问"""
    print("\n" + "=" * 60)
    print("示例3：批量提问")
    print("=" * 60)
    
    try:
        llm_client = LLMClientFactory.create_from_file("config.json")
        qa_system = PDFQASystem(llm_client, "New Client Risk Review.pdf")
        
        questions = [
            "这是什么类型的文档？",
            "文档中包含哪些关键信息？",
            "有哪些需要填写的字段？"
        ]
        
        results = qa_system.batch_ask(questions)
        
        print("\n批量提问结果：")
        for q, a in results.items():
            print(f"\nQ: {q}")
            print(f"A: {a}")
            print("-" * 60)
            
    except FileNotFoundError as e:
        print(f"错误: {e}")


def example_4_pdf_info():
    """示例4：查看PDF信息"""
    print("\n" + "=" * 60)
    print("示例4：查看PDF信息")
    print("=" * 60)
    
    from pdf_extractor import PDFExtractor
    
    try:
        extractor = PDFExtractor("New Client Risk Review.pdf")
        
        # 获取元数据
        metadata = extractor._extract_metadata()
        print("\n文档元数据：")
        for key, value in metadata.items():
            if value:
                print(f"  {key}: {value}")
        
        # 获取页数
        print(f"\n总页数: {len(extractor.reader.pages)}")
        
        # 获取表单字段
        fields = extractor.extract_form_fields()
        print(f"\n表单字段数量: {len(fields)}")
        if fields:
            print("\n表单字段列表：")
            for field_name, value in list(fields.items())[:5]:  # 只显示前5个
                print(f"  {field_name}: {value}")
            if len(fields) > 5:
                print(f"  ... 还有 {len(fields) - 5} 个字段")
        
        # 获取文本内容长度
        text = extractor.extract_text()
        print(f"\n文本内容长度: {len(text)} 字符")
        
    except FileNotFoundError:
        print("错误: 找不到PDF文件")


def example_5_custom_prompt():
    """示例5：自定义提示词"""
    print("\n" + "=" * 60)
    print("示例5：自定义提示词")
    print("=" * 60)
    
    try:
        from pdf_extractor import PDFExtractor
        
        llm_client = LLMClientFactory.create_from_file("config.json")
        extractor = PDFExtractor("New Client Risk Review.pdf")
        
        # 获取PDF内容
        pdf_content = extractor.get_formatted_content()
        
        # 自定义提示词
        custom_prompt = f"""
你是一个专业的文档分析专家。请仔细分析以下PDF文档内容，并提取关键信息。

文档内容：
{pdf_content}

请回答以下问题：
1. 这是什么类型的文档？
2. 文档的主要目的是什么？
3. 列出文档中的所有重要字段和它们的值
4. 是否有任何需要注意的风险或警告信息？

请用结构化的方式回答。
"""
        
        # 直接调用LLM
        messages = [{"role": "user", "content": custom_prompt}]
        answer = llm_client.chat(messages)
        
        print("分析结果：")
        print(answer)
        
    except FileNotFoundError as e:
        print(f"错误: {e}")


def example_6_save_results():
    """示例6：保存问答结果"""
    print("\n" + "=" * 60)
    print("示例6：保存问答结果到文件")
    print("=" * 60)
    
    try:
        llm_client = LLMClientFactory.create_from_file("config.json")
        qa_system = PDFQASystem(llm_client, "New Client Risk Review.pdf")
        
        questions = [
            "文档类型是什么？",
            "主要内容是什么？"
        ]
        
        results = qa_system.batch_ask(questions)
        
        # 保存为JSON
        output = {
            "pdf_file": "New Client Risk Review.pdf",
            "timestamp": "2024-01-01",
            "qa_results": results
        }
        
        with open("qa_results.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print("✓ 结果已保存到 qa_results.json")
        
    except FileNotFoundError as e:
        print(f"错误: {e}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("PDF问答系统 - 示例脚本")
    print("=" * 60)
    print("\n这个脚本演示了PDF问答系统的各种用法")
    print("\n注意：运行前请先配置 config.json 文件中的API密钥\n")
    
    # 运行不需要API的示例
    example_4_pdf_info()
    
    # 以下示例需要配置API密钥
    print("\n\n" + "=" * 60)
    print("以下示例需要配置API密钥才能运行")
    print("=" * 60)
    print("\n请编辑 config.json 文件，填入你的API密钥，然后取消下面的注释：")
    print("""
# example_1_basic_usage()
# example_2_direct_client()
# example_3_batch_questions()
# example_5_custom_prompt()
# example_6_save_results()
    """)


if __name__ == "__main__":
    main()
