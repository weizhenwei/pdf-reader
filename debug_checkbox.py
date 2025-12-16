"""
调试脚本：专门查看checkbox字段
"""
from pdf_extractor import PDFExtractor
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "New Client Risk Review.pdf"

extractor = PDFExtractor(pdf_path)

# 获取原始字段
fields = extractor.reader.get_fields()

print("=" * 80)
print("查找包含 'hazardous' 和 'leave of ab' 的字段")
print("=" * 80)

if fields:
    for field_name, field_data in fields.items():
        # 查找特定字段
        if "hazardous" in field_name.lower() or "leave of ab" in field_name.lower():
            print(f"\n>>> 字段名: {field_name}")
            print(f"    字段类型 (/FT): {field_data.get('/FT', 'N/A')}")
            print(f"    值 (/V): {field_data.get('/V', 'N/A')}")
            print(f"    默认值 (/DV): {field_data.get('/DV', 'N/A')}")
            print(f"    外观状态 (/AS): {field_data.get('/AS', 'N/A')}")
            print(f"    标志 (/Ff): {field_data.get('/Ff', 'N/A')}")
            
            # 检查是否有子字段
            if "/Kids" in field_data:
                print(f"    有子字段 (/Kids): {field_data['/Kids']}")
            
            # 检查所有可能的状态
            if "/_States_" in field_data:
                print(f"    可用状态: {field_data['/_States_']}")
            
            print(f"\n    完整字段数据:")
            for key, value in field_data.items():
                print(f"      {key}: {value}")
            print("-" * 80)

# 显示提取后的值
print("\n" + "=" * 80)
print("提取后的字段值")
print("=" * 80)
extracted_fields = extractor.extract_form_fields()
for field_name, value in extracted_fields.items():
    if "hazardous" in field_name.lower() or "leave of ab" in field_name.lower():
        print(f"{field_name}: {value}")
