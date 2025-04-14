import json
import sqlite3

# Función para cargar los datos desde el archivo JSON
def load_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Función para crear la tabla subastas
def create_subastas_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subastas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            Identificador TEXT,
            Tipo_subasta TEXT,
            Cuenta_expediente TEXT,
            Fecha_inicio TEXT,
            Fecha_conclusion TEXT,
            Cantidad_reclamada TEXT,
            Lotes TEXT,
            Forma_adjudicacion TEXT,
            Anuncio_BOE TEXT,
            Valor_subasta TEXT,
            Tasacion TEXT,
            Puja_minima TEXT,
            Tramos_pujas TEXT,
            Importe_deposito TEXT,
            Codigo TEXT,
            Descripcion TEXT,
            Direccion TEXT,
            Telefono TEXT,
            Fax TEXT,
            Correo_electronico TEXT
        )
    ''')
    conn.commit()

# Función para insertar datos en la tabla subastas
def insert_data_into_subastas(conn, data):
    cursor = conn.cursor()
    for auction in data:
        try:
            cursor.execute('''
                INSERT INTO subastas (
                    url, Identificador, Tipo_subasta, Cuenta_expediente,
                    Fecha_inicio, Fecha_conclusion, Cantidad_reclamada,
                    Lotes, Forma_adjudicacion, Anuncio_BOE,
                    Valor_subasta, Tasacion, Puja_minima,
                    Tramos_pujas, Importe_deposito, Codigo,
                    Descripcion, Direccion, Telefono,
                    Fax, Correo_electronico
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                auction['url'],
                auction['Identificador'],
                auction['Tipo de subasta'],
                auction.get('Cuenta expediente', ''),
                auction['Fecha de inicio'],
                auction['Fecha de conclusión'],
                auction.get('Cantidad reclamada', ''),
                auction['Lotes'],
                auction.get('Forma adjudicación', ''),
                auction.get('Anuncio BOE', ''),
                auction.get('Valor subasta', ''),
                auction.get('Tasación', ''),
                auction.get('Puja mínima', ''),
                auction.get('Tramos entre pujas', ''),
                auction.get('Importe del depósito', ''),
                auction.get('Código', ''),
                auction['Descripción'],
                auction.get('Dirección', ''),
                auction.get('Teléfono', ''),
                auction.get('Fax', ''),
                auction.get('Correo electrónico', '')
            ))
            conn.commit()
            print(f"Datos de la subasta {auction['Identificador']} insertados correctamente.")
        except sqlite3.Error as e:
            print(f"Error al insertar datos en la tabla subastas: {e}")

# Función principal para ejecutar el proceso
def main():
    try:
        conn = sqlite3.connect('auctions.db')
        create_subastas_table(conn)
        data = load_data_from_json('all_details.json')
        insert_data_into_subastas(conn, data)
    except sqlite3.Error as e:
        print(f"Error al operar con la base de datos SQLite: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
