# from Usuario import Usuario
#from Foro import Foro
#from ForoPrivado import ForoPrivado
#from Comentario import Comentario
#from Fecha import Fecha
#from datetime import date

"""class Execute:

    # Crear instancias de Usuario y Foro para pruebas
    foro = Foro("Adminstradores", "General", "Foro de discusión general")
    usuario1 = Usuario("Oscar","oscar_3325","342567","General")
    usuario2 = Usuario("Ana","ana_1234","987654","General")
    usuario3 = Usuario("Admin","Admin","Admin","Admin")
    base_de_usuarios = [usuario1, usuario2, usuario3]
    base_de_foros = [foro]
    
    
    def mostrar_opciones(self):
        print("\nOpciones disponibles:")
        print("1. Agregar comentario")
        print("2. Eliminar comentario")
        print("3. Editar comentario")
        print("4. Actualizar lista de  comentarios")
        print("5. Seleccionar comentario")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")
        return opcion

    def iniciar_sesion(self):
        print("\nBienvenido al sistema de foros, por favor inicie sesión o cree una.")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        opcion = input("Seleccione una opción (1 o 2): ")
        if opcion == "1":
            email = input("Ingrese su correo: ")
            password = input("Ingrese su contraseña: ")
            for usuario in Execute.base_de_usuarios:
                if email == usuario.correo and password == usuario.contraseña:
                    print("Inicio de sesión exitoso.")
                    return usuario
            print("Correo o contraseña incorrectos.")
            return None
        elif opcion == "2":
            nombre = input("Ingrese su nombre de usuario: ")
            email = input("Ingrese su correo: ")
            password = input("Cree una contraseña: ")
            nuevo_usuario = Usuario(nombre, email, password, "General")
            Execute.base_de_usuarios.append(nuevo_usuario)
            print(f"Cuenta creada para {nuevo_usuario.nombre} con correo {nuevo_usuario.correo}.")
            return nuevo_usuario
        else:
            print("Opción no válida.")
            return None

    def seleccionar_foro(self, usuario_actual):
        print("\nForos disponibles:")
        print("1. Crear nuevo foro")
        for idx, foro in enumerate(Execute.base_de_foros, start=2):
            print(f"{idx}. {foro.nombre_foro}")
        opcion_foro = input("Seleccione un foro por número o cree uno nuevo (1 para crear): ")
        
        if opcion_foro == "1":
            nombre_foro = input("Ingrese el nombre del foro: ")
            descripcion_foro = input("Ingrese la descripción del foro: ")
            es_privado = input("¿Desea que este foro sea privado? (s/n): ").lower() == 's'

            if es_privado:
                foro_actual = ForoPrivado(nombre_foro, descripcion_foro)
                foro_actual.agregar_a_whitelist(usuario_actual)
                print("Foro privado creado. Usted ha sido agregado a la whitelist.")

                respuesta = 's'
                while respuesta == 's':
                    correo_usuario = input("Ingrese el correo del usuario a agregar a la whitelist: ")
                    usuario_a_agregar = next((u for u in Execute.base_de_usuarios if u.correo == correo_usuario), None)
                    if usuario_a_agregar == usuario_actual:
                        print("No puedes agregarte a ti mismo nuevamente.")
                    elif usuario_a_agregar is None:
                        print("Usuario no encontrado.")
                    elif foro_actual.esta_en_whitelist(usuario_a_agregar):
                        print("Usuario ya está en la whitelist.")
                    else:
                        foro_actual.agregar_a_whitelist(usuario_a_agregar)
                        print(f"Usuario {usuario_a_agregar.nombre} agregado a la whitelist.")
                    respuesta = input("¿Desea agregar otro usuario? (s/n): ").lower()

                print("Usuarios en la whitelist:")
                foro_actual.mostrar_whitelist()

            else:
                foro_actual = Foro(nombre_foro, descripcion_foro)
                print("Foro público creado.")

            if foro_actual not in Execute.base_de_foros:
                Execute.base_de_foros.append(foro_actual)
            else:
                print("El foro ya existe.")

        elif opcion_foro.isdigit() and 2 <= int(opcion_foro) < len(Execute.base_de_foros) + 2:
            foro_actual = Execute.base_de_foros[int(opcion_foro) - 2]
        else:
            print("Opción no válida.")
            return None

        print(f"Has entrado al foro: {foro_actual.nombre_foro}")
        return foro_actual

    def usar_comentarios(self, usuario_actual, foro_actual):
        while True:
            opcion_comentario = self.mostrar_opciones()
            if opcion_comentario == "0":
                print("Saliendo del sistema de comentarios.")
                break

            if isinstance(foro_actual, ForoPrivado) and usuario_actual not in foro_actual.whitelist:
                print("No tienes permiso para comentar en este foro privado.")
                continue

            match opcion_comentario:
                case "1":
                    contenido = input("Escribe tu comentario: ")
                    comentario = Comentario(usuario_actual, contenido, foro_actual.nombre_foro)
                    foro_actual.agregar_comentario(comentario)
                    print("Comentario agregado.")
                case "2":
                    try:
                        indice = int(input("Ingrese el número del comentario a eliminar: ")) - 1
                    except ValueError:
                        print("Debe ingresar un número válido.")
                        continue

                    comentario = foro_actual.obtener_comentario(indice)
                    if comentario is None:
                        print("Comentario no encontrado.")
                        continue

                    if usuario_actual.rol == 'Admin' or comentario.autor == usuario_actual:
                        comentario.borrar()
                        foro_actual.limpiar_eliminados()
                        print("Comentario eliminado.")
                    else:
                        print("No puedes eliminar este comentario.")
                case "3":
                    try:
                        indice = int(input("Ingrese el número del comentario a editar: ")) - 1
                    except ValueError:
                        print("Debe ingresar un número válido.")
                        continue
                    comentario = foro_actual.obtener_comentario(indice)
                    if comentario is None:
                        print("Comentario no encontrado.")
                        continue
                    if comentario.autor == usuario_actual:
                        nuevo_contenido = input("Ingrese el nuevo contenido del comentario: ")
                        comentario.editar_comentario(nuevo_contenido) 
                        print("Comentario editado.")
                case "4":
                    print("Comentarios actuales:")
                    foro_actual.mostrar_comentarios()
                case "5":
                    try:
                        indice = int(input("Ingrese el número del comentario a seleccionar: ")) - 1
                    except ValueError:
                        print("Debe ingresar un número válido.")
                        continue
                    comentario = foro_actual.obtener_comentario(indice)
                    if comentario is None:
                        print("Comentario no encontrado.")
                        continue
                    print("Comentario seleccionado:")
                    print(comentario.mostrar_comentario(comentario))
                    print("Respuestas:")
                    comentario.mostrar_respuestas()

                case _:
                    print("Opción no válida.")

    def banner_inicio(self):
        print("=" * 50)
        print(" BIENVENIDO AL SISTEMA DE FOROS INTERACTIVOS ")
        print("=" * 50)

    def main(self):
        self.banner_inicio()
        usuario_actual = None
        foro_actual = None
        fecha_hoy = Fecha()

        print("Fecha de hoy:", fecha_hoy.mostrar_fecha())
        print("-----")

        while not isinstance(usuario_actual, Usuario):
            usuario_actual = self.iniciar_sesion()
            if not isinstance(usuario_actual, Usuario):
                print("No se pudo iniciar sesión o crear cuenta, vuelve a intentarlo.")

        print("-----")

        while not isinstance(foro_actual, Foro):
            foro_actual = self.seleccionar_foro(usuario_actual)
            if not isinstance(foro_actual, Foro):
                print("No se pudo seleccionar o crear un foro, vuelve a intentarlo.")

        self.usar_comentarios(usuario_actual, foro_actual)


if __name__ == "__main__":
    Execute().main()
"""