from database.db_connection import create_connection, close_connection

class Fecha:
    def __init__(self, dia, mes, anio, hora):
        self.__dia = dia
        self.__mes = mes
        self.__anio = anio
        self.__hora = hora  # tipo TIME en DB

    # Métodos de base de datos
    def guardar_bd(self):
        """Inserta esta fecha en la base de datos"""
        conn = create_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO fechas (dia, mes, anio, hora) VALUES (%s, %s, %s, %s);"
            cursor.execute(sql, (self.__dia, self.__mes, self.__anio, self.__hora))
            conn.commit()
            close_connection(conn)
            print(f"[DB] Fecha {self.mostrar_fecha()} guardada correctamente.")

    @staticmethod
    def obtener_todas():
        """Devuelve todas las fechas de la base de datos"""
        conn = create_connection()
        fechas = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_fecha, dia, mes, anio, hora FROM fechas;")
            filas = cursor.fetchall()
            for fila in filas:
                f = Fecha(fila[1], fila[2], fila[3], str(fila[4]))
                fechas.append(f)
            close_connection(conn)
        return fechas

    # Mostrar fecha
    def mostrar_fecha(self):
        return f"{self.__dia:02d}/{self.__mes:02d}/{self.__anio} {self.__hora}"

    # Setters y Getters
    @property
    def dia(self):
        return self.__dia
    @dia.setter
    def dia(self, nuevo_dia):
        self.__dia = nuevo_dia

    @property
    def mes(self):
        return self.__mes
    @mes.setter
    def mes(self, nuevo_mes):
        self.__mes = nuevo_mes

    @property
    def anio(self):
        return self.__anio
    @anio.setter
    def anio(self, nuevo_anio):
        self.__anio = nuevo_anio

    @property
    def hora(self):
        return self.__hora
    @hora.setter
    def hora(self, nueva_hora):
        self.__hora = nueva_hora