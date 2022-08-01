import xml.etree.ElementTree as ET
import json
import uuid
import datetime
import xmltodict
import codecs

xml_dict_names = ['RegionDict', 'ProcessingKindDict', 'ObjectKindDict',
                  'InformationKindDict', 'CoordinateSystemDict']

path = codecs.open('RegionDict.xml', 'r', 'utf_8_sig')
Region_Dict = xmltodict.parse(path.read())
path = codecs.open('ProcessingKindDict.xml', 'r', 'utf_8_sig')
ProcessingKindDict = xmltodict.parse(path.read())
path = codecs.open('ObjectKindDict.xml', 'r', 'utf_8_sig')
ObjectKindDict = xmltodict.parse(path.read())
path = codecs.open('InformationKindDict.xml', 'r', 'utf_8_sig')
InformationKindDict = xmltodict.parse(path.read())
path = codecs.open('CoordinateSystemDict.xml', 'r', 'utf_8_sig')
CoordinateSystemDict = xmltodict.parse(path.read())

def dict_find(name, search_name, search_value, value_name):
    for item in name['xs:schema']['xs:simpleType']['xs:restriction']['xs:enumeration']:
        if item[f'{search_name}'] == f'{search_value}':
            return item[value_name]
    # pretty = JS.dumps(xml_dict, ensure_ascii=False, indent=4)
    # print(pretty)
    # print(xml_dict)
    # print(type(xml_dict))
    # for item in xml_dict['xs:schema']['xs:simpleType']['xs:restriction']['xs:enumeration']:
    #     print(item['@value'])
    




### Вытаскиваем значения справочников

###


ns = {'xs': 'http://www.w3.org/2001/XMLSchema'}
with open("input.json", "r", encoding='UTF-8') as json_file:
    data = json.load(json_file)
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

features = data['features']
p = 'properties'
s = 'string'
g = 'geometry'
c = 'coordinates'

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
Count_Unload = str(len(features))
Sender = ET.SubElement(eDocument, 'Sender', attrib={'Region':Region, 'Name':Name, 'DateTime_Upload':DateTime_Upload,
                                                    'Count_Unload':Count_Unload})
# 2
Package = ET.SubElement(root, 'Package')
# 2.1
CoordinateSystem = 'EPSG:3857'
ZonyMozno = ET.SubElement(Package, 'ZonyMozno', attrib={'CoordinateSystem':CoordinateSystem})
# 2.1.1

#
#
#
# print(len(features[1][g][c][0]))


