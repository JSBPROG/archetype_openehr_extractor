from extractor import Extractor
import json


if __name__ == "__main__":
    extractor = Extractor(output_path="./output")  # puedes cambiar la ruta si quieres
    extractor.load_doc_list()
    extractor.extract_all()
    extractor.save_json_list()  # guarda data_from_xml.json

    extractor.generate_simplified_json(save=True)  # guarda simplified_data.json



    
