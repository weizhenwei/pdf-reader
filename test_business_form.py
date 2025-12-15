"""
测试 Business_Information_Form.pdf 的内容提取
"""

from pdf_extractor import PDFExtractor
import json


def test_business_form():
    """测试 Business_Information_Form.pdf"""
    print("=" * 70)
    print("测试 Business_Information_Form.pdf")
    print("=" * 70)
    
    pdf_path = "Business_Information_Form.pdf"
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        print(f"\n✓ 成功加载PDF: {pdf_path}")
        print(f"✓ 总页数: {len(extractor.reader.pages)}")
        
        # 1. 查看所有原始字段
        print("\n" + "=" * 70)
        print("1. 所有原始字段")
        print("=" * 70)
        
        fields = extractor.extract_form_fields()
        print(f"\n共 {len(fields)} 个字段\n")
        
        for field_name, value in fields.items():
            if value and value != "" and value != "Off":
                print(f"  {field_name}: {value}")
        
        # 2. 查找与交通工具相关的字段
        print("\n" + "=" * 70)
        print("2. 查找与交通工具相关的字段")
        print("=" * 70)
        
        keywords = ["vehicle", "car", "aircraft", "plane", "watercraft", "boat", "driver", "transportation"]
        
        print("\n可能相关的字段：")
        for field_name, value in fields.items():
            field_lower = field_name.lower()
            if any(keyword in field_lower for keyword in keywords):
                print(f"  {field_name}: {value}")
        
        # 3. 查看格式化内容
        print("\n" + "=" * 70)
        print("3. 格式化内容（用于LLM）")
        print("=" * 70)
        
        formatted = extractor.get_formatted_content(interpret_boolean=True)
        print(f"\n{formatted}")
        
        # 4. 保存完整数据
        print("\n" + "=" * 70)
        print("4. 保存完整数据")
        print("=" * 70)
        
        all_content = extractor.extract_all_content()
        with open("business_form_content.json", "w", encoding="utf-8") as f:
            json.dump(all_content, f, ensure_ascii=False, indent=2)
        
        print("\n✓ 完整数据已保存到: business_form_content.json")
        
        # 5. 结构化数据
        structured = extractor.get_structured_data(interpret_boolean=True)
        with open("business_form_structured.json", "w", encoding="utf-8") as f:
            json.dump(structured, f, ensure_ascii=False, indent=2)
        
        print("✓ 结构化数据已保存到: business_form_structured.json")
        
        print("\n" + "=" * 70)
        print("✓ 测试完成！")
        print("=" * 70)
        
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
    test_business_form()
