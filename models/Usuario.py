from database.db_connection import get_conn
from database.db_connection import create_connection, close_connection

class Usuario:
    def __init__(self, nombre, correo, contraseña, rol):
        self.__nombre = nombre
        self.__correo = correo
        self.__contraseña = contraseña
        self.__rol = rol

    # Métodos de base de datos
    def guardar_bd(self):
        """Inserta este usuario en la base de datos"""
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nombre, correo, contraseña, rol) VALUES (%s, %s, %s, %s);"
            cursor.execute(sql, (self.__nombre, self.__correo, self.__contraseña, self.__rol))
            conn.commit()
            close_connection(conn)
            print(f"[DB] Usuario '{self.__nombre}' insertado correctamente.")

    @staticmethod
    def obtener_todos():
        """Obtiene todos los usuarios desde la base de datos"""
        conn = create_connection()
        usuarios = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, correo, contraseña, rol FROM usuarios;")
            filas = cursor.fetchall()
            for fila in filas:
                u = Usuario(fila[1], fila[2], fila[3], fila[4])
                usuarios.append(u)
            close_connection(conn)
        return usuarios

    @staticmethod
    def buscar_por_correo(correo):
        """Devuelve un usuario según su correo"""
        conn = create_connection()
        usuario = None
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, correo, contraseña, rol FROM usuarios WHERE correo=%s;", (correo,))
            fila = cursor.fetchone()
            if fila:
                usuario = Usuario(fila[1], fila[2], fila[3], fila[4])
            close_connection(conn)
        return usuario

    # Información del usuario
    def mostrar_info(self):
        return f"Nombre: {self.__nombre}, Correo: {self.__correo}, Rol: {self.__rol}"

    # Setters y Getters
    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    @property
    def correo(self):
        return self.__correo
    @correo.setter
    def correo(self, nuevo_correo):
        self.__correo = nuevo_correo

    @property
    def contraseña(self):
        return self.__contraseña
    @contraseña.setter
    def contraseña(self, nueva_contraseña):
        self.__contraseña = nueva_contraseña

    @property
    def rol(self):
        return self.__rol
    @rol.setter
    def rol(self, nuevo_rol):
        self.__rol = nuevo_rol