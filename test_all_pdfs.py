"""
测试所有PDF文件的字段提取功能
"""
from pdf_extractor import PDFExtractor
import os

# 测试的PDF文件列表
test_pdfs = [
    "Business_Information_Form.pdf",
    "Enhanced EPLI Questionnaire.pdf",
    "New Client Risk Review.pdf",
]

print("=" * 80)
print("PDF字段提取测试")
print("=" * 80)

for pdf_file in test_pdfs:
    if not os.path.exists(pdf_file):
        print(f"\n❌ 文件不存在: {pdf_file}")
        continue
    
    print(f"\n{'=' * 80}")
    print(f"测试文件: {pdf_file}")
    print('=' * 80)
    
    try:
        extractor = PDFExtractor(pdf_file)
        
        # 提取字段
        fields = extractor.extract_form_fields()
        
        if fields:
            print(f"\n✅ 成功提取 {len(fields)} 个字段:\n")
            
            # 按类型分组显示
            text_fields = {}
            button_fields = {}
            
            for field_name, value in fields.items():
                if value in ['Yes', 'No', 'On', 'Off', '0', '1']:
                    button_fields[field_name] = value
                else:
                    text_fields[field_name] = value
            
            if text_fields:
                print("文本字段:")
                for name, value in text_fields.items():
                    value_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    print(f"  • {name}: {value_str}")
            
            if button_fields:
                print("\n按钮字段 (checkbox/radio):")
                for name, value in button_fields.items():
                    symbol = "✓" if value in ['Yes', 'On', '1'] else "✗"
                    print(f"  {symbol} {name}: {value}")
        else:
            print("\n⚠️  未找到表单字段")
        
        # 显示页数
        print(f"\n文档信息: {len(extractor.reader.pages)} 页")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
