import xml.etree.ElementTree as ET
from datetime import datetime


# Función para cargar y parsear el XML
def cargar_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root


# Función para validar si una incidencia está en el rango de fechas válido
def es_fecha_valida(fecha_str):
    # Formato de la fecha, puedes ajustarlo según tu XML
    formato_fecha = "%Y-%m-%d"

    # Convertimos la fecha de la incidencia a un objeto datetime
    fecha_incidencia = datetime.strptime(fecha_str, formato_fecha)

    # Obtenemos la fecha actual del sistema
    fecha_actual = datetime.now()

    # Definimos el 1 de septiembre del año actual
    inicio_septiembre = datetime(fecha_actual.year, 9, 1)

    # Comprobamos si la fecha de la incidencia es válida
    if inicio_septiembre <= fecha_incidencia <= fecha_actual:
        return True
    else:
        return False


# Función para filtrar incidencias por fecha
def filtrar_incidencias(root):
    incidencias_ok = []

    for incidencia in root.findall('incidencia'):
        fecha = incidencia.find('fecha').text
        if es_fecha_valida(fecha):
            incidencias_ok.append(incidencia)

    return incidencias_ok


# Función para procesar las incidencias válidas y mostrar información
def procesar_incidencias_ok(incidencias_ok):
    print(f"Total de incidencias válidas: {len(incidencias_ok)}")

    # Imprimir alguna información relevante de las incidencias válidas
    for incidencia in incidencias_ok:
        id_incidencia = incidencia.find('id').text
        fecha = incidencia.find('fecha').text
        descripcion = incidencia.find('descripcion').text
        print(f"ID: {id_incidencia}, Fecha: {fecha}, Descripción: {descripcion}")


# Programa principal
def main():
    # Cargar el fichero XML (cambia la ruta al archivo correspondiente)
    file_path = 'incidencias.xml'
    root = cargar_xml(file_path)

    # Filtrar incidencias por fecha
    incidencias_ok = filtrar_incidencias(root)

    # Procesar y mostrar las incidencias válidas
    procesar_incidencias_ok(incidencias_ok)


if __name__ == "__main__":
    main()
