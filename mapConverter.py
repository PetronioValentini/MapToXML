import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def process_file(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Arquivo: {input_file} não encontrado")
        return False

    with open(input_file, 'r') as f:
        lines = f.readlines()

    root = ET.Element("TextureAtlas", imagePath="sheet.png")

    part_dict = {}
    reading_part = False

    for line in lines:
        line = line.strip()

        if line.startswith("LayerManager:AddLayerParts"):
            if reading_part and part_dict:
                add_subtexture(root, part_dict)

            part_dict = {}
            reading_part = True

        elif reading_part:
            if line == "}":
                add_subtexture(root, part_dict)
                reading_part = False
            elif " = " in line:
                key, value = line.split(" = ")
                part_dict[key.strip()] = value.strip().strip('"').replace('&quot;', '')

    xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    with open(output_file, 'w') as f:
        f.write(pretty_xml)

    return True 

def add_subtexture(root, part_dict):
    ET.SubElement(root, "SubTexture", {
        "CATEGORY": part_dict.get("CATEGORY", "").replace('"', '').strip(','),
        "PARTNAME": part_dict.get("PARTNAME", "").replace('"', '').strip(','),
        "TEX_NAME": part_dict.get("TEX_NAME", "").replace('.dds', '').replace('"', '').strip(','),
        "TEX_X": part_dict.get("TEX_X", ""),
        "TEX_Y": part_dict.get("TEX_Y", ""),
        "TEX_WIDTH": part_dict.get("TEX_WIDTH", ""),
        "TEX_HEIGHT": part_dict.get("TEX_HEIGHT", ""),
        "PARTS_WIDTH": part_dict.get("PARTS_WIDTH", ""),
        "PARTS_HEIGHT": part_dict.get("PARTS_HEIGHT", ""),
    })

def main():
    input_file = input("Digite o nome do arquivo de entrada: ")
    output_file = input("Digite o nome do arquivo de saída: ")

    if process_file(input_file, output_file):
        print("Arquivo convertido com sucesso!")

if __name__ == "__main__":
    main()
