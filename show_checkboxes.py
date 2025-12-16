"""
显示所有checkbox字段的状态
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
print("所有按钮类型字段 (/Btn) 的状态")
print("=" * 80)

if fields:
    checkbox_count = 0
    checked_count = 0
    
    for field_name, field_data in fields.items():
        # 只显示按钮类型字段（checkbox/radio button）
        if field_data.get('/FT') == '/Btn':
            checkbox_count += 1
            value = field_data.get('/V', 'N/A')
            
            # 判断是否被勾选
            is_checked = False
            if hasattr(value, 'name'):
                value_str = value.name
            else:
                value_str = str(value)
            
            # 移除前导斜杠
            if value_str.startswith('/'):
                value_str = value_str[1:]
            
            # 判断状态
            if value_str in ['On', 'Yes', 'True', '1']:
                is_checked = True
                checked_count += 1
                status = "✓ 已勾选"
            elif value_str in ['Off', 'No', 'False', '0']:
                status = "✗ 未勾选"
            else:
                status = f"? 未知状态 ({value_str})"
            
            print(f"\n{status}")
            print(f"  字段名: {field_name}")
            print(f"  原始值: {value}")
    
    print("\n" + "=" * 80)
    print(f"统计: 共 {checkbox_count} 个checkbox字段，其中 {checked_count} 个被勾选")
    print("=" * 80)
else:
    print("未找到表单字段")
