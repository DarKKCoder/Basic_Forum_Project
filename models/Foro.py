from usuario import Usuario
from comentario import Comentario
class Foro:
    def __init__(self, autor:Usuario, nombre_foro="General", descripcion="Foro de discusión general"):
        if not isinstance(autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.") 
        self.__autor = autor  # Usuario que creó el foro
        self.__nombre_foro = nombre_foro
        self.__descripcion = descripcion
        self.__comentarios = []  # Lista de comentarios en el foro

    #Métodos
    def agregar_comentario(self, comentario:Comentario):
        if not isinstance(comentario, Comentario):
            raise ValueError("El comentario debe ser una instancia de Comentario.")
        self.__comentarios.append(comentario)

    def mostrar_comentarios(self):
        for i, comentario in enumerate(self.comentarios, 1):
            print(f"{i}. {comentario.mostrar_comentario()}")

    def obtener_comentario(self, indice):
        if 0 <= indice < len(self.__comentarios):
            return self.__comentarios[indice]
        return None

    def cerrar_foro(self):
        """Limpia manualmente los comentarios y desconecta referencias."""
        for comentario in self.__comentarios:
            comentario.borrar()
        self.__comentarios.clear()
        print(f"Foro '{self.__nombre_foro}' cerrado correctamente.")

    def __del__(self):
        """Destructor de seguridad (no siempre garantizado)."""
        try:
            if self.__comentarios:
                print(f"Destruyendo foro '{self.__nombre_foro}' y limpiando comentarios...")
                self.cerrar_foro()
        except Exception as e:
            print(f"Error en destructor de Foro: {e}")

    #Setters y Getters
    @property
    def autor(self):
        return self.__autor.nombre
    @property
    def comentarios(self):
        return self.__comentarios
    @property
    def cantidad_comentarios(self):
        return len(self.__comentarios)
    @property
    def nombre_foro(self):
        return self.__nombre_foro
    @property
    def descripcion(self):
        return self.__descripcion
    @autor.setter
    def autor(self, nuevo_autor):
        self.__autor = nuevo_autor
    @descripcion.setter
    def descripcion(self, nueva_descripcion):
        self.__descripcion = nueva_descripcion
    @nombre_foro.setter
    def nombre_foro(self, nuevo_nombre):
        self.__nombre_foro = nuevo_nombre
    @comentarios.setter
    def comentarios(self, nueva_lista):
        self.__comentarios = nueva_lista