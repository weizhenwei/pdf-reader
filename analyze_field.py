"""
深入分析 'Do you have any employees currently on leave of ab' 字段
"""
from pdf_extractor import PDFExtractor
from pypdf import PdfReader
import sys

if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    pdf_path = "New Client Risk Review.pdf"

reader = PdfReader(pdf_path)
fields = reader.get_fields()

target_field_name = "Do you have any employees currently on leave of ab"

if target_field_name in fields:
    field_data = fields[target_field_name]
    
    print("=" * 80)
    print(f"字段分析: {target_field_name}")
    print("=" * 80)
    
    print("\n完整字段数据:")
    for key, value in field_data.items():
        print(f"  {key}: {value}")
    
    # 如果有子字段，分析子字段
    if "/Kids" in field_data:
        print("\n" + "=" * 80)
        print("子字段分析:")
        print("=" * 80)
        
        kids = field_data["/Kids"]
        for i, kid_ref in enumerate(kids):
            print(f"\n子字段 {i+1}:")
            try:
                kid_obj = kid_ref.get_object()
                for key, value in kid_obj.items():
                    print(f"  {key}: {value}")
            except Exception as e:
                print(f"  错误: {e}")
    
    # 检查页面上的注释
    print("\n" + "=" * 80)
    print("检查页面注释:")
    print("=" * 80)
    
    for page_num, page in enumerate(reader.pages):
        if "/Annots" in page:
            print(f"\n第 {page_num + 1} 页:")
            try:
                for annot_ref in page["/Annots"]:
                    annot = annot_ref.get_object()
                    if annot.get("/Subtype") == "/Widget":
                        # 获取字段名
                        field_name = annot.get("/T", "")
                        if target_field_name in str(field_name):
                            print(f"  找到相关widget:")
                            for key, value in annot.items():
                                print(f"    {key}: {value}")
            except Exception as e:
                print(f"  错误: {e}")
else:
    print(f"未找到字段: {target_field_name}")
