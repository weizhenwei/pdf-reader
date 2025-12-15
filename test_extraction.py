"""
简单测试脚本：验证PDF提取功能
"""

from pdf_extractor import PDFExtractor
import json


def test_pdf_extraction():
    """测试PDF提取功能"""
    print("=" * 60)
    print("测试PDF内容提取")
    print("=" * 60)
    
    pdf_path = "New Client Risk Review.pdf"
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        # 1. 基本信息
        print(f"\n✓ 成功加载PDF: {pdf_path}")
        print(f"✓ 总页数: {len(extractor.reader.pages)}")
        
        # 2. 提取元数据
        print("\n【文档元数据】")
        metadata = extractor._extract_metadata()
        if metadata:
            for key, value in metadata.items():
                if value:
                    print(f"  {key}: {value}")
        else:
            print("  (无元数据)")
        
        # 3. 提取表单字段
        print("\n【表单字段】")
        fields = extractor.extract_form_fields()
        if fields:
            print(f"  共 {len(fields)} 个字段")
            print("\n  前10个字段：")
            for i, (field_name, value) in enumerate(list(fields.items())[:10], 1):
                print(f"  {i}. {field_name}: {value}")
            if len(fields) > 10:
                print(f"  ... 还有 {len(fields) - 10} 个字段")
        else:
            print("  (无表单字段)")
        
        # 4. 提取文本内容
        print("\n【文本内容】")
        text = extractor.extract_text()
        if text:
            print(f"  文本长度: {len(text)} 字符")
            print(f"\n  前200个字符预览：")
            print(f"  {text[:200]}...")
        else:
            print("  (无文本内容)")
        
        # 5. 获取格式化内容（用于LLM）
        print("\n【格式化内容（用于LLM）】")
        formatted = extractor.get_formatted_content()
        print(f"  格式化内容长度: {len(formatted)} 字符")
        
        # 6. 保存完整内容到JSON
        print("\n【保存到JSON】")
        all_content = extractor.extract_all_content()
        with open("pdf_content_test.json", "w", encoding="utf-8") as f:
            json.dump(all_content, f, ensure_ascii=False, indent=2)
        print("  ✓ 已保存到 pdf_content_test.json")
        
        print("\n" + "=" * 60)
        print("✓ PDF提取测试完成！")
        print("=" * 60)
        
        return True
        
    except FileNotFoundError:
        print(f"\n✗ 错误: 找不到文件 {pdf_path}")
        return False
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_pdf_extraction()
