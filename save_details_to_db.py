import json
import sqlite3

def create_tables(c):
    c.execute('''
        CREATE TABLE IF NOT EXISTS details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                Identificador TEXT,
                Tipo_de_subasta TEXT,
                Cuenta_expediente TEXT,
                Fecha_de_inicio TEXT,
                Fecha_de_conclusion TEXT,
                Cantidad_reclamada TEXT,
                Lotes INTEGER,
                Forma_adjudicacion TEXT,
                Anuncio_BOE TEXT,
                Valor_subasta TEXT,
                Tasacion TEXT,
                Puja_minima TEXT,
                Tramos_entre_pujas TEXT,
                Importe_deposito TEXT,
                Codigo TEXT,
                Descripcion TEXT,
                Direccion TEXT,
                Telefono TEXT,
                Fax TEXT,
                Correo_electronico TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_id INTEGER,
            lot_number INTEGER,
            title TEXT,
            description TEXT,
            idufir TEXT,
            address TEXT,
            codigo_postal TEXT,
            localidad TEXT,
            provincia TEXT,
            valor_subasta TEXT,
            valor_tasacion TEXT,
            importe_deposito TEXT,
            puja_minima TEXT,
            tramos_entre_pujas TEXT,
            referencia_catastral TEXT,
            situacion_posesoria TEXT,
            visitable TEXT,
            cargas TEXT,
            inscripcion_registral TEXT,
            informacion_adicional TEXT,
            FOREIGN KEY (auction_id) REFERENCES details(id)
        )
    ''')

def insert_data(c, all_details):
    for auction in all_details:
        try:
            # Insertar subasta
            c.execute('''
                INSERT OR IGNORE INTO details (
                    url, Identificador, Tipo_de_subasta, Cuenta_expediente, Fecha_de_inicio,
                    Fecha_de_conclusion, Cantidad_reclamada, Lotes, Forma_adjudicacion,
                    Anuncio_BOE, Valor_subasta, Tasacion, Puja_minima, Tramos_entre_pujas,
                    Importe_deposito, Codigo, Descripcion, Direccion, Telefono, Fax,
                    Correo_electronico
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                auction.get('url'), auction.get('Identificador'), auction.get('Tipo de subasta'),
                auction.get('Cuenta expediente'), auction.get('Fecha de inicio'), auction.get('Fecha de conclusión'),
                auction.get('Cantidad reclamada'), auction.get('Lotes'), auction.get('Forma adjudicación'),
                auction.get('Anuncio BOE'), auction.get('Valor subasta'), auction.get('Tasación'),
                auction.get('Puja mínima'), auction.get('Tramos entre pujas'), auction.get('Importe del depósito'),
                auction.get('Código'), auction.get('Descripción'), auction.get('Dirección'), auction.get('Teléfono'),
                auction.get('Fax'), auction.get('Correo electrónico') 
                ))

            c.execute('''
                SELECT id FROM details WHERE url = ?
            ''', (auction.get('url'),))
            auction_id = c.fetchone()[0]

            for key, lot_data in auction.items():
                if key.startswith('Lote_'):
                    lot_number = int(key.split('_')[1])
                    # Insertar lote
                    c.execute('''
                            INSERT INTO lots (auction_id, lot_number, title, description, idufir, address, codigo_postal, localidad,
                                            provincia, valor_subasta, valor_tasacion, importe_deposito, puja_minima, tramos_entre_pujas,
                                            referencia_catastral, situacion_posesoria, visitable, cargas,
                                            inscripcion_registral, informacion_adicional)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            auction_id, lot_number,
                            lot_data.get('Descripción', ''),
                            lot_data.get('Descripción', ''),  # Asumiendo que 'Descripción' es equivalente a 'description'
                            lot_data.get('IDUFIR', ''),
                            lot_data.get('Dirección', ''),
                            lot_data.get('Código Postal', ''),
                            lot_data.get('Localidad', ''),
                            lot_data.get('Provincia', ''),
                            lot_data.get('Valor Subasta', ''),
                            lot_data.get('Valor de tasación', ''),
                            lot_data.get('Importe del depósito', ''),
                            lot_data.get('Puja mínima', ''),
                            lot_data.get('Tramos entre pujas', ''),
                            lot_data.get('Referencia catastral', ''),
                            lot_data.get('Situación posesoria', ''),
                            lot_data.get('Visitable', ''),
                            lot_data.get('Cargas', ''),
                            lot_data.get('Inscripción registral', ''),
                            lot_data.get('Información adicional', '')
                        ))
        except Exception as e:
            print(f"Error inserting data for auction {auction.get('url', '')}: {e}")

def main():
    # Conectar a la base de datos
    conn = sqlite3.connect('auctions.db')
    c = conn.cursor()

    # Crear las tablas
    create_tables(c)

    # Leer los datos del archivo JSON
    try:
        with open('all_details.json', 'r', encoding='utf-8') as f:
            all_details = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Insertar los datos en las tablas
    insert_data(c, all_details)

    # Confirmar y cerrar la conexión
    conn.commit()
    conn.close()

    print("Datos insertados correctamente en la base de datos.")

if __name__ == '__main__':
    main()
