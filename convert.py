import xml.etree.ElementTree as ET
import simplejson as JS

with open("input.json", "r", encoding='UTF-8') as json_file:
    data = JS.load(json_file)

# Корневой элемент
root = ET.Element('DataMessage')

# Элементы первого уровня:
# 1. eDocument
eDocument = ET.SubElement(root, 'eDocument')









# Сохранение 
ET.indent(root, space='   ', level=0)
tree = ET.ElementTree(root)
tree.write("DataMessage.xml")