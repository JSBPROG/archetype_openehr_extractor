import glob
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
import os

class Extractor:
    """
    ExtractorXML parses OpenEHR ADL 1.4 archetype XML files and extracts metadata and element definitions in English.

    Attributes:
        file_names (list): XML file paths to process.
        json_list (list): Extracted data dictionaries.
        output_path (str): Default output path for saving JSON files.
    """
    def __init__(self, output_path="./output"):
        self.file_names = []
        self.json_list = []
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def load_doc_list(self, extension="xml"): 
        """
        Populate file_names with all files in the 'data/' folder matching extension.

        Args:
            extension (str): File extension to search for.
        """
        try:
            self.file_names = glob.glob(f"data/*.{extension}") or []
        except Exception:
            self.file_names = []

    def extract_info_from_file(self, xml_file):
        """
        Parse a single XML file and extract:
          - file path
          - purpose and use in English ('en')
          - element definitions (code, data type, name, description, SNOMED code)

        Args:
            xml_file (str): Path to the XML file.

        Returns:
            dict: Extracted information with empty defaults if parsing fails.
        """
        result = {
            "file": xml_file,
            "en": {"purpose": None, "use": None},
            "elements": []
        }

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception:
            return result

        ns = {
            'x': 'http://schemas.openehr.org/v1',
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

        
        for details in root.findall(".//x:description/x:details", ns):
            lang = details.findtext("x:language/x:code_string", default=None, namespaces=ns)
            if lang == "en":
                result["en"]["purpose"] = details.findtext("x:purpose", default=None, namespaces=ns)
                result["en"]["use"] = details.findtext("x:use", default=None, namespaces=ns)

        
        term_names = {}
        term_descs = {}
        for td in root.findall(".//x:ontology/x:term_definitions", ns):
            if td.attrib.get("language") != "en":
                continue
            for item in td.findall("x:items", ns):
                code = item.attrib.get("code")
                for sub in item.findall("x:items", ns):
                    sub_id = sub.attrib.get("id")
                    if sub_id == "text":
                        term_names[code] = sub.text
                    elif sub_id == "description":
                        term_descs[code] = sub.text

        
        snomed_bindings = {}
        for bind in root.findall(".//x:term_bindings[@terminology='SNOMED-CT']/x:items", ns):
            code = bind.attrib.get("code")
            code_str = bind.findtext("x:value/x:code_string", default=None, namespaces=ns)
            if code and code_str:
                snomed_bindings[code] = code_str

        
        for comp in root.findall(".//x:children[@xsi:type='C_COMPLEX_OBJECT']", ns):
            try:
                if comp.findtext("x:rm_type_name", namespaces=ns) != "ELEMENT":
                    continue
                code = comp.findtext("x:node_id", namespaces=ns)
                if not code:
                    continue

                val = comp.find(".//x:attributes/x:children[@xsi:type='C_COMPLEX_OBJECT']", ns)
                data_type = val.findtext("x:rm_type_name", namespaces=ns) if val is not None else None

                result["elements"].append({
                    "code": code,
                    "type": data_type,
                    "name": {
                        "en": term_names.get(code)
                    },
                    "description": {
                        "en": term_descs.get(code)
                    },
                    "snomed": snomed_bindings.get(code)
                })
            except Exception:
                continue

        return result

    def extract_all(self):
        """
        Extract information from all loaded XML files into json_list.
        """
        self.json_list = []
        for xml_file in self.file_names:
            info = self.extract_info_from_file(xml_file)
            if info is not None:
                self.json_list.append(info)

    def save_json_list(self, out_file=None):  
        """
        Save json_list to disk as formatted JSON.

        Args:
            out_file (str): Output file path. Uses default if None.
        """
        out_file = out_file or os.path.join(self.output_path, "data_from_xml.json")
        try:
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(self.json_list, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def generate_simplified_json(self, save=True):
        """
        Generate a simplified version of the extracted data with only:
          - file
          - purpose
          - use
          - elements: name and description in English

        Args:
            save (bool): Whether to save the result to a file.

        Returns:
            list: Simplified structure.
        """
        simplified = []

        for item in self.json_list:
            simplified_item = {
                "file": item.get("file"),
                "purpose": item.get("en", {}).get("purpose"),
                "use": item.get("en", {}).get("use"),
                "elements": []
            }

            for el in item.get("elements", []):
                simplified_item["elements"].append({
                    "name": el.get("name", {}).get("en"),
                    "description": el.get("description", {}).get("en")
                })

            simplified.append(simplified_item)

        if save:
            try:
                with open(os.path.join(self.output_path, "simplified_data.json"), "w", encoding="utf-8") as f:
                    json.dump(simplified, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        return simplified
