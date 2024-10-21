import os
import xml.etree.ElementTree as ET
from datetime import datetime
import json
from tqdm import tqdm
import time  # Importamos time para controlar la velocidad


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

    # Contar el total de incidencias para la barra de progreso
    total_incidencias = len(root.findall('.//ns1:Incidencia', ns))

    # Iterar sobre cada incidencia en el XML con barra de progreso
    for incidencia in tqdm(root.findall('.//ns1:Incidencia', ns), total=total_incidencias,
                           desc="Procesando incidencias"):
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

        # Simulamos un pequeño retraso para que la barra de progreso sea visible
        time.sleep(0.005)  # Ajusta este valor para cambiar la velocidad

    # Imprimir resultados
    print(f'Total de incidencias encontradas: {len(lista_todas_incidencias)}')

    # Retardamos la impresión de las incidencias válidas para que no sea tan rápida
    print(f'Total de incidencias válidas: {len(lista_incidencias_validas)}')
    time.sleep(1)  # Espera un segundo antes de mostrar las incidencias válidas

    # Mostrar las incidencias válidas lentamente
    print("\nIncidencias válidas:")
    for incidencia in lista_incidencias_validas:
        print(incidencia)
        time.sleep(0.2)  # Espera 0.2 segundos entre cada impresión

    # Guardar listas en archivos JSON
    with open('incidencias_todas.json', 'w') as f:
        json.dump(lista_todas_incidencias, f, indent=4)  # Guardar todas las incidencias

    with open('incidencias_validas.json', 'w') as f:
        json.dump(lista_incidencias_validas, f, indent=4)  # Guardar incidencias válidas

    # Imprimir la ruta donde se guardaron los archivos
    print(f'Archivos guardados en: {os.getcwd()}')


# Ruta del archivo XML
ruta_archivo_xml = "./Grup 4 - XML Con Excel.xml"

# Llama a la función
extraer_incidencias(ruta_archivo_xml)
