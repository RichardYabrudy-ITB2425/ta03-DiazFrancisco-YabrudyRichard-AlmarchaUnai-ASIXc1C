import xml.etree.ElementTree as ET
from datetime import datetime
import json
from tqdm import tqdm
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, Style, init

# Inicializar colorama y consola Rich
init(autoreset=True)
console = Console()


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
    desc = f"{Fore.GREEN}Procesando incidencias"
    with tqdm(total=total_incidencias, desc=desc,
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed} < {remaining}, {rate_fmt}]") as pbar:

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

            # Simulamos un pequeño retraso para que la barra de progreso sea visible
            time.sleep(0.005)
            pbar.update(1)  # Actualiza la barra de progreso



    # Guardar listas en archivos JSON
    with open('incidencias_todas.json', 'w') as f:
        json.dump(lista_todas_incidencias, f, indent=4)  # Guardar todas las incidencias

    with open('incidencias_validas.json', 'w') as f:
        json.dump(lista_incidencias_validas, f, indent=4)  # Guardar incidencias válidas

    # Mostrar un banner en la consola
    banner_text = Text(f"Total de incidencias encontradas: {len(lista_todas_incidencias)}\n"
                       f"Total de incidencias válidas: {len(lista_incidencias_validas)}",
                       justify="center")
    console.print(Panel(banner_text, title="Resumen de Incidencias", expand=False))


# Ruta del archivo XML
ruta_archivo_xml = "./Grup 4 - XML Con Excel.xml"

# Llama a la función
extraer_incidencias(ruta_archivo_xml)
