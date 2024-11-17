import os
import xml.etree.ElementTree as ET

def process_xml_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            process_xml_file(file_path, directory)

def process_xml_file(file_path, output_directory):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Buscar el título
        ns = {'ns': 'http://openlyrics.info/namespace/2009/song'}  # Espacio de nombres
        title_element = root.find(".//ns:title", ns)
        if title_element is None:
            print(f"No se encontró un <title> en el archivo {file_path}")
            return

        title = title_element.text.strip() if title_element.text else "Sin_Titulo"
        output_file = os.path.join(output_directory, f"{title}.txt")

        # Buscar las líneas
        lines_elements = root.findall(".//ns:lines", ns)
        content = ""
        for lines_element in lines_elements:
            lines_text = ""
            for part in lines_element.itertext():
                lines_text += part + "\n"
            content += lines_text + "\n"  # Agregar salto de línea al final de cada <lines>

        # Escribir el contenido en el nuevo archivo
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(content.strip())
        
        # Eliminar el archivo XML original
        os.remove(file_path)
        print(f"Archivo generado y procesado: {output_file}. Archivo XML eliminado: {file_path}")
        
    except ET.ParseError as e:
        print(f"Error al analizar el archivo {file_path}: {e}")
    except Exception as e:
        print(f"Ocurrió un error procesando el archivo {file_path}: {e}")

# Directorio de entrada
input_directory = "exportados"

# Procesar los archivos XML en el directorio
process_xml_directory(input_directory)

