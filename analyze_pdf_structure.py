"""
深入分析PDF表单字段和Appearance Stream
"""
from pypdf import PdfReader
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "Enhanced EPLI Questionnaire.pdf"

print("=" * 80)
print(f"分析PDF: {pdf_path}")
print("=" * 80)

reader = PdfReader(pdf_path)

# 1. 检查表单字段
print("\n1. 表单字段分析:")
print("-" * 80)
fields = reader.get_fields()
if fields:
    print(f"找到 {len(fields)} 个表单字段:\n")
    for field_name, field_data in fields.items():
        print(f"字段名: {field_name}")
        print(f"  类型 (/FT): {field_data.get('/FT', 'N/A')}")
        print(f"  值 (/V): {field_data.get('/V', 'N/A')}")
        print(f"  默认值 (/DV): {field_data.get('/DV', 'N/A')}")
        print(f"  外观状态 (/AS): {field_data.get('/AS', 'N/A')}")
        
        # 检查Appearance字典
        if '/AP' in field_data:
            print(f"  外观字典 (/AP): 存在")
            ap = field_data['/AP']
            if '/N' in ap:
                print(f"    正常外观 (/N): {ap['/N']}")
        print()
else:
    print("未找到表单字段！")

# 2. 检查页面注释（Annotations）
print("\n2. 页面注释分析:")
print("-" * 80)
for page_num, page in enumerate(reader.pages):
    print(f"\n第 {page_num + 1} 页:")
    
    if "/Annots" in page:
        annots = page["/Annots"]
        print(f"  找到 {len(annots)} 个注释")
        
        for i, annot_ref in enumerate(annots):
            try:
                annot = annot_ref.get_object()
                subtype = annot.get("/Subtype", "N/A")
                
                print(f"\n  注释 {i+1}:")
                print(f"    子类型: {subtype}")
                
                if subtype == "/Widget":
                    # 这是表单字段widget
                    print(f"    字段名 (/T): {annot.get('/T', 'N/A')}")
                    print(f"    字段类型 (/FT): {annot.get('/FT', 'N/A')}")
                    print(f"    值 (/V): {annot.get('/V', 'N/A')}")
                    print(f"    默认值 (/DV): {annot.get('/DV', 'N/A')}")
                    
                    # 检查Appearance
                    if '/AP' in annot:
                        print(f"    有外观字典 (/AP)")
                        ap = annot['/AP']
                        if '/N' in ap:
                            n_ap = ap['/N']
                            print(f"      正常外观类型: {type(n_ap)}")
                            
                            # 如果是字典，可能有多个状态
                            if hasattr(n_ap, 'get_object'):
                                n_ap = n_ap.get_object()
                            
                            if isinstance(n_ap, dict):
                                print(f"      外观状态: {list(n_ap.keys())}")
                    
                    # 检查矩形位置
                    if '/Rect' in annot:
                        rect = annot['/Rect']
                        print(f"    位置 (/Rect): {rect}")
                    
            except Exception as e:
                print(f"  注释 {i+1} 解析错误: {e}")
    else:
        print("  没有注释")

# 3. 提取页面文本内容
print("\n\n3. 页面文本内容:")
print("-" * 80)
for page_num, page in enumerate(reader.pages):
    text = page.extract_text()
    print(f"\n第 {page_num + 1} 页文本长度: {len(text)} 字符")
    print("前500字符:")
    print(text[:500])

print("\n" + "=" * 80)
