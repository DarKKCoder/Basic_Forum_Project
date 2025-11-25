import Comentario
import Foro
class Usuario:
    def __init__(self, nombre, correo, contraseña, rol):
        self.__nombre = nombre
        self.__correo = correo
        self.__contraseña = contraseña
        self.__rol = rol

    #Métodos
    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Correo: {self.correo}"
    def crear_foro(self):
        titulo = input("Ingrese el título del foro: ")
        descripcion = input("Ingrese la descripción del foro: ")
        return Foro(self.nombre, titulo, descripcion)
    def crear_comentario(self):
        foro = input("Ingrese el nombre del foro (por defecto 'General'): ") or "General"
        contenido = input("Ingrese el contenido del comentario: ")
        return Comentario(self.nombre, contenido, foro)
    def editar_comentario(self, comentario):
        print("Comentario actual:", comentario.contenido)
        nuevo_contenido = input("Ingrese el contenido del comentario: ")
        comentario.contenido = nuevo_contenido
        return comentario
    def eliminar_comentario_propio(self, comentario):
        if comentario.autor == self.nombre:
            comentario.borrar()
            print("Comentario eliminado.")
        else:
            print("No se puede eliminar el comentario. No es tuyo o no existe.")
    
    #Setters y Getters
    @property
    def nombre(self):
        return self.__nombre
    @property
    def correo(self):
        return self.__correo
    @property
    def contraseña(self):
        return self.__contraseña
    @property
    def rol(self):
        return self.__rol
    @rol.setter
    def rol(self, nuevo_rol):
        self.__rol = nuevo_rol
    @contraseña.setter
    def contraseña(self, nueva_contraseña):
        self.__contraseña = nueva_contraseña
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
    @correo.setter
    def correo(self, nuevo_correo):
        self.__correo = nuevo_correo