# Extractor para OpenEHR ADL 1.4 Archetype en XML

Este proyecto proporciona una clase **Extractor** en Python para analizar archivos XML de arquetipos OpenEHR ADL 1.4, extrayendo metadatos y definiciones de elementos en inglés, y generando archivos JSON estructurados y simplificados.

---

## ¿Qué hace este script?

- **Carga archivos XML** desde la carpeta `data/`, buscando por extensión (`xml` por defecto).
- **Extrae información relevante** de cada archivo:
  - Propósito y uso del arquetipo (en inglés).
  - Definiciones de cada elemento (nombre, descripción, tipo, código y bindings SNOMED-CT).
- **Guarda los resultados** en formato JSON en la carpeta `output/`:
  - Un archivo completo (`data_from_xml.json`) con todo el contenido extraído.
  - Un archivo simplificado (`simplified_data.json`) solo con las partes más relevantes (nombre y descripción de cada elemento en inglés).
- **Permite adaptar la salida** a tus necesidades: puedes elegir extraer todo o una versión resumida.

---

## ¿Cómo funciona?

- Usa la librería estándar *xml.etree.ElementTree* para el análisis eficiente de XML[4][6][8].
- Recoge términos específicos solo en inglés (atributo `language="en"`).
- Asocia los códigos locales con sus binding SNOMED-CT si existen.
- Ponte en marcha con pocos pasos: solo necesitas poner tus archivos XML de arquetipo en la carpeta `data/` y lanzar el script.

---

## Estructura principal

- `Extractor.load_doc_list()`  
  Busca y lista todos los archivos XML en `data/`.
- `Extractor.extract_info_from_file()`  
  Procesa cada XML y extrae los metadatos y elementos.
- `Extractor.extract_all()`  
  Extrae la información de todos los archivos listados.
- `Extractor.save_json_list()`  
  Guarda toda la información extraída en un archivo JSON.
- `Extractor.generate_simplified_json()`  
  Genera una versión más sencilla, solo con los campos más importantes, para uso rápido o revisión manual.

---

## Ejemplo de uso básico

`from extractor import Extractor`  

`extr = Extractor()`  
`extr.load_doc_list() # Carga todos los XML en 'data/'`  
`extr.extract_all() # Procesa y extrae los datos`
`extr.save_json_list() # Guarda 'output/data_from_xml.json'`  
`extr.generate_simplified_json() # Guarda 'output/simplified_data.json'`    


---

## ¿Para quién es útil?

- Desarrolladores que trabajan con modelos clínicos openEHR.
- Quienes necesitan analizar o convertir metadatos de arquetipos a otros formatos de forma automatizada o masiva.
- Equipos de interoperabilidad en salud interesados en vincular definiciones clínicas con SNOMED-CT.

---

## Requisitos

- Python 3.x (usa solo librerías estándar).
- Archivos XML válidos exportados desde herramientas compatibles con openEHR ADL 1.4.

---

## Notas

- Todos los resultados se guardan automáticamente en la carpeta `output/`.
- El código está preparado para ignorar y continuar ante errores de archivos corruptos o mal formateados.

---



