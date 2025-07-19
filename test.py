from extractor import Extractor
import json


if __name__ == "__main__":
    extractor = Extractor(output_path="./output")  
    extractor.load_doc_list()
    extractor.extract_all()
    extractor.save_json_list()  

    extractor.generate_simplified_json(save=True)  



    
