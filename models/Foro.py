# models/foro.py
from database.db_connection import create_connection, close_connection
from usuario import Usuario
from comentario import Comentario

class Foro:
    def __init__(self, autor: Usuario, nombre_foro="General", descripcion="Foro de discusión general", es_privado=False):
        if not isinstance(autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.") 
        self.__autor = autor
        self.__nombre_foro = nombre_foro
        self.__descripcion = descripcion
        self.__comentarios = []  # Lista de comentarios en memoria
        self.__es_privado = es_privado
        self.__id_foro = None  # ID en la base de datos
        self.guardar_bd()  # Insertar en DB al crear el foro

    # =========================
    # BASE DE DATOS
    # =========================
    def guardar_bd(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO foros (id_autor, nombre_foro, descripcion, es_privado)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(sql, (self.__autor.id_usuario, self.__nombre_foro, self.__descripcion, self.__es_privado))
            conn.commit()
            # Recuperar el id_foro generado automáticamente
            cursor.execute("SELECT LAST_INSERT_ID();")
            self.__id_foro = cursor.fetchone()[0]
            close_connection(conn)
            print(f"[DB] Foro '{self.__nombre_foro}' creado con ID {self.__id_foro}.")

    def agregar_comentario(self, comentario: Comentario):
        if not isinstance(comentario, Comentario):
            raise ValueError("El comentario debe ser una instancia de Comentario.")
        self.__comentarios.append(comentario)
        comentario.guardar_bd(self.__id_foro)  # Guardar en la DB asociando id_foro

    def obtener_comentario(self, indice):
        if 0 <= indice < len(self.__comentarios):
            return self.__comentarios[indice]
        return None

    def mostrar_comentarios(self):
        print(f"Comentarios del foro '{self.__nombre_foro}':")
        for i, comentario in enumerate(self.__comentarios, 1):
            print(f"{i}. {comentario.mostrar_comentario()}")

    def cerrar_foro(self):
        """Limpia manualmente los comentarios y desconecta referencias."""
        for comentario in self.__comentarios:
            comentario.borrar()  # Debería borrar también de la DB
        self.__comentarios.clear()
        print(f"Foro '{self.__nombre_foro}' cerrado correctamente.")

    # =========================
    # PROPIEDADES
    # =========================
    @property
    def id_foro(self):
        return self.__id_foro

    @property
    def autor(self):
        return self.__autor

    @property
    def comentarios(self):
        return self.__comentarios

    @property
    def nombre_foro(self):
        return self.__nombre_foro

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def es_privado(self):
        return self.__es_privado

    @comentarios.setter
    def comentarios(self, nueva_lista):
        self.__comentarios = nueva_lista

    @nombre_foro.setter
    def nombre_foro(self, nuevo_nombre):
        self.__nombre_foro = nuevo_nombre

    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        self.__descripcion = nueva_descripcion

    @es_privado.setter
    def es_privado(self, valor):
        self.__es_privado = valor
