"""
查找特定文本相关的字段
"""
from pypdf import PdfReader
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "Enhanced EPLI Questionnaire.pdf"

reader = PdfReader(pdf_path)

print("=" * 80)
print("查找所有字段")
print("=" * 80)

# 1. 从字段定义查找
fields = reader.get_fields()
if fields:
    print(f"\n从字段定义中找到 {len(fields)} 个字段:\n")
    for field_name, field_data in fields.items():
        print(f"字段名: {field_name}")
        print(f"  类型: {field_data.get('/FT', 'N/A')}")
        print(f"  值: {field_data.get('/V', 'N/A')}")
        print()

# 2. 从页面注释查找
print("\n" + "=" * 80)
print("从页面注释中查找字段")
print("=" * 80)

for page_num, page in enumerate(reader.pages):
    if "/Annots" not in page:
        continue
    
    print(f"\n第 {page_num + 1} 页:")
    annots = page["/Annots"]
    
    for i, annot_ref in enumerate(annots):
        try:
            annot = annot_ref.get_object()
            
            if annot.get("/Subtype") == "/Widget":
                field_name = annot.get("/T")
                field_type = annot.get("/FT")
                value = annot.get("/V")
                rect = annot.get("/Rect")
                
                print(f"\n  Widget {i+1}:")
                print(f"    字段名: {field_name}")
                print(f"    类型: {field_type}")
                print(f"    值: {value}")
                if rect:
                    print(f"    位置: {rect}")
                
                # 检查是否有父字段
                if "/Parent" in annot:
                    parent = annot["/Parent"].get_object()
                    parent_name = parent.get("/T")
                    print(f"    父字段: {parent_name}")
                
        except Exception as e:
            print(f"  Widget {i+1} 解析错误: {e}")
