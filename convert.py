from textwrap import indent
import xml.etree.ElementTree as ET
import json as JS
import uuid
import datetime
import xmltodict
import codecs

xml_file = codecs.open( "RegionDict.xml", "r", "utf_8_sig" )
a = xmltodict.parse(xml_file.read())
pretty = JS.dumps(a, ensure_ascii=False, indent=4)
# print(pretty)
# print(a)
# print(type(a))

for item in a['xs:schema']['xs:simpleType']['xs:restriction']['xs:enumeration']:
    print(item['@value'])

# for key, value in a['xs:schema']['xs:simpleType'][0]['xs:restriction'].items():
#     print(key,value)
#     print('')





ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
with open("input.json", "r", encoding='UTF-8') as json_file:
    data = JS.load(json_file)
d = ET.parse('Dictionaries.xml')
d_root = d.getroot()

############################
# Электронный документ:
# 1. Тип обработки заявки
PKDict = {1:'Addition', 2:'Replacement', 3:'Deletion'}
ProcessingKind = PKDict[1]
# 2. Тип объектов, передаваемый в рамках XML-файла
IKDict = {1:'SpecialZones', 2:'ZonyMozno', 3:'ParcelWithoutBorder', 4:'FreeRightParcels'}
InformationKind = IKDict[2]

# Отправитель:
# 1. Код региона отправителя
Region = '29'
# 2. Наименование организации отправителя
Name = 'ООО "Рога и Копыта"'




############################

# for i in d_root[0][1].findall('./xs:enumeration/[@value="29"]', ns):
#     print(i.tag, i.attrib)

ph = '*****'

# Корневой элемент
root = ET.Element('DataMessage')
# 1
GUID = str(uuid.uuid4()).upper()
eDocument = ET.SubElement(root, 'eDocument', attrib={'Version':'01', 'GUID':GUID, 'ProcessingKind':ProcessingKind,
                                                    'InformationKind':InformationKind})
# 1.1
now = datetime.datetime.now()
DateTime_Upload = now.strftime("%Y-%m-%dT%H:%M:%S")
Count_Unload = str(len(data['features']))
Sender = ET.SubElement(eDocument, 'Sender', attrib={'Region':Region, 'Name':Name, 'DateTime_Upload':DateTime_Upload,
                                                    'Count_Unload':Count_Unload})
# 2
Package = ET.SubElement(root, 'Package')
# 2.1
CoordinateSystem = 'EPSG:3857'
ZonyMozno = ET.SubElement(Package, 'ZonyMozno', attrib={'CoordinateSystem':CoordinateSystem})
# 2.1.1
ZonyMoznoEntitySpatial = ET.SubElement(ZonyMozno, 'ZonyMoznoEntitySpatial')




# 2.1.1.1
ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':ph, 'Name':ph,
                                                                                           'DocumentName':ph, 'Authority':ph})




# 2.1.1.2
SpatialElement = ET.SubElement(ZonyMoznoEntitySpatial, 'SpatialElement')


# 2.1.1.2.1
SpelementUnitOuter = ET.SubElement(SpatialElement, 'SpelementUnit', attrib={'TypeUnit':ph})
# 2.1.1.2.1.1
NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':ph, 'X':ph, 'Y':ph})
# 2.1.1.2.2
SpatialRingElement = ET.SubElement(SpatialElement, 'SpatialRingElement')
# 2.1.1.2.2.1
SpelementUnitInner = ET.SubElement(SpatialRingElement, 'SpelementUnit')
# 2.1.1.2.2.1.1
NewOrdinateInner = ET.SubElement(SpelementUnitInner, 'NewOrdinate', attrib={'Num_Geopoint':ph, 'X':ph, 'Y':ph})

# for i in root[1][0][0][0].iter():
    # root[1][0][0][0].append(ZonyMoznoObjectInfo)


# for i in range(len(data['features'])):
#     d = i + 1
#     for key, value in data['features'][d]['properties'].items():
#         print(key, value)
#         d+=1
#     print('')


# for i in range(len(data['features'])):
#     print(data['features'][i]['properties'][].values())
#     print('')

    # ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':ph, 'Name':ph,
    #                                                                                        'DocumentName':ph, 'Authority':ph})
    # root[1][0][0].append(ZonyMoznoObjectInfo)


    


# Сохранение 
ET.indent(root, space='   ', level=0)
tree = ET.ElementTree(root)





tree.write("DataMessage.xml", encoding='UTF-8')