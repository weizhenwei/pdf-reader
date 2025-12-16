"""
检查特定字段的提取情况
"""
from pdf_extractor import PDFExtractor
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "Enhanced EPLI Questionnaire.pdf"

extractor = PDFExtractor(pdf_path)
fields = extractor.extract_form_fields()

print("=" * 80)
print("所有提取的字段:")
print("=" * 80)

for field_name, value in fields.items():
    print(f"\n字段名: {field_name}")
    print(f"值: {value}")

print("\n" + "=" * 80)
print("查找包含 'notification' 或 'claims' 的字段:")
print("=" * 80)

for field_name, value in fields.items():
    if 'notification' in field_name.lower() or 'claims' in field_name.lower() or 'labor' in field_name.lower():
        print(f"\n✓ {field_name}")
        print(f"  值: {value}")
