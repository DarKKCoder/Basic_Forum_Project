import tkinter as tk
from tkinter import messagebox
from usuario import Usuario
from foro import Foro
from comentario import Comentario
from fecha import Fecha
from datetime import datetime

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
RED_COLOR = "#e74c3c"
GREEN_COLOR = "#2ecc71"
ORANGE_COLOR = "#f39c12"

class ForoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Foros")
        self.master.configure(bg=BG_COLOR)
        self.master.geometry("1000x700")

        self.base_de_usuarios = Usuario.obtener_todos()
        self.base_de_foros = Foro.obtener_todos()
        self.usuario_actual = None
        self.foro_actual = None

        # ==== FRAME DE SESIÓN ====
        self.frame_sesion = tk.Frame(self.master, bg=BG_COLOR)
        self.frame_sesion.pack(padx=10, pady=10, fill="x")
        tk.Label(self.frame_sesion, text="Usuario:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        self.entry_usuario = tk.Entry(self.frame_sesion)
        self.entry_usuario.pack(side="left", padx=5)
        tk.Label(self.frame_sesion, text="Contraseña:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        self.entry_pass = tk.Entry(self.frame_sesion, show="*")
        self.entry_pass.pack(side="left", padx=5)
        tk.Button(self.frame_sesion, text="Iniciar sesión", bg=GREEN_COLOR, fg=BG_COLOR, command=self.iniciar_sesion).pack(side="left", padx=5)
        tk.Button(self.frame_sesion, text="Registrar usuario", bg=ORANGE_COLOR, fg=BG_COLOR, command=self.registrar_usuario).pack(side="left", padx=5)

        # ==== FRAME DE FOROS ====
        self.frame_foros = tk.Frame(self.master, bg=BG_COLOR)
        self.frame_foros.pack(padx=10, pady=10, fill="x")
        tk.Label(self.frame_foros, text="Foros disponibles:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w")
        self.listbox_foros = tk.Listbox(self.frame_foros, bg="#2c2c2c", fg=FG_COLOR, height=5)
        self.listbox_foros.pack(fill="x")
        self.listbox_foros.bind("<<ListboxSelect>>", self.seleccionar_foro)
        self.actualizar_lista_foros()
        tk.Button(self.frame_foros, text="Crear Foro", bg=GREEN_COLOR, fg=BG_COLOR, command=self.crear_foro).pack(side="left", padx=5)
        tk.Button(self.frame_foros, text="Cerrar Foro", bg=RED_COLOR, fg=BG_COLOR, command=self.cerrar_foro).pack(side="left", padx=5)
        tk.Button(self.frame_foros, text="Agregar a Whitelist", bg=ORANGE_COLOR, fg=BG_COLOR, command=self.agregar_whitelist).pack(side="left", padx=5)

        # ==== FRAME DE COMENTARIOS ====
        self.frame_comentarios = tk.Frame(self.master, bg=BG_COLOR)
        self.frame_comentarios.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Label(self.frame_comentarios, text="Comentarios:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w")
        self.listbox_comentarios = tk.Listbox(self.frame_comentarios, bg="#2c2c2c", fg=FG_COLOR)
        self.listbox_comentarios.pack(fill="both", expand=True)
        self.entry_comentario = tk.Entry(self.frame_comentarios, bg="#333333", fg=FG_COLOR)
        self.entry_comentario.pack(fill="x", pady=5)
        tk.Button(self.frame_comentarios, text="Agregar comentario", bg=ORANGE_COLOR, fg=BG_COLOR, command=self.agregar_comentario).pack(fill="x", pady=2)
        tk.Button(self.frame_comentarios, text="Editar comentario seleccionado", bg=GREEN_COLOR, fg=BG_COLOR, command=self.editar_comentario).pack(fill="x", pady=2)
        tk.Button(self.frame_comentarios, text="Eliminar comentario seleccionado", bg=RED_COLOR, fg=BG_COLOR, command=self.eliminar_comentario).pack(fill="x", pady=2)
        tk.Button(self.frame_comentarios, text="Actualizar lista", bg=GREEN_COLOR, fg=BG_COLOR, command=self.actualizar_lista_comentarios).pack(fill="x", pady=2)

    # ==== REGISTRO ====
    def registrar_usuario(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Registrar Usuario")
        ventana.geometry("300x250")
        ventana.configure(bg=BG_COLOR)

        tk.Label(ventana, text="Nombre:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)
        tk.Label(ventana, text="Correo:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_correo = tk.Entry(ventana)
        entry_correo.pack(pady=5)
        tk.Label(ventana, text="Contraseña:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_pass = tk.Entry(ventana, show="*")
        entry_pass.pack(pady=5)
        tk.Label(ventana, text="Rol:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_rol = tk.Entry(ventana)
        entry_rol.pack(pady=5)

        def crear_usuario():
            nombre = entry_nombre.get().strip()
            correo = entry_correo.get().strip()
            contraseña = entry_pass.get().strip()
            rol = entry_rol.get().strip() or "General"
            if not nombre or not correo or not contraseña:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            if Usuario.buscar_por_correo(correo):
                messagebox.showerror("Error", f"El correo '{correo}' ya está registrado")
                return
            try:
                nuevo_usuario = Usuario(nombre, correo, contraseña, rol)
                nuevo_usuario.guardar_bd()
                self.base_de_usuarios.append(nuevo_usuario)
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado correctamente")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Registrar", bg=GREEN_COLOR, fg=BG_COLOR, command=crear_usuario).pack(pady=10)

    # ==== LOGIN ====
    def iniciar_sesion(self):
        email = self.entry_usuario.get()
        password = self.entry_pass.get()
        for u in self.base_de_usuarios:
            if u.correo == email and u.contraseña == password:
                self.usuario_actual = u
                self.entry_usuario.delete(0, tk.END)
                self.entry_pass.delete(0, tk.END)
                messagebox.showinfo("Sesión iniciada", f"Bienvenido {u.nombre}")
                self.actualizar_lista_comentarios()
                return
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # ==== FOROS ====
    def actualizar_lista_foros(self):
        self.listbox_foros.delete(0, tk.END)
        self.base_de_foros = Foro.obtener_todos()
        for f in self.base_de_foros:
            self.listbox_foros.insert(tk.END, f.nombre_foro)

    def seleccionar_foro(self, event):
        idx = self.listbox_foros.curselection()
        if idx:
            self.foro_actual = self.base_de_foros[idx[0]]
            self.actualizar_lista_comentarios()

    def crear_foro(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión para crear un foro")
            return
        ventana = tk.Toplevel(self.master)
        ventana.title("Crear Foro")
        ventana.geometry("300x200")
        ventana.configure(bg=BG_COLOR)
        tk.Label(ventana, text="Nombre del Foro:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)
        tk.Label(ventana, text="Descripción:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_desc = tk.Entry(ventana)
        entry_desc.pack(pady=5)

        def crear():
            nombre = entry_nombre.get().strip()
            descripcion = entry_desc.get().strip() or "Foro de discusión"
            foro = Foro.crear(self.usuario_actual, nombre, descripcion)
            self.actualizar_lista_foros()
            ventana.destroy()
            messagebox.showinfo("Éxito", f"Foro '{nombre}' creado correctamente")

        tk.Button(ventana, text="Crear Foro", bg=GREEN_COLOR, fg=BG_COLOR, command=crear).pack(pady=10)

    def cerrar_foro(self):
        if not self.foro_actual:
            messagebox.showerror("Error", "Selecciona un foro")
            return
        if self.foro_actual.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
            # Borrar todos los comentarios antes de borrar el foro
            for c in self.foro_actual.comentarios:
                c.borrar(self.usuario_actual)  # Si eres admin puedes forzar borrado
            self.foro_actual.cerrar_foro()
            self.actualizar_lista_foros()
            self.foro_actual = None
        else:
            messagebox.showerror("Error", "Solo el propietario o un admin puede cerrar el foro")


    # ==== WHITELIST ====
    def agregar_whitelist(self):
        messagebox.showinfo("Info", "Whitelist no implementada en esta versión de emergencia.")

    # ==== COMENTARIOS ====
    def actualizar_lista_comentarios(self):
        self.listbox_comentarios.delete(0, tk.END)
        if self.foro_actual:
            self.foro_actual.comentarios = Comentario.obtener_por_foro(self.foro_actual.id_foro)
            for c in self.foro_actual.comentarios:
                autor_nombre = c.autor.nombre if c.autor else "Desconocido"
                self.listbox_comentarios.insert(tk.END, f"{autor_nombre}: {c.contenido}")

    def agregar_comentario(self):
        if self.usuario_actual and self.foro_actual:
            contenido = self.entry_comentario.get().strip()
            if contenido:
                # Crear objeto Fecha con fecha/hora actual
                ahora = datetime.now()
                fecha = Fecha(dia=ahora.day, mes=ahora.month, anio=ahora.year, hora=ahora.strftime("%H:%M:%S"))
                fecha.guardar_bd()  # Guarda en DB y asigna id_fecha
                
                # Crear comentario con fecha
                comentario = Comentario(self.usuario_actual, self.foro_actual, contenido, fecha)
                comentario.guardar_bd()
                self.entry_comentario.delete(0, tk.END)
                self.actualizar_lista_comentarios()
            else:
                messagebox.showerror("Error", "El comentario no puede estar vacío")
        else:
            messagebox.showerror("Error", "Debes iniciar sesión y seleccionar un foro")

    def eliminar_comentario(self):
        idx = self.listbox_comentarios.curselection()
        if idx and self.foro_actual:
            comentario = self.foro_actual.obtener_comentario(idx[0])
            if comentario.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
                comentario.borrar(self.usuario_actual)
                self.actualizar_lista_comentarios()
            else:
                messagebox.showerror("Error", "No puedes eliminar este comentario")

    def editar_comentario(self):
        idx = self.listbox_comentarios.curselection()
        if idx and self.foro_actual:
            comentario = self.foro_actual.obtener_comentario(idx[0])
            if comentario.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
                nuevo_texto = self.entry_comentario.get().strip()
                if nuevo_texto:
                    comentario.editar(nuevo_texto, self.usuario_actual)
                    self.entry_comentario.delete(0, tk.END)
                    self.actualizar_lista_comentarios()
            else:
                messagebox.showerror("Error", "No puedes editar este comentario")


if __name__ == "__main__":
    root = tk.Tk()
    app = ForoGUI(root)
    root.mainloop()
