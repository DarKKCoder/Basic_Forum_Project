from foro import Foro 
from foroPrivado import ForoPrivado
from comentario import Comentario
from fecha import Fecha
from usuario import Usuario
from datetime import date

class Execute:

    # Datos iniciales del sistema
    foro = Foro("Administradores", "General", "Foro de discusión general")
    usuario1 = Usuario("Oscar", "oscar_3325", "342567", "General")
    usuario2 = Usuario("Ana", "ana_1234", "987654", "General")
    usuario3 = Usuario("Admin", "Admin", "Admin", "Admin")

    base_de_usuarios = [usuario1, usuario2, usuario3]
    base_de_foros = [foro]

    # ===========
    # Logs (no inputs)
    # ===========

    def mostrar_opciones(self):
        print("\n[LOG] Opciones disponibles:")
        print("1. Agregar comentario")
        print("2. Eliminar comentario")
        print("3. Editar comentario")
        print("4. Actualizar lista de comentarios")
        print("5. Seleccionar comentario")
        print("0. Salir")
        print("[LOG] GUI deberá manejar la selección del usuario.")
        return None   # GUI decidirá

    def iniciar_sesion(self):
        print("\n[LOG] iniciar_sesion() llamado.")
        print("[LOG] Esta función ya no pide email/contraseña.")
        print("[LOG] El GUI deberá enviar email y password manualmente.")

        # Ya no busca usuario. El GUI debe hacerlo.  
        return None

    def seleccionar_foro(self, usuario_actual):
        print("\n[LOG] seleccionar_foro() llamado.")
        print("[LOG] GUI debe decidir qué foro abrir o crear.")
        print("[LOG] Foros disponibles:")
        for foro in Execute.base_de_foros:
            print(" -", foro.nombre_foro)

        return None

    def usar_comentarios(self, usuario_actual, foro_actual):
        print("\n[LOG] usar_comentarios() llamado.")
        print("[LOG] Ahora esta función NO hace ninguna acción.")
        print("[LOG] El GUI debe llamar directamente:")
        print(" - foro_actual.agregar_comentario()")
        print(" - foro_actual.obtener_comentario()")
        print(" - comentario.editar_comentario()")
        print(" - comentario.borrar()")
        print(" - foro_actual.limpiar_eliminados()")

    def banner_inicio(self):
        print("=" * 50)
        print(" BIENVENIDO AL SISTEMA DE FOROS (MODO GUI READY) ")
        print("=" * 50)

    # ====================
    #        MAIN
    # ====================
    def main(self):
        self.banner_inicio()

        print("[LOG] Sistema iniciado.")
        print("[LOG] Usuarios precargados:")
        for u in Execute.base_de_usuarios:
            print(f" - {u.nombre} ({u.correo}) rol={u.rol}")

        print("\n[LOG] Foros precargados:")
        for f in Execute.base_de_foros:
            print(f" - {f.nombre_foro} ({f.descripcion})")

        fecha_hoy = Fecha()
        print("\n[LOG] Fecha de hoy:", fecha_hoy.mostrar_fecha())

        print("\n[LOG] El sistema está listo para ser controlado por Tkinter.")
        print("[LOG] No se inicia sesión, no se selecciona foro, no se comentará desde consola.")
        print("[LOG] El GUI debe tomar el control a partir de aquí.")



if __name__ == "__main__":
    Execute().main()
