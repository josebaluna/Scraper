import subprocess
import json
import sqlite3
import time

# Función para ejecutar el script de Node.js y capturar los datos
def run_node_script():
    try:
        # Ejecutar el script de Node.js y capturar la salida
        result = subprocess.run(['node', 'scrape_boe.js'], capture_output=True, text=True)
        print("stdout:", result.stdout)  # Agregar esta línea para imprimir la salida estándar
        print("stderr:", result.stderr)  # Agregar esta línea para imprimir la salida de error
        if result.returncode == 0:
            with open('all_auctions.json', 'r', encoding='utf-8') as file:
                auctions = json.load(file)
            return auctions
        else:
            print(f"Error al ejecutar el script de Node.js: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error al ejecutar el script de Node.js: {e}")
        return []

# Función para guardar los datos en la base de datos
def save_to_db(auctions):
    if not auctions:
        print("No se encontraron subastas para guardar.")
        return

    try:
        conn = sqlite3.connect('auctions.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS auctions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                court TEXT,
                case_number TEXT,
                status TEXT,
                description TEXT,
                url TEXT
            )
        ''')

        for auction in auctions:
            # Verificar si el registro tiene todos los campos necesarios
            if 'title' in auction:
                # Verificar si el registro ya existe
                c.execute('''
                    SELECT 1 FROM auctions WHERE title = ?
                ''', (auction['title'],))
                if c.fetchone() is None:
                    # Si no existe, insertarlo
                    c.execute('''
                        INSERT INTO auctions (title, court, case_number, status, description, url) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        auction['title'],
                        auction.get('court', ''),
                        auction.get('caseNumber', ''),
                        auction.get('status', ''),
                        auction.get('description', ''),
                        auction.get('detailUrl', '')
                    ))
                    print(f"Subasta {auction['title']} se ha guardado en la base de datos.")
                else:
                    print(f"Subasta {auction['title']} ya existe en la base de datos.")
            else:
                print(f"Registro incompleto o sin 'title'. No se puede insertar en la base de datos: {auction}")

        conn.commit()
        time.sleep(0.1)  # Retraso de 0.1 segundos entre inserciones

    except sqlite3.Error as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    auctions = run_node_script()

    # Mostrar las subastas encontradas
    if auctions:
        print(f"Se encontraron {len(auctions)} subastas.")
        for auction in auctions:
            print(auction)
        # Guardar los datos en la base de datos
        save_to_db(auctions)
        print("Datos guardados en la base de datos.")
    else:
        print("No se encontraron subastas para guardar.")
