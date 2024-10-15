import xml.etree.ElementTree as ET

# Define el espacio de nombres utilizado en el XML
namespaces = {'ns1': 'http://www.exemple.com/IncidenciasGrup4'}

# Parsear el documento XML
tree = ET.parse('Grup 4 - XML Con Excel.xml')
root = tree.getroot()

# Buscar el nodo NivellUrgencia utilizando el espacio de nombres
item_code_node = root.find('ns1:Incidencias/ns1:Incidencia/ns1:NivellUrgencia', namespaces)

# Comprobar si se ha encontrado el nodo
if item_code_node is not None:
    item_code = item_code_node.text

    # Validar el valor del nodo NivellUrgencia
    if item_code != 'ABWS':
        raise ValueError('The ItemCode value is invalid.')
    else:
        print(f'NivellUrgencia: {item_code} is valid.')
else:
    print('Node not found.')
