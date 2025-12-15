"""
测试改进后的PDF提取功能
验证字段值的正确解释和格式化
"""

from pdf_extractor import PDFExtractor
import json


def test_improved_extraction():
    """测试改进后的提取功能"""
    print("=" * 70)
    print("测试改进后的PDF内容提取")
    print("=" * 70)
    
    pdf_path = "New Client Risk Review.pdf"
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        print(f"\n✓ 成功加载PDF: {pdf_path}")
        print(f"✓ 总页数: {len(extractor.reader.pages)}")
        
        # 测试1：原始字段提取
        print("\n" + "=" * 70)
        print("测试1：原始字段提取（未解释）")
        print("=" * 70)
        
        fields = extractor.extract_form_fields()
        print(f"\n共 {len(fields)} 个字段")
        
        # 显示一些关键字段的原始值
        key_fields = [
            "Company has drivers",
            "Employees handle hazardous materials",
            "RadioButton5",
            "Textfield0"
        ]
        
        print("\n关键字段的原始值：")
        for field_name in key_fields:
            if field_name in fields:
                print(f"  {field_name}: {fields[field_name]}")
        
        # 测试2：智能解释的字段
        print("\n" + "=" * 70)
        print("测试2：智能解释的字段值")
        print("=" * 70)
        
        structured_data = extractor.get_structured_data(interpret_boolean=True)
        
        print("\n解释后的关键字段：")
        for field_name in key_fields:
            if field_name in structured_data["fields"]:
                field_info = structured_data["fields"][field_name]
                print(f"\n  {field_name}:")
                print(f"    原始值: {field_info['raw_value']}")
                print(f"    解释值: {field_info['interpreted_value']}")
                print(f"    是否选中: {field_info['is_checked']}")
        
        # 测试3：格式化内容（用于LLM）
        print("\n" + "=" * 70)
        print("测试3：格式化内容（用于LLM）")
        print("=" * 70)
        
        formatted = extractor.get_formatted_content(interpret_boolean=True)
        print(f"\n格式化内容长度: {len(formatted)} 字符")
        print("\n格式化内容预览：")
        print("-" * 70)
        # 只显示表单字段部分
        if "【表单字段内容】" in formatted:
            parts = formatted.split("【表单字段内容】")
            if len(parts) > 1:
                field_section = parts[1].split("【")[0]
                print("【表单字段内容】" + field_section[:800])
        print("-" * 70)
        
        # 测试4：字段分组
        print("\n" + "=" * 70)
        print("测试4：字段分组（问题和详情关联）")
        print("=" * 70)
        
        field_groups = structured_data["field_groups"]
        print(f"\n共 {len(field_groups)} 个字段组")
        
        # 显示有详情的字段组
        print("\n有详细信息的字段：")
        count = 0
        for field_name, group_data in field_groups.items():
            if "detail" in group_data and group_data["detail"]:
                count += 1
                value = group_data.get("value", "N/A")
                detail = group_data.get("detail", "")
                print(f"\n  {count}. {field_name}")
                print(f"     值: {value}")
                print(f"     详情: {detail}")
                if count >= 5:  # 只显示前5个
                    break
        
        # 测试5：保存结构化数据
        print("\n" + "=" * 70)
        print("测试5：保存结构化数据")
        print("=" * 70)
        
        output_file = "pdf_structured_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 结构化数据已保存到: {output_file}")
        
        # 统计信息
        print("\n" + "=" * 70)
        print("统计信息")
        print("=" * 70)
        
        checked_count = sum(1 for f in structured_data["fields"].values() if f["is_checked"])
        unchecked_count = sum(1 for f in structured_data["fields"].values() if f["is_unchecked"])
        text_count = len(structured_data["fields"]) - checked_count - unchecked_count
        
        print(f"\n  选中的字段: {checked_count}")
        print(f"  未选中的字段: {unchecked_count}")
        print(f"  文本字段: {text_count}")
        print(f"  总字段数: {len(structured_data['fields'])}")
        
        print("\n" + "=" * 70)
        print("✓ 所有测试完成！")
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
    test_improved_extraction()
