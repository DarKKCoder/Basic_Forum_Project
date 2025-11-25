from Foro import Foro
from Usuario import Usuario
from Comentario import Comentario
class ForoPrivado(Foro):
    def __init__(self, autor:Usuario,nombre_foro="Privado", descripcion="Foro secreto", whitelist=None, comentarios=[]):
        if not isinstance(autor, Usuario):
            raise ValueError("El autor debe ser una instancia de Usuario.")
        super().__init__(autor, nombre_foro, descripcion, comentarios)
        if whitelist is None:
            whitelist = [autor]
        self.__whitelist = whitelist# Lista de usuarios permitidos

    # Polimorfismo: mostrar comentarios con mensaje especial
    def mostrar_comentarios(self):
        print("En la cámara de los secretos se dice:")
        super().mostrar_comentarios()
    def agregar_a_whitelist(self, usuario):
        if usuario not in self.__whitelist:
            self.__whitelist.append(usuario)
    def remover_de_whitelist(self, usuario):
        if usuario in self.__whitelist:
            self.__whitelist.remove(usuario)
    def esta_en_whitelist(self, usuario):
        return usuario in self.__whitelist
    def mostrar_whitelist(self):
        if not self.__whitelist or len(self.__whitelist) == 1:
            print("La whitelist está vacía.")
        else:
            print("Usuarios permitidos:")
            for u in self.__whitelist:
                print(f"- {u.nombre}")
    # Sobrescritura: solo usuarios en la whitelist pueden agregar comentarios
    def agregar_comentario(self, comentario):
        if comentario.autor in self.__whitelist:
            super().agregar_comentario(comentario)
        else:
            print("No tienes permiso para comentar en este foro privado.")
    #Setters y Getters
    @property
    def whitelist(self):
        return self.__whitelist
    @whitelist.setter
    def whitelist(self, nueva_whitelist):
        self.__whitelist = nueva_whitelist