# Собираем объект
for num_obj in range(len(features)):
    # print(features[i][p][s])

    if features[num_obj][g]['type'] == 'Polygon':
            # Polygon 
            # Инициализируем геометрию/часть геометрии объекта
            ZonyMoznoEntitySpatial = ET.SubElement(ZonyMozno, 'ZonyMoznoEntitySpatial')
            Region = dict_find(Region_Dict, 'xs:documentation', features[num_obj][p][s], '@value')
            Name = features[num_obj][p]['string4']
            # Инициализируем объект
            ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':f'29', 'Name':f'{Name}',
                                                'DocumentName':ph, 'Authority':ph})                                   
            SpatialElement = ET.SubElement(ZonyMoznoEntitySpatial, 'SpatialElement')
            SpelementUnitOuter = ET.SubElement(SpatialElement, 'SpelementUnit', attrib={'TypeUnit':'Точка'})
            if len(features[num_obj][g][c]) == 1:
                for num_o_point in range(len(features[num_obj][g][c][0])):
                    x = features[num_obj][g][c][0][num_o_point][1]
                    y = features[num_obj][g][c][0][num_o_point][0]
                    n_o_p = num_o_point
                    if n_o_p == len(features[num_obj][g][c][0])-1:
                        n_o_p = 0
                    NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_o_p+1}', 'X':f'{x}', 'Y':f'{y}'})
            # Polygon with inner    
            else:
                for num_o_point in range(len(features[num_obj][g][c][0])):
                    x = features[num_obj][g][c][0][num_o_point][1]
                    y = features[num_obj][g][c][0][num_o_point][0]
                    n_o_p = num_o_point
                    if n_o_p == len(features[num_obj][g][c][0])-1:
                        n_o_p = 0
                    NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_o_p+1}', 'X':f'{x}', 'Y':f'{y}'})
                SpatialRingElement = ET.SubElement(SpatialElement, 'SpatialRingElement')
                SpelementUnitInner = ET.SubElement(SpatialRingElement, 'SpelementUnit')
                for num_subpoly in range(len(features[num_obj][g][c])):
                    if num_subpoly > 0:
                        for num_i_point in range(len(features[num_obj][g][c][num_subpoly])):
                            x = features[num_obj][g][c][num_subpoly][num_i_point][1]
                            y = features[num_obj][g][c][num_subpoly][num_i_point][0]
                            n_i_p = num_i_point
                            if n_i_p == len(features[num_obj][g][c][num_subpoly])-1:
                                n_i_p = 0
                            NewOrdinateInner = ET.SubElement(SpelementUnitInner, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_i_p+1}', 'X':f'{x}', 'Y':f'{y}'})
    # Multipolygon
    else:
        # Инициализируем геометрию/часть геометрии объекта
        ZonyMoznoEntitySpatial = ET.SubElement(ZonyMozno, 'ZonyMoznoEntitySpatial')
        Region = dict_find(Region_Dict, 'xs:documentation', features[num_obj][p][s], '@value')
        Name = features[num_obj][p]['string4']
        # Инициализируем объект
        ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':f'29', 'Name':f'{Name}',
                                            'DocumentName':ph, 'Authority':ph})
        for num_part in range(len(features[num_obj][g][c])):
            SpatialElement = ET.SubElement(ZonyMoznoEntitySpatial, 'SpatialElement')
            for num_poly in range(len(features[num_obj][g][c][num_part])):
                # Polygon 
                # Инициализируем геометрию/часть геометрии объекта                                 
                # SpatialElement = ET.SubElement(ZonyMoznoEntitySpatial, 'SpatialElement')
                
                if len(features[num_obj][g][c][num_part]) == 1:
                    SpelementUnitOuter = ET.SubElement(SpatialElement, 'SpelementUnit', attrib={'TypeUnit':'мультиТочка'})
                    for num_o_point in range(len(features[num_obj][g][c][num_part][num_poly])):
                        x = features[num_obj][g][c][num_part][num_poly][num_o_point][1]
                        y = features[num_obj][g][c][num_part][num_poly][num_o_point][0]
                        n_o_p = num_o_point
                        if n_o_p == len(features[num_obj][g][c][num_part][num_poly])-1:
                            n_o_p = 0
                        NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_o_p+1}', 'X':f'{x}', 'Y':f'{y}'})
                # Polygon with inner    
                # else:
                #     for num_o_point in range(len(features[num_obj][g][c][0])):
                #         x = features[num_obj][g][c][0][num_o_point][1]
                #         y = features[num_obj][g][c][0][num_o_point][0]
                #         n_o_p = num_o_point
                #         if n_o_p == len(features[num_obj][g][c][0])-1:
                #             n_o_p = 0
                #         NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_o_p+1}', 'X':f'{x}', 'Y':f'{y}'})
                #     SpatialRingElement = ET.SubElement(SpatialElement, 'SpatialRingElement')
                #     SpelementUnitInner = ET.SubElement(SpatialRingElement, 'SpelementUnit')
                #     for num_subpoly in range(len(features[num_obj][g][c])):
                #         if num_subpoly > 0:
                #             for num_i_point in range(len(features[num_obj][g][c][num_subpoly])):
                #                 x = features[num_obj][g][c][num_subpoly][num_i_point][1]
                #                 y = features[num_obj][g][c][num_subpoly][num_i_point][0]
                #                 n_i_p = num_i_point
                #                 if n_i_p == len(features[num_obj][g][c][num_subpoly])-1:
                #                     n_i_p = 0
                #                 NewOrdinateInner = ET.SubElement(SpelementUnitInner, 'NewOrdinate', attrib={'Num_Geopoint':f'{n_i_p+1}', 'X':f'{x}', 'Y':f'{y}'})
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # for num_point in range(len(features[num_obj][g][c][0])):
    #     # print(features[i][g][c][0][j][1])
    #     SpelementUnitOuter = ET.SubElement(SpatialElement, 'SpelementUnit', attrib={'TypeUnit':'Точка'})
    #     if features[num_obj][g]['type'] == 'Polygon':
    #         if len(features[num_obj][g][c]) == 1:
    #             x = features[num_obj][g][c][0][num_point][1]
    #             y = features[num_obj][g][c][0][num_point][0]
    #             NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{num_point+1}', 'X':f'{x}', 'Y':f'{y}'})
    #         else:
    #             # num_point = 0
    #             print(features[num_obj][g][c][0][0][0])
    #             x = features[num_obj][g][c][0][0][0][1]
    #             y = features[num_obj][g][c][0][0][0][0]
    #             NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{num_point+1}', 'X':f'{x}', 'Y':f'{y}'})
    #             SpatialRingElement = ET.SubElement(SpatialElement, 'SpatialRingElement')
    #             SpelementUnitInner = ET.SubElement(SpatialRingElement, 'SpelementUnit')
    #             for num_subpoly in range(len(features[num_obj][g][c])):
    #                 x = features[num_obj][g][c][0][num_subpoly+1][1]
    #                 y = features[num_obj][g][c][0][num_subpoly+1][0]
    #                 NewOrdinateInner = ET.SubElement(SpelementUnitInner, 'NewOrdinate', attrib={'Num_Geopoint':ph, 'X':ph, 'Y':ph})
    #                 print(len(features[num_obj][g][c]))
                # print(f'== {features[num_obj][g][c]}')

        # else:
        #     print(len(features[i][g][c][0][j]))
        #     for k in range(len(features[i][g][c][0][j])):
        #         x = features[i][g][c][0][j][0][1]
        #         y = features[i][g][c][0][j][0][0]
        #         NewOrdinateOuter = ET.SubElement(SpelementUnitOuter, 'NewOrdinate', attrib={'Num_Geopoint':f'{j+1}', 'X':f'{x}', 'Y':f'{y}'})





#     for j in rg['xs:schema']['xs:simpleType']['xs:restriction']['xs:enumeration']:
#         ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':ph, 'Name':ph,
#                                             'DocumentName':ph, 'Authority':ph})
#         root[1][0][0].append(ZonyMoznoObjectInfo)

#
#
#
# 2.1.1.1
ZonyMoznoObjectInfo = ET.SubElement(ZonyMoznoEntitySpatial, 'ZonyMoznoObjectInfo', attrib={'Index':'', 'Region':ph, 'Name':ph,
                                                                                           'DocumentName':ph, 'Authority':ph})




# 2.1.1.2
SpatialElement = ET.SubElement(ZonyMoznoEntitySpatial, 'SpatialElement')

# 2.1.1.2.1
SpelementUnitOuter = ET.SubElement(SpatialElement, 'SpelementUnit', attrib={'TypeUnit':'Точка'})
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


# for i in range(len(features)):
#     d = i + 1
#     for key, value in features[d]['properties'].items():
#         print(key, value)
#         d+=1
#     print('')





    


# Сохранение 
ET.indent(root, space='   ', level=0)
tree = ET.ElementTree(root)





tree.write("DataMessage.xml", encoding='UTF-8')