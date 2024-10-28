import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime
from tqdm import tqdm
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, init, Style
import os

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
    # Verificar que el archivo existe
    if not os.path.exists(xml_file):
        console.print(Panel(Text("Error: El archivo XML no existe o la ruta es incorrecta.", justify="center"),
                            title="Archivo no encontrado", style="bold red", expand=False))
        return

    try:
        # Cargar y parsear el archivo XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError:
        console.print(Panel(Text("Error: El archivo XML no es válido o está corrupto.", justify="center"),
                            title="Error de XML", style="bold red", expand=False))
        return

    # Espacio de nombres en XML
    ns = {'ns1': 'http://www.exemple.com/IncidenciasGrup4'}

    # Inicializar listas
    lista_todas_incidencias = []  # Lista para almacenar todas las incidencias
    lista_incidencias_validas = []  # Lista para almacenar las incidencias válidas
    lista_incidencias_erroneas = []  # Lista para almacenar las incidencias erróneas
    incidencias_molt_urgent = 0  # Contador para incidencias "Molt Urgent"

    # Obtener la fecha actual
    fecha_actual = datetime.today().date()
    fecha_septiembre_actual = datetime(year=fecha_actual.year, month=9, day=1).date()

    # Contar el total de incidencias para la barra de progreso
    total_incidencias = len(root.findall('.//ns1:Incidencia', ns))
    desc = f"{Fore.GREEN}Procesando incidencias"

    with tqdm(total=total_incidencias, desc=desc,
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed} < {remaining}, {rate_fmt}]") as pbar:
        for incidencia in root.findall('.//ns1:Incidencia', ns):
            # Extraer todos los elementos de la incidencia
            incidencia_data = {}
            for elemento in incidencia:
                tag_name = elemento.tag.split('}')[1]  # Obtener el nombre de la etiqueta sin el namespace
                incidencia_data[tag_name] = elemento.text
            lista_todas_incidencias.append(incidencia_data)

            # Validar la fecha de la incidencia
            if 'DataIncidencia' in incidencia_data and validar_fecha(incidencia_data['DataIncidencia']):
                fecha_incidencia = datetime.strptime(incidencia_data['DataIncidencia'], "%Y-%m-%d").date()
                if fecha_septiembre_actual <= fecha_incidencia <= fecha_actual:
                    lista_incidencias_validas.append(incidencia_data)
                    if incidencia_data.get('NivellUrgencia') == "Molt Urgent":
                        incidencias_molt_urgent += 1
                else:
                    lista_incidencias_erroneas.append(incidencia_data)
            else:
                lista_incidencias_erroneas.append(incidencia_data)
            time.sleep(0.005)
            pbar.update(1)  # Actualiza la barra de progreso

    # Guardar incidencias en archivos JSON
    nombre_archivo_json_validas = f'incidencias_validas_{fecha_actual}.json'
    nombre_archivo_json_erroneas = f'incidencias_erroneas_{fecha_actual}.json'
    with open(nombre_archivo_json_validas, 'w', encoding='utf-8') as f:
        json.dump(lista_incidencias_validas, f, ensure_ascii=False, indent=4)
    with open(nombre_archivo_json_erroneas, 'w', encoding='utf-8') as f:
        json.dump(lista_incidencias_erroneas, f, ensure_ascii=False, indent=4)

    # Calcular el porcentaje de incidencias "Molt Urgent"
    porcentaje_molt_urgent = (
                incidencias_molt_urgent / len(lista_incidencias_validas) * 100) if lista_incidencias_validas else 0

    # Mostrar el resumen en consola
    console.print(Panel(Text(f"Total de incidencias encontradas: {len(lista_todas_incidencias)}\n"
                             f"Total de incidencias válidas: {len(lista_incidencias_validas)}\n"
                             f"Total de incidencias erróneas: {len(lista_incidencias_erroneas)}\n"
                             f"Porcentaje de incidencias 'Molt Urgent': {porcentaje_molt_urgent:.2f}%",
                             justify="center"), title="Resumen de Incidencias", expand=False))

    # Guardar estadísticas
    estadisticas = {
        "total_incidencias": len(lista_todas_incidencias),
        "incidencias_validas": len(lista_incidencias_validas),
        "incidencias_erroneas": len(lista_incidencias_erroneas),
        "incidencias_molt_urgent": incidencias_molt_urgent,
        "porcentaje_molt_urgent": porcentaje_molt_urgent,
        "fecha_procesamiento": str(fecha_actual)
    }
    with open(f'estadisticas_{fecha_actual}.json', 'w', encoding='utf-8') as f:
        json.dump(estadisticas, f, ensure_ascii=False, indent=4)

# Ruta del archivo XML
ruta_archivo_xml = "./incidencias.xml"

# Llama a la función con la ruta a tu archivo XML
extraer_incidencias(ruta_archivo_xml)
