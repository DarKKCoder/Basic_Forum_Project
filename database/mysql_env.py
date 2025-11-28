from db_connection import create_connection, close_connection

def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cultivos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_cultivo VARCHAR(100) UNIQUE NOT NULL,
                costo_cosechar VARCHAR(100) NOT NULL,
                fecha_plantacion DATE NOT NULL,
                fecha_cosecha DATE NOT NULL,
                necesita_fertilizante BOOL NOT NULL
            );
        """)
        conn.commit()
        print("Tabla 'cultivos' creada (si no existía).")
        close_connection(conn)

def insert_plant(nombre_cultivo, costo_cosechar, fecha_plantacion, fecha_cosecha, necesita_fertilizante):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO cultivos (nombre_cultivo, costo_cosechar, fecha_plantacion, fecha_cosecha, necesita_fertilizante) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(sql, (nombre_cultivo, costo_cosechar, fecha_plantacion, fecha_cosecha, necesita_fertilizante))
        conn.commit()
        print(f"Cultivo '{nombre_cultivo}' insertado correctamente.")
        close_connection(conn)

def get_all_plants():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cultivos;")
        filas = cursor.fetchall()
        print("📋 Todos los cultivos:")
        for fila in filas:
            print(fila)
        close_connection(conn)

def get_columns():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW COLUMNS FROM cultivos;")
        columnas = cursor.fetchall()
        print("Columnas de la tabla 'cultivos':")
        for col in columnas:
            print(f"- {col[0]} ({col[1]})")
        close_connection(conn)

def main():
    create_table()                 # Crear la tabla si no existe
    insert_plant("Tomate", "500", "2024-03-01", "2024-06-01", True)  # Insertar un cultivo de ejemplo
    get_all_plants()               # Mostrar todos los cultivos
    get_columns()                  # Mostrar columnas

if __name__ == "__main__":
    main()
