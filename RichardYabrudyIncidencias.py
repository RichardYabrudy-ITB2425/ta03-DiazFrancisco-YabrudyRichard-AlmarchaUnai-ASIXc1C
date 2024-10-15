import xml.etree.ElementTree as ET
from datetime import datetime


def validar_fecha(fecha_str):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def extraer_incidencias(xml_file):
    # Cargar y parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Espacio de nombres en XML
    ns = {'ns1': 'http://www.exemple.com/IncidenciasGrup4'}

    # Inicializar listas
    lista_todas_incidencias = []  # Lista para almacenar todas las incidencias
    lista_incidencias_validas = []  # Lista para almacenar las incidencias válidas

    # Iterar sobre cada incidencia en el XML
    for incidencia in root.findall('.//ns1:Incidencia', ns):
        # Extraer todos los elementos de la incidencia
        incidencia_data = {}
        for elemento in incidencia:
            # Guardar los datos de cada elemento en un diccionario
            incidencia_data[elemento.tag.split('}')[1]] = elemento.text

        # Añadir la incidencia completa a la lista de todas las incidencias
        lista_todas_incidencias.append(incidencia_data)

        # Validar la fecha de la incidencia
        if 'DataIncidencia' in incidencia_data and validar_fecha(incidencia_data['DataIncidencia']):
            lista_incidencias_validas.append(incidencia_data)  # Añadir a la lista de válidas

    # Imprimir resultados
    print(f'Total de incidencias encontradas: {len(lista_todas_incidencias)}')
    print(f'Total de incidencias válidas: {len(lista_incidencias_validas)}')

    # Imprimir las incidencias válidas
    print('Incidencias válidas:')
    for inc in lista_incidencias_validas:
        print(inc)


# Ruta del archivo XML
ruta_archivo_xml = "./Grup 4 - XML Con Excel.xml"

# Llama a la función con la ruta a tu archivo XML
extraer_incidencias(ruta_archivo_xml)