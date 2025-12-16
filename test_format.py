"""
测试格式化输出
"""
from pdf_extractor import PDFExtractor
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "Enhanced EPLI Questionnaire.pdf"

extractor = PDFExtractor(pdf_path)

# 获取格式化内容
formatted_content = extractor.get_formatted_content()

print("=" * 80)
print("格式化内容:")
print("=" * 80)
print(formatted_content)

print("\n" + "=" * 80)
print("查找 'notification' 相关内容:")
print("=" * 80)

lines = formatted_content.split('\n')
for i, line in enumerate(lines):
    if 'notification' in line.lower() or 'claims' in line.lower():
        print(f"行 {i}: {line}")
