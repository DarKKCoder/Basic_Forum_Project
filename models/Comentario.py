import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from usuario import Usuario
from fecha import Fecha
from database.db_connection import create_connection, close_connection

class Comentario:
    def __init__(self, autor: Usuario, foro, contenido: str, fecha: Fecha):
        self.autor = autor
        self.foro = foro
        self.contenido = contenido
        self.fecha = fecha  # Debe ser un objeto Fecha
        self.id_comentario = None

    def mostrar_comentario(self):
        return f"{self.autor.nombre}: {self.contenido}"

    def guardar_bd(self):
        """Inserta el comentario en la base de datos con su fecha asociada"""
        if not self.fecha.id_fecha:
            raise ValueError("El objeto Fecha debe estar guardado en la DB antes de guardar el Comentario")
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO comentarios (id_autor, id_foro, id_fecha, contenido) VALUES (%s, %s, %s, %s)",
                (
                    self.autor.id_usuario,
                    self.foro.id_foro if self.foro else None,
                    self.fecha.id_fecha,
                    self.contenido
                )
            )
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID();")
            self.id_comentario = cursor.fetchone()[0]
            close_connection(conn)

    def editar(self, nuevo_contenido: str, usuario_actual: Usuario):
        """Solo permite editar si es el autor"""
        if self.autor.id_usuario != usuario_actual.id_usuario:
            raise PermissionError("No puedes editar un comentario que no es tuyo")
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE comentarios SET contenido=%s WHERE id_comentario=%s",
                (nuevo_contenido, self.id_comentario)
            )
            conn.commit()
            self.contenido = nuevo_contenido
            close_connection(conn)

    def borrar(self, usuario_actual: Usuario):
        """Solo permite borrar si es el autor"""
        if self.autor.id_usuario != usuario_actual.id_usuario and usuario_actual.rol != "Admin":
            raise PermissionError("No puedes borrar un comentario que no es tuyo")
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM comentarios WHERE id_comentario=%s",
                (self.id_comentario,)
            )
            conn.commit()
            close_connection(conn)

    @classmethod
    def obtener_por_foro(cls, id_foro, foro_obj=None):
        """Retorna lista de Comentarios, enlazando al objeto Foro si se pasa"""
        comentarios = []
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT c.id_comentario, c.id_autor, c.id_fecha, c.contenido, f.dia, f.mes, f.anio, f.hora "
                "FROM comentarios c "
                "JOIN fechas f ON c.id_fecha = f.id_fecha "
                "WHERE c.id_foro=%s",
                (id_foro,)
            )
            for row in cursor.fetchall():
                fecha = Fecha(row[4], row[5], row[6], str(row[7]))
                fecha._Fecha__id_fecha = row[2]  # asignamos id_fecha
                c = cls(
                    autor=Usuario.buscar_por_id(row[1]),
                    foro=foro_obj,
                    contenido=row[3],
                    fecha=fecha
                )
                c.id_comentario = row[0]
                comentarios.append(c)
            close_connection(conn)
        return comentarios
