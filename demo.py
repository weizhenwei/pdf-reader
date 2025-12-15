"""
完整演示脚本
展示PDF问答系统的完整工作流程
"""

import os
import json
from pdf_extractor import PDFExtractor
from llm_client import OpenAIClient, LLMClientFactory
from pdf_qa_system import PDFQASystem


def demo_step_1_extract_pdf():
    """步骤1：提取PDF内容"""
    print("\n" + "=" * 70)
    print("步骤1：提取PDF内容")
    print("=" * 70)
    
    pdf_path = "New Client Risk Review.pdf"
    extractor = PDFExtractor(pdf_path)
    
    print(f"\n✓ 加载PDF: {pdf_path}")
    print(f"✓ 总页数: {len(extractor.reader.pages)}")
    
    # 提取元数据
    metadata = extractor._extract_metadata()
    print("\n【文档元数据】")
    for key, value in metadata.items():
        if value:
            print(f"  {key}: {value}")
    
    # 提取表单字段
    fields = extractor.extract_form_fields()
    print(f"\n【表单字段】共 {len(fields)} 个")
    print("  示例字段：")
    for i, (name, value) in enumerate(list(fields.items())[:5], 1):
        print(f"  {i}. {name}: {value}")
    
    # 提取文本
    text = extractor.extract_text()
    print(f"\n【文本内容】长度: {len(text)} 字符")
    print("  前150字符预览：")
    print(f"  {text[:150]}...")
    
    return extractor


def demo_step_2_format_for_llm(extractor):
    """步骤2：格式化内容用于LLM"""
    print("\n" + "=" * 70)
    print("步骤2：格式化内容用于LLM")
    print("=" * 70)
    
    formatted_content = extractor.get_formatted_content()
    
    print(f"\n✓ 格式化内容长度: {len(formatted_content)} 字符")
    print("\n【格式化内容预览】")
    print(formatted_content[:500] + "...")
    
    return formatted_content


def demo_step_3_setup_llm():
    """步骤3：设置LLM客户端"""
    print("\n" + "=" * 70)
    print("步骤3：设置LLM客户端")
    print("=" * 70)
    
    config_path = "config.json"
    
    if not os.path.exists(config_path):
        print("\n✗ 配置文件不存在！")
        print("\n请创建 config.json 文件，内容如下：")
        print("""
{
  "llm": {
    "provider": "openai",
    "api_key": "your-api-key-here",
    "model": "gpt-3.5-turbo"
  }
}
        """)
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        api_key = config.get('llm', {}).get('api_key')
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            print("\n✗ 请在 config.json 中配置有效的API密钥")
            print("\n提示：你可以使用以下服务：")
            print("  - OpenAI: https://platform.openai.com/")
            print("  - DeepSeek: https://platform.deepseek.com/")
            print("  - 智谱AI: https://open.bigmodel.cn/")
            return None
        
        llm_client = LLMClientFactory.create_from_file(config_path)
        print(f"\n✓ LLM客户端创建成功")
        print(f"  提供商: {config['llm']['provider']}")
        print(f"  模型: {config['llm']['model']}")
        
        return llm_client
        
    except Exception as e:
        print(f"\n✗ 创建LLM客户端失败: {e}")
        return None


def demo_step_4_qa_system(llm_client, pdf_path):
    """步骤4：使用问答系统"""
    print("\n" + "=" * 70)
    print("步骤4：使用PDF问答系统")
    print("=" * 70)
    
    if not llm_client:
        print("\n✗ 跳过此步骤（需要配置LLM客户端）")
        return
    
    qa_system = PDFQASystem(llm_client, pdf_path)
    
    # 示例问题
    questions = [
        "这个PDF文档是什么类型的文档？",
        "文档中填写的公司名称是什么？",
        "文档中有哪些主要的信息类别？"
    ]
    
    print("\n【示例问答】")
    for i, question in enumerate(questions, 1):
        print(f"\n问题 {i}: {question}")
        try:
            answer = qa_system.ask(question)
            print(f"回答: {answer}")
        except Exception as e:
            print(f"错误: {e}")
            break


def demo_step_5_batch_processing(llm_client, pdf_path):
    """步骤5：批量处理"""
    print("\n" + "=" * 70)
    print("步骤5：批量问题处理")
    print("=" * 70)
    
    if not llm_client:
        print("\n✗ 跳过此步骤（需要配置LLM客户端）")
        return
    
    qa_system = PDFQASystem(llm_client, pdf_path)
    
    questions = [
        "文档的主要目的是什么？",
        "有哪些风险相关的问题？"
    ]
    
    print("\n【批量提问】")
    try:
        results = qa_system.batch_ask(questions)
        
        # 保存结果
        output_file = "demo_qa_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"\n✗ 批量处理失败: {e}")


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("PDF问答系统 - 完整演示")
    print("=" * 70)
    print("\n这个演示将展示完整的工作流程：")
    print("  1. 提取PDF内容")
    print("  2. 格式化内容用于LLM")
    print("  3. 设置LLM客户端")
    print("  4. 使用问答系统")
    print("  5. 批量问题处理")
    
    pdf_path = "New Client Risk Review.pdf"
    
    # 步骤1：提取PDF
    extractor = demo_step_1_extract_pdf()
    
    # 步骤2：格式化
    formatted_content = demo_step_2_format_for_llm(extractor)
    
    # 步骤3：设置LLM
    llm_client = demo_step_3_setup_llm()
    
    # 步骤4：问答系统
    demo_step_4_qa_system(llm_client, pdf_path)
    
    # 步骤5：批量处理
    demo_step_5_batch_processing(llm_client, pdf_path)
    
    # 总结
    print("\n" + "=" * 70)
    print("演示完成！")
    print("=" * 70)
    
    if llm_client:
        print("\n✓ 所有功能演示成功！")
        print("\n下一步：")
        print("  - 运行交互模式: python pdf_qa_system.py 'your.pdf' -i")
        print("  - 查看更多示例: python examples.py")
        print("  - 阅读文档: README.md, QUICKSTART.md")
    else:
        print("\n⚠ 部分功能需要配置API密钥")
        print("\n配置步骤：")
        print("  1. 编辑 config.json")
        print("  2. 填入你的API密钥")
        print("  3. 重新运行此演示")
        print("\n详细说明见: CONFIG.md")


if __name__ == "__main__":
    main()
