class Fecha:
    def __init__(self, dia, mes, anio, hora):
        self.dia = dia
        self.mes = mes
        self.anio = anio
        self.__hora = hora

    #Métodos
    def mostrar_fecha(self):
        return f"{self.dia}/{self.mes}/{self.anio}"
    
    #Setters y Getters
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