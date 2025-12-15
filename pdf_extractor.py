"""
PDF内容提取器
支持纯文本PDF和可填写表格PDF的内容提取
"""

from pypdf import PdfReader
from typing import Dict, Any, List
import json


class PDFExtractor:
    """PDF内容提取器，支持文本和表单字段提取"""
    
    def __init__(self, pdf_path: str):
        """
        初始化PDF提取器
        
        Args:
            pdf_path: PDF文件路径
        """
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)
        
    def extract_all_content(self) -> Dict[str, Any]:
        """
        提取PDF的所有内容，包括文本和表单字段
        
        Returns:
            包含文本内容、表单字段和元数据的字典
        """
        return {
            "metadata": self._extract_metadata(),
            "text_content": self.extract_text(),
            "form_fields": self.extract_form_fields(),
            "pages": self.extract_pages_content(),
            "total_pages": len(self.reader.pages)
        }
    
    def _extract_metadata(self) -> Dict[str, Any]:
        """提取PDF元数据"""
        metadata = {}
        if self.reader.metadata:
            for key, value in self.reader.metadata.items():
                # 移除PDF键名前缀
                clean_key = key.replace("/", "")
                metadata[clean_key] = str(value) if value else None
        return metadata
    
    def extract_text(self) -> str:
        """
        提取PDF所有页面的文本内容
        
        Returns:
            合并后的文本内容
        """
        text_content = []
        for i, page in enumerate(self.reader.pages):
            text = page.extract_text()
            if text and text.strip():
                text_content.append(f"=== 第 {i+1} 页 ===\n{text}")
        return "\n\n".join(text_content)
    
    def extract_form_fields(self) -> Dict[str, Any]:
        """
        提取PDF表单字段
        
        Returns:
            字段名和值的字典
        """
        fields = self.reader.get_fields()
        if not fields:
            return {}
        
        result = {}
        for field_name, field in fields.items():
            value = field.get("/V")
            result[field_name] = self._normalize_value(value)
        
        return result
    
    def extract_pages_content(self) -> List[Dict[str, Any]]:
        """
        按页提取内容，包括文本和该页的表单字段
        
        Returns:
            每页内容的列表
        """
        pages = []
        for i, page in enumerate(self.reader.pages):
            page_data = {
                "page_number": i + 1,
                "text": page.extract_text() or "",
                "fields": {}
            }
            
            # 提取该页的表单字段
            if "/Annots" in page:
                try:
                    for annot in page["/Annots"]:
                        obj = annot.get_object()
                        if obj.get("/Subtype") == "/Widget":
                            name = self._get_field_full_name(obj)
                            if name:
                                raw_value = self._get_field_value_recursive(obj)
                                page_data["fields"][name] = self._normalize_value(raw_value)
                except Exception as e:
                    print(f"警告: 提取第{i+1}页表单字段时出错: {e}")
            
            pages.append(page_data)
        return pages
    
    def _normalize_value(self, value, interpret_boolean=False):
        """
        统一处理PDF中的各种值类型
        
        Args:
            value: PDF字段值
            interpret_boolean: 是否将On、Off等转换为Yes/No
            
        Returns:
            标准化后的值
        """
        if value is None:
            return None
        
        # Boolean / NameObject
        if hasattr(value, "name"):
            str_value = value.name
            # 始终移除前导斜杠（PDF NameObject格式）
            if str_value.startswith("/"):
                str_value = str_value[1:]
            
            if interpret_boolean:
                # 将常见的布尔值转换为Yes/No
                if str_value in ["On", "Yes", "True", "1"]:
                    return "Yes"
                elif str_value in ["Off", "No", "False", "0"]:
                    return "No"
            return str_value
        
        # Text
        str_value = str(value)
        # 也处理文本形式的斜杠前缀
        if str_value.startswith("/"):
            str_value = str_value[1:]
            
        if interpret_boolean:
            # 处理数字形式的布尔值
            if str_value in ["0"]:
                return "No"
            elif str_value in ["1"]:
                return "Yes"
        return str_value
    
    def _get_field_full_name(self, field_obj):
        """
        递归获取字段完整名称（处理层级）
        
        Args:
            field_obj: PDF字段对象
            
        Returns:
            字段完整名称
        """
        names = []
        current = field_obj
        while current:
            if "/T" in current:
                names.insert(0, str(current["/T"]))
            if "/Parent" in current:
                current = current["/Parent"].get_object()
            else:
                break
        return ".".join(names) if names else None
    
    def _get_field_value_recursive(self, field_obj):
        """
        递归查找字段值
        
        Args:
            field_obj: PDF字段对象
            
        Returns:
            字段值
        """
        if "/V" in field_obj:
            return field_obj["/V"]
        if "/Parent" in field_obj:
            return self._get_field_value_recursive(field_obj["/Parent"].get_object())
        return None
    
    def get_formatted_content(self, interpret_boolean=True) -> str:
        """
        获取格式化的PDF内容，适合作为LLM的上下文
        
        Args:
            interpret_boolean: 是否将/On、/Off等转换为Yes/No
        
        Returns:
            格式化的文本内容
        """
        content_parts = []
        
        # 添加元数据
        metadata = self._extract_metadata()
        if metadata:
            content_parts.append("【PDF文档信息】")
            for key, value in metadata.items():
                if value:
                    content_parts.append(f"{key}: {value}")
            content_parts.append("")
        
        # 添加文本内容
        text = self.extract_text()
        if text.strip():
            content_parts.append("【文档文本内容】")
            content_parts.append(text)
            content_parts.append("")
        
        # 添加表单字段 - 改进版
        fields = self.extract_form_fields()
        if fields:
            content_parts.append("【表单字段内容】")
            
            # 智能分组和格式化字段
            formatted_fields = self._format_fields_intelligently(fields, interpret_boolean)
            content_parts.extend(formatted_fields)
            content_parts.append("")
        
        return "\n".join(content_parts)
    
    def _format_fields_intelligently(self, fields: Dict[str, Any], interpret_boolean: bool = True) -> list:
        """
        智能格式化表单字段，将相关字段组合在一起
        
        Args:
            fields: 字段字典
            interpret_boolean: 是否解释布尔值
            
        Returns:
            格式化后的字段列表
        """
        formatted = []
        processed = set()
        
        for field_name, raw_value in fields.items():
            if field_name in processed:
                continue
            
            # 解释值
            value = self._normalize_value(raw_value, interpret_boolean) if interpret_boolean else raw_value
            
            # 跳过空值和未选中的复选框/单选框
            if value is None or value == "":
                processed.add(field_name)
                continue
            
            # 如果是No或Off，跳过（通常不需要显示未选中的选项）
            if value in ["No", "Off", "0"]:
                processed.add(field_name)
                continue
            
            # 检查是否有关联的详细字段（通常以0结尾）
            detail_field_name = field_name + "0"
            detail_value = None
            
            if detail_field_name in fields:
                detail_value = fields[detail_field_name]
                processed.add(detail_field_name)
            
            # 格式化输出
            if value in ["Yes", "On", "1"]:
                # 这是一个选中的选项
                if detail_value and detail_value.strip():
                    formatted.append(f"✓ {field_name}: Yes (详情: {detail_value})")
                else:
                    formatted.append(f"✓ {field_name}: Yes")
            else:
                # 普通文本字段
                formatted.append(f"• {field_name}: {value}")
            
            processed.add(field_name)
        
        return formatted
    
    def get_structured_data(self, interpret_boolean=True) -> Dict[str, Any]:
        """
        获取结构化的PDF数据，包含智能解释的字段值
        
        Args:
            interpret_boolean: 是否将/On、/Off等转换为Yes/No
            
        Returns:
            结构化数据字典
        """
        fields = self.extract_form_fields()
        
        # 创建解释后的字段字典
        interpreted_fields = {}
        field_groups = {}
        
        for field_name, raw_value in fields.items():
            # 解释值
            value = self._normalize_value(raw_value, interpret_boolean) if interpret_boolean else raw_value
            
            # 跳过完全空的值
            if value is None or value == "":
                continue
            
            interpreted_fields[field_name] = {
                "raw_value": raw_value,
                "interpreted_value": value,
                "is_checked": value in ["Yes", "On", "1"],
                "is_unchecked": value in ["No", "Off", "0"]
            }
            
            # 尝试分组（基于字段名）
            if field_name.endswith("0"):
                base_name = field_name[:-1]
                if base_name not in field_groups:
                    field_groups[base_name] = {}
                field_groups[base_name]["detail"] = value
            else:
                if field_name not in field_groups:
                    field_groups[field_name] = {}
                field_groups[field_name]["value"] = value
        
        return {
            "metadata": self._extract_metadata(),
            "text_content": self.extract_text(),
            "fields": interpreted_fields,
            "field_groups": field_groups,
            "total_pages": len(self.reader.pages)
        }
    
    def to_json(self) -> str:
        """
        将提取的内容转换为JSON格式
        
        Returns:
            JSON字符串
        """
        content = self.extract_all_content()
        return json.dumps(content, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    
    # 测试代码
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        pdf_path = "New Client Risk Review.pdf"
        print(f"使用默认PDF文件: {pdf_path}\n")
    
    try:
        extractor = PDFExtractor(pdf_path)
        
        # 显示格式化内容
        print("=" * 60)
        print("PDF内容提取结果")
        print("=" * 60)
        print(extractor.get_formatted_content())
        
        # 可选：保存为JSON
        # with open("pdf_content.json", "w", encoding="utf-8") as f:
        #     f.write(extractor.to_json())
        # print("\n内容已保存到 pdf_content.json")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {pdf_path}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
