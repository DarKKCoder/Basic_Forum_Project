# models/comentario.py
from fecha import Fecha
from usuario import Usuario
from foro import Foro
from database.db_connection import create_connection, close_connection
from datetime import date

class Comentario:
    def __init__(self, autor: Usuario, contenido: str, foro: Foro):
        if not isinstance(autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.")
        if not isinstance(foro, Foro):
            raise ValueError("El foro debe ser una instancia de Foro.")

        self.__autor = autor
        self.__contenido = contenido
        self.__fecha = Fecha(date.today().day, date.today().month, date.today().year, "00:00:00")
        self.__foro = foro
        self.__respuestas = []
        self.__activo = True
        self.__id_comentario = None

        self.guardar_bd()  # Inserta el comentario en la DB

    # =========================
    # BASE DE DATOS
    # =========================
    def guardar_bd(self, id_foro=None):
        id_foro = id_foro or self.__foro.id_foro
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            # Insertar fecha primero
            cursor.execute(
                "INSERT INTO fechas (dia, mes, anio, hora) VALUES (%s, %s, %s, %s);",
                (self.__fecha.dia, self.__fecha.mes, self.__fecha.anio, self.__fecha.hora)
            )
            cursor.execute("SELECT LAST_INSERT_ID();")
            id_fecha = cursor.fetchone()[0]

            # Insertar comentario
            sql = """
                INSERT INTO comentarios (id_autor, id_foro, contenido, id_fecha, activo)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(sql, (self.__autor.id_usuario, id_foro, self.__contenido, id_fecha, self.__activo))
            cursor.execute("SELECT LAST_INSERT_ID();")
            self.__id_comentario = cursor.fetchone()[0]

            conn.commit()
            close_connection(conn)
            print(f"[DB] Comentario de '{self.__autor.nombre}' agregado al foro '{self.__foro.nombre_foro}' con ID {self.__id_comentario}.")

    # =========================
    # MÉTODOS PRINCIPALES
    # =========================
    def mostrar_comentario(self):
        return f"{self.__autor.nombre} dice: {self.__contenido}" if self.__activo else f"{self.__autor.nombre} ha eliminado este comentario."

    def borrar(self):
        if self.__activo:
            self.__contenido = "[comentario eliminado]"
            self.__activo = False
            self.actualizar_bd()

        for resp in self.__respuestas:
            resp.borrar()
        self.limpiar_respuestas_eliminadas()

    def editar_comentario(self, nuevo_contenido):
        if self.__activo:
            self.__contenido = nuevo_contenido
            self.actualizar_bd()
            return True
        return False

    def agregar_respuesta(self, respuesta):
        self.__respuestas.append(respuesta)
        if self.__id_comentario:
            respuesta.guardar_bd(id_foro=self.__foro.id_foro)  # Guardar respuesta vinculada

    def mostrar_respuestas(self, nivel=1):
        indent = "  " * nivel
        for resp in self.__respuestas:
            print(f"{indent}{resp.mostrar_comentario()}")
            resp.mostrar_respuestas(nivel + 1)

    def limpiar_respuestas_eliminadas(self):
        self.__respuestas = [r for r in self.__respuestas if r.esta_activo()]
        for r in self.__respuestas:
            r.limpiar_respuestas_eliminadas()

    def esta_activo(self):
        return self.__activo

    # =========================
    # ACTUALIZACIÓN EN BD
    # =========================
    def actualizar_bd(self):
        if not self.__id_comentario:
            return
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE comentarios SET contenido=%s, activo=%s WHERE id_comentario=%s;",
                (self.__contenido, self.__activo, self.__id_comentario)
            )
            conn.commit()
            close_connection(conn)
            print(f"[DB] Comentario ID {self.__id_comentario} actualizado.")

    # =========================
    # PROPIEDADES
    # =========================
    @property
    def autor(self):
        return self.__autor

    @property
    def contenido(self):
        return self.__contenido

    @contenido.setter
    def contenido(self, nuevo_contenido):
        self.__contenido = nuevo_contenido
        self.actualizar_bd()

    @property
    def fecha(self):
        return self.__fecha

    @property
    def foro(self):
        return self.__foro

    @property
    def id_comentario(self):
        return self.__id_comentario

    @property
    def cantidad_respuestas(self):
        return len(self.__respuestas)
