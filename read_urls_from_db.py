import sqlite3

# Conectar a la base de datos SQLite
conn = sqlite3.connect('auctions.db')
cursor = conn.cursor()

# Consultar las URLs desde la base de datos
cursor.execute("SELECT url FROM auctions")
urls = [row[0] for row in cursor.fetchall()]

# Cerrar la conexión con la base de datos
conn.close()

# Imprimir las URLs (opcional, solo para verificar)
print("URLs obtenidas desde la base de datos:")
for url in urls:
    print(url)

# Escribir las URLs en un archivo de texto para que el script de JavaScript las lea
with open('urls.txt', 'w') as f:
    for url in urls:
        f.write(url + '\n')
