# Scraper
Este proyecto realiza el scraping de información publicada en el BOE desde un archivo JSON previamente procesado y la guarda en una base de datos SQLite.

📦 Funcionalidades
🔍 Extracción de datos
Carga un archivo all_details.json que contiene la información estructurada de múltiples subastas.

Identifica automáticamente los datos generales de cada subasta y los distintos lotes asociados a ella.

🗃️ Base de datos SQLite
Crea dos tablas principales:

details: contiene los datos generales de cada subasta (ej. identificador, tipo, fechas, dirección, valores, etc.).

lots: contiene la información específica de cada lote de subasta (ej. descripción, valor, referencia catastral, cargas, etc.).

Relación uno-a-muchos entre details y lots, usando auction_id como clave foránea.

🛠️ Inserción de datos
Inserta la información de cada subasta y sus respectivos lotes en la base de datos auctions.db.

Verifica duplicados mediante la URL de la subasta antes de insertar.

Manejo de errores robusto durante la inserción.

🗂️ Estructura esperada del JSON
Ejemplo de entrada:

json
Copiar
Editar
{
  "url": "https://subastas.boe.es/...",
  "Identificador": "SUB-123456",
  "Lote_1": {
    "Descripción": "LOTE 1: URBANA. Plaza de aparcamiento...",
    "Valor Subasta": "12.553,20 €",
    "Referencia catastral": "3349830XH6034N0070PD",
    ...
  },
  "Lote_2": {
    "Descripción": "LOTE 2: Vivienda en planta baja...",
    ...
  }
}
🧰 Cómo usar
Asegúrate de tener Python 3 instalado.

Coloca el archivo all_details.json en el mismo directorio que el script.

Ejecuta el script principal:

bash
Copiar
Editar
python scraper.py
Esto creará (si no existe) una base de datos auctions.db con las tablas details y lots, e insertará todos los datos desde el archivo JSON.

🛑 Requisitos
Python 3.x

Módulos estándar:

json

sqlite3

📁 Archivos del proyecto
scraper.py: script principal.

all_details.json: archivo con los datos a importar.

auctions.db: base de datos SQLite generada.
