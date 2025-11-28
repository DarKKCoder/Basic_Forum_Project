from fecha import Fecha
from datetime import date
from usuario import Usuario
from foro import Foro

class Comentario:
    def __init__(self, autor:Usuario, contenido, foro:Foro):
        if not isinstance(autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.")
        self.__autor = autor
        self.__contenido = contenido
        self.__fecha = Fecha(date.today().day, date.today().month, date.today().year) #Ejemplo de composición
        if not isinstance(foro, Foro):
            raise ValueError("El foro debe ser una instancia de Foro.")
        self.__foro = foro
        self.__respuestas = []
        self.__activo = True  # Control de estado del comentario (activo/eliminado)
    
    #Métodos
    def mostrar_comentario(self):
        if not self.__activo:
            return f"{self.__autor.nombre} ha eliminado este comentario."
        return f"{self.__autor.nombre} dice: {self.__contenido}"
    def borrar(self):
        """Borrado lógico"""
        if self.__activo:
            self.__contenido = "[comentario eliminado]"
            self.__activo = False
        for resp in self.__respuestas:
            resp.borrar()
        self.limpiar_respuestas_eliminadas()
    def __del__(self):
        """Destructor de seguridad (no siempre garantizado)."""
        try:
            print(f"Destruyendo comentario de {self.__autor.nombre}...")
            self.borrar()
            self.__autor = None
            self.__foro = None # Desconectar referencias
            self.__respuestas.clear()
        except Exception as e:
            print(f"Error en destructor de Comentario: {e}")
    def limpiar_respuestas_eliminadas(self):
        self.__respuestas = [r for r in self.__respuestas if r.esta_activo()]
        for r in self.__respuestas:
            r.limpiar_respuestas_eliminadas()
    def esta_activo(self):
        return self.__activo
    def editar_comentario(self, nuevo_contenido):
        if self.__activo:
            self.__contenido = nuevo_contenido
            return True
        else:
            print("No se puede editar un comentario eliminado.")
            return False
    #Control de respuestas
    def agregar_respuesta(self, respuesta):
        self.__respuestas.append(respuesta)
    def mostrar_respuestas(self, nivel=1):
        indent = "  " * nivel
        for resp in self.__respuestas:
            print(f"{indent}{resp.mostrar_comentario()}")
            resp.mostrar_respuestas(nivel + 1)        

    #Setters y Getters
    @property
    def cantidad_respuestas(self):
        return len(self.__respuestas)
    @property
    def autor(self):
        return self.__autor.nombre
    @autor.setter
    def autor(self, nuevo_autor:Usuario):
        if not isinstance(nuevo_autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.")
        self.__autor = nuevo_autor
    @property
    def contenido(self):
        return self.__contenido
    @contenido.setter
    def contenido(self, nuevo_contenido):
        self.__contenido = nuevo_contenido
    @property
    def fecha(self):
        return self.__fecha
    @property
    def foro(self):
        return self.__foro.nombre_foro
    @foro.setter
    def foro(self, nuevo_foro:Foro):
        if not isinstance(nuevo_foro, Foro):
            raise ValueError("El foro debe ser una instancia de Foro.")
        self.__foro = nuevo_foro
    def __str__(self):
        estado = " (eliminado)" if not self.__activo else ""
        return f"{self.__autor.nombre}{estado}: {self.__contenido}"
