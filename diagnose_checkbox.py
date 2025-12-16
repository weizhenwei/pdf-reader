"""
PDF Checkbox 诊断工具
帮助用户检查checkbox是否被正确保存
"""
from pdf_extractor import PDFExtractor
from pypdf import PdfReader
import sys

def diagnose_checkbox(pdf_path, checkbox_name):
    """诊断特定checkbox的状态"""
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    
    if checkbox_name not in fields:
        print(f"❌ 未找到字段: {checkbox_name}")
        print(f"\n可用的checkbox字段:")
        for name, field in fields.items():
            if field.get('/FT') == '/Btn':
                print(f"  - {name}")
        return
    
    field = fields[checkbox_name]
    
    print("=" * 80)
    print(f"Checkbox 诊断: {checkbox_name}")
    print("=" * 80)
    
    # 基本信息
    print(f"\n字段类型: {field.get('/FT', 'N/A')}")
    
    # 值信息
    v_value = field.get('/V')
    as_value = field.get('/AS')
    dv_value = field.get('/DV')
    
    print(f"\n值信息:")
    print(f"  /V (Value):           {v_value}")
    print(f"  /AS (Appearance):     {as_value}")
    print(f"  /DV (Default Value):  {dv_value}")
    
    # 可用状态
    if '/_States_' in field:
        print(f"  可用状态:             {field['/_States_']}")
    
    # 判断状态
    print(f"\n状态判断:")
    
    # 使用 /AS (外观状态)
    if as_value:
        as_str = str(as_value).replace('/', '')
        if as_str in ['On', 'Yes', 'True', '1']:
            print(f"  根据外观状态 (/AS):  ✓ 已勾选")
        elif as_str in ['Off', 'No', 'False', '0']:
            print(f"  根据外观状态 (/AS):  ✗ 未勾选")
        else:
            print(f"  根据外观状态 (/AS):  ? 未知 ({as_str})")
    else:
        print(f"  根据外观状态 (/AS):  (无外观状态)")
    
    # 使用 /V (值)
    if v_value:
        v_str = str(v_value).replace('/', '')
        if v_str in ['On', 'Yes', 'True', '1']:
            print(f"  根据值 (/V):         ✓ 已勾选")
        elif v_str in ['Off', 'No', 'False', '0']:
            print(f"  根据值 (/V):         ✗ 未勾选")
        else:
            print(f"  根据值 (/V):         ? 未知 ({v_str})")
    else:
        print(f"  根据值 (/V):         (无值)")
    
    # 建议
    print(f"\n💡 建议:")
    
    # 确定实际状态（优先使用 /AS，否则使用 /V）
    actual_value = as_value if as_value else v_value
    
    if actual_value:
        actual_str = str(actual_value).replace('/', '')
        if actual_str in ['Off', 'No', 'False', '0']:
            print(f"  • 该checkbox在PDF中确实是未勾选状态")
            print(f"  • 如果您已经勾选，请确保:")
            print(f"    1. 使用PDF编辑器勾选后点击了保存")
            print(f"    2. 保存时选择了正确的保存选项（不是'另存为副本'）")
            print(f"    3. 重新打开PDF文件确认勾选状态已保存")
        elif actual_str in ['On', 'Yes', 'True', '1']:
            print(f"  • 该checkbox已正确勾选并保存")
        else:
            print(f"  • 该checkbox的值不是标准格式: {actual_str}")
    else:
        print(f"  • 该checkbox没有值，可能是PDF格式问题")
    
    print("=" * 80)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python diagnose_checkbox.py <pdf_file> [checkbox_name]")
        print("\n示例:")
        print('  python diagnose_checkbox.py "New Client Risk Review.pdf" "Employees handle hazardous materials"')
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if len(sys.argv) >= 3:
        checkbox_name = sys.argv[2]
        diagnose_checkbox(pdf_path, checkbox_name)
    else:
        # 显示所有checkbox
        print("显示所有checkbox字段，请指定要诊断的字段名\n")
        reader = PdfReader(pdf_path)
        fields = reader.get_fields()
        
        print("可用的checkbox字段:")
        for name, field in fields.items():
            if field.get('/FT') == '/Btn':
                v = field.get('/AS') or field.get('/V')
                v_str = str(v).replace('/', '') if v else 'N/A'
                status = "✓" if v_str in ['On', 'Yes', 'True', '1'] else "✗"
                print(f"  {status} {name}")
