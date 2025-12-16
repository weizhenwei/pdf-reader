"""
调试脚本：查看PDF表单字段的原始值
"""
from pdf_extractor import PDFExtractor
import json
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "New Client Risk Review.pdf"

extractor = PDFExtractor(pdf_path)

# 获取原始字段
fields = extractor.reader.get_fields()

print("=" * 80)
print("原始表单字段详细信息")
print("=" * 80)

if fields:
    for field_name, field_data in fields.items():
        print(f"\n字段名: {field_name}")
        print(f"  完整数据: {field_data}")
        
        # 显示所有键值对
        for key, value in field_data.items():
            print(f"  {key}: {value}")
        
        # 特别关注值相关的键
        if "/V" in field_data:
            print(f"  >>> 值 (/V): {field_data['/V']}")
        if "/DV" in field_data:
            print(f"  >>> 默认值 (/DV): {field_data['/DV']}")
        if "/AS" in field_data:
            print(f"  >>> 外观状态 (/AS): {field_data['/AS']}")
        
        print("-" * 80)
else:
    print("未找到表单字段")

# 也显示提取后的字段
print("\n" + "=" * 80)
print("提取后的字段值")
print("=" * 80)
extracted_fields = extractor.extract_form_fields()
print(json.dumps(extracted_fields, ensure_ascii=False, indent=2))
