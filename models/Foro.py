import sys
import os
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from usuario import Usuario
from database.db_connection import create_connection, close_connection

class Foro:
    def __init__(self):
        self.id_foro = None
        self.autor: Usuario = None
        self.nombre_foro: str = ""
        self.descripcion: str = ""
        self.es_privado: bool = False
        self.comentarios: List = []
        self.whitelist: List[Usuario] = []

    @classmethod
    def crear(cls, autor: Usuario, nombre: str, descripcion: str = "", privado: bool = False):
        foro = cls()
        foro.autor = autor
        foro.nombre_foro = nombre
        foro.descripcion = descripcion
        foro.es_privado = privado
        foro.guardar_bd()
        return foro

    def guardar_bd(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            if self.id_foro:
                cursor.execute(
                    "UPDATE foros SET nombre_foro=%s, descripcion=%s, es_privado=%s WHERE id_foro=%s",
                    (self.nombre_foro, self.descripcion, self.es_privado, self.id_foro)
                )
            else:
                cursor.execute(
                    "INSERT INTO foros (id_autor, nombre_foro, descripcion, es_privado) VALUES (%s, %s, %s, %s)",
                    (self.autor.id_usuario, self.nombre_foro, self.descripcion, self.es_privado)
                )
                cursor.execute("SELECT LAST_INSERT_ID();")
                self.id_foro = cursor.fetchone()[0]
            conn.commit()
            close_connection(conn)

    def cerrar_foro(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Primero eliminar de la whitelist
                cursor.execute("DELETE FROM whitelist WHERE id_foro=%s", (self.id_foro,))
                
                # Luego eliminar el foro
                cursor.execute("DELETE FROM foros WHERE id_foro=%s", (self.id_foro,))
                
                conn.commit()
                
            except Exception as e:
                conn.rollback()
                print(f"Error al cerrar el foro: {e}")
                
            finally:
                close_connection(conn)

    def agregar_comentario(self, comentario):
        self.comentarios.append(comentario)

    def obtener_comentario(self, idx: int):
        return self.comentarios[idx]

    def agregar_a_whitelist(self, usuario: Usuario):
        if usuario not in self.whitelist:
            self.whitelist.append(usuario)
    def eliminar_de_whitelist(self, usuario: Usuario):
        if usuario in self.whitelist:
            self.whitelist.remove(usuario)
    def actualizar_whitelist_bd(self):
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM whitelist_foros_privados WHERE id_foro=%s", (self.id_foro,))
            for usuario in self.whitelist:
                cursor.execute(
                    "INSERT INTO whitelist_foros_privados (id_foro, id_usuario) VALUES (%s, %s)",
                    (self.id_foro, usuario.id_usuario)
                )
            conn.commit()
            close_connection(conn)

    def puede_comentar(self, usuario: Usuario) -> bool:
        if not self.es_privado:
            return True
        return usuario in self.whitelist or usuario == self.autor

    @classmethod
    def obtener_todos(cls):
        foros = []
        from comentario import Comentario  # Import local para evitar circularidad
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_foro, id_autor, nombre_foro, descripcion, es_privado FROM foros")
            for row in cursor.fetchall():
                f = cls()
                f.id_foro = row[0]
                f.autor = Usuario.buscar_por_id(row[1])
                f.nombre_foro = row[2]
                f.descripcion = row[3]
                f.es_privado = bool(row[4])
                f.comentarios = Comentario.obtener_por_foro(f.id_foro)
                foros.append(f)
            close_connection(conn)
        return foros
