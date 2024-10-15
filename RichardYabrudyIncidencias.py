import xml.etree.ElementTree as ET
from datetime import datetime


def validar_fecha(fecha_str):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def extraer_fechas_y_validar(xml_file):
    # Cargar y parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Espacio de nombres en XML
    ns = {'ns1': 'http://www.exemple.com/IncidenciasGrup4'}

    # Inicializar contadores
    total_fechas = 0
    total_fechas_validas = 0

    # Iterar sobre cada incidencia en el XML
    for incidencia in root.findall('.//ns1:Incidencia', ns):
        # Extraer la fecha de incidencia
        fecha_incidencia = incidencia.find('ns1:DataIncidencia', ns)
        if fecha_incidencia is not None:
            fecha_incidencia_str = fecha_incidencia.text
            total_fechas += 1

            # Validar la fecha
            if validar_fecha(fecha_incidencia_str):
                total_fechas_validas += 1

    print(f'Total de fechas encontradas: {total_fechas}')
    print(f'Total de fechas válidas: {total_fechas_validas}')


# Ruta del archivo XML
ruta_archivo_xml = "/home/richard.yabrudy.7e6/Escriptori/DADES/Richard Yabrudy/Grup 4 - XML Con Excel.xml"

# Llama a la función con la ruta a tu archivo XML
extraer_fechas_y_validar(ruta_archivo_xml)
