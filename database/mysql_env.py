from db_connection import create_connection, close_connection


# ============================
#  TABLA: USUARIOS
# ============================
def create_table_usuarios():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) UNIQUE NOT NULL,
                contraseña VARCHAR(255) NOT NULL,
                rol VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        print("Tabla 'usuarios' creada (si no existía).")
        close_connection(conn)

def insert_usuario(nombre, correo, contraseña, rol):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombre, correo, contraseña, rol) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (nombre, correo, contraseña, rol))
        conn.commit()
        print(f"Usuario '{nombre}' insertado correctamente.")
        close_connection(conn)



# ============================
#  TABLA: FOROS
# ============================
def create_table_foros():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foros (
                id_foro INT AUTO_INCREMENT PRIMARY KEY,
                id_autor INT NOT NULL,
                nombre_foro VARCHAR(100) DEFAULT 'General',
                descripcion TEXT,
                es_privado BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (id_autor) REFERENCES usuarios(id_usuario)
            );
        """)
        conn.commit()
        print("Tabla 'foros' creada (si no existía).")
        close_connection(conn)

def insert_foro(id_autor, nombre_foro, descripcion, es_privado=False):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO foros (id_autor, nombre_foro, descripcion, es_privado) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (id_autor, nombre_foro, descripcion, es_privado))
        conn.commit()
        print(f"Foro '{nombre_foro}' insertado correctamente.")
        close_connection(conn)



# ============================
#  TABLA: FECHAS
# ============================
def create_table_fechas():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fechas (
                id_fecha INT AUTO_INCREMENT PRIMARY KEY,
                dia INT NOT NULL,
                mes INT NOT NULL,
                anio INT NOT NULL,
                hora TIME
            );
        """)
        conn.commit()
        print("Tabla 'fechas' creada (si no existía).")
        close_connection(conn)

def insert_fecha(dia, mes, anio, hora):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO fechas (dia, mes, anio, hora) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (dia, mes, anio, hora))
        conn.commit()
        print("Fecha insertada correctamente.")
        close_connection(conn)



# ============================
#  TABLA: COMENTARIOS
# ============================
def create_table_comentarios():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id_comentario INT AUTO_INCREMENT PRIMARY KEY,
                id_autor INT NOT NULL,
                id_foro INT NOT NULL,
                contenido TEXT NOT NULL,
                id_fecha INT NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (id_autor) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_foro) REFERENCES foros(id_foro),
                FOREIGN KEY (id_fecha) REFERENCES fechas(id_fecha)
            );
        """)
        conn.commit()
        print("Tabla 'comentarios' creada (si no existía).")
        close_connection(conn)

def insert_comentario(id_autor, id_foro, contenido, id_fecha):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO comentarios (id_autor, id_foro, contenido, id_fecha) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql, (id_autor, id_foro, contenido, id_fecha))
        conn.commit()
        print("Comentario insertado correctamente.")
        close_connection(conn)



# ============================
#  TABLA: WHITELIST FOROS PRIVADOS
# ============================
def create_table_whitelist():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS whitelist_foros_privados (
                id_whitelist INT AUTO_INCREMENT PRIMARY KEY,
                id_foro INT NOT NULL,
                id_usuario INT NOT NULL,
                FOREIGN KEY (id_foro) REFERENCES foros(id_foro),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
        conn.commit()
        print("Tabla 'whitelist_foros_privados' creada (si no existía).")
        close_connection(conn)

def insert_whitelist(id_foro, id_usuario):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO whitelist_foros_privados (id_foro, id_usuario) VALUES (%s, %s);"
        cursor.execute(sql, (id_foro, id_usuario))
        conn.commit()
        print(f"Whitelist: acceso dado → Foro {id_foro}, Usuario {id_usuario}")
        close_connection(conn)



# ============================
#  MAIN
# ============================
def main():
    print("\n=== CREANDO TABLAS ===")
    create_table_usuarios()
    create_table_foros()
    create_table_fechas()
    create_table_comentarios()
    create_table_whitelist()

    print("\n=== INSERTANDO DATOS DE PRUEBA ===")

    # Usuarios
    insert_usuario("Oscar", "oscar@example.com", "1234", "admin")
    insert_usuario("María", "maria@example.com", "abcd", "usuario")
    insert_usuario("Luis", "luis@example.com", "xyz", "usuario")

    # Foros (públicos y privados)
    insert_foro(1, "Foro General", "Bienvenido al foro principal.", 0)
    insert_foro(2, "Foro de Mascotas", "Habla de tus animales favoritos.", 0)
    insert_foro(3, "Staff Interno", "Foro privado del personal.", 1)

    # Whitelist del foro privado (id_foro = 3)
    insert_whitelist(3, 1)
    insert_whitelist(3, 2)
    insert_whitelist(3, 3)

    # Fechas
    insert_fecha(10, 2, 2025, "12:45:00")
    insert_fecha(11, 2, 2025, "13:20:00")

    # Comentarios
    insert_comentario(1, 1, "Hola, este es mi primer comentario.", 1)
    insert_comentario(2, 2, "Los animales son increíbles!", 2)
    insert_comentario(3, 3, "Información solo del staff.", 1)

    print("\TEST COMPLETO FINALIZADO — REVISA TU BASE DE DATOS")


if __name__ == "__main__":
    main()
