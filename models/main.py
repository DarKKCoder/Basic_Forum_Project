import tkinter as tk
from tkinter import messagebox, scrolledtext
from usuario import Usuario
from foro import Foro
from comentario import Comentario
from fecha import Fecha
from notificacion import Notificacion
from datetime import datetime

BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
RED_COLOR = "#e74c3c"
GREEN_COLOR = "#2ecc71"
ORANGE_COLOR = "#f39c12"
BLUE_COLOR = "#3498db"
PURPLE_COLOR = "#9b59b6"

class ForoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Foros")
        self.master.configure(bg=BG_COLOR)
        self.master.geometry("1000x750")

        self.base_de_usuarios = Usuario.obtener_todos()
        self.base_de_foros = Foro.obtener_todos()
        self.usuario_actual = None
        self.foro_actual = None
        self.sistema_notificaciones = Notificacion()
        self.notificaciones_usuario = []  # Lista de notificaciones del usuario actual

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
        
        # Botón de notificaciones (con contador)
        self.btn_notificaciones = tk.Button(self.frame_sesion, text="🔔 Notificaciones (0)", 
                                           bg=PURPLE_COLOR, fg=BG_COLOR, command=self.ver_notificaciones)
        self.btn_notificaciones.pack(side="right", padx=5)

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
        tk.Button(self.frame_foros, text="Agregar a Whitelist", bg=BLUE_COLOR, fg=BG_COLOR, command=self.agregar_whitelist).pack(side="left", padx=5)
        tk.Button(self.frame_foros, text="Ver Whitelist", bg=ORANGE_COLOR, fg=BG_COLOR, command=self.ver_whitelist).pack(side="left", padx=5)

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

    # ==== SISTEMA DE NOTIFICACIONES ====
    def agregar_notificacion(self, mensaje, tipo='info'):
        """Agrega una notificación a la cola del usuario actual"""
        if self.usuario_actual:
            notificacion = {
                'mensaje': mensaje,
                'tipo': tipo,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            self.notificaciones_usuario.append(notificacion)
            self.actualizar_contador_notificaciones()
    
    def actualizar_contador_notificaciones(self):
        """Actualiza el contador de notificaciones en el botón"""
        cantidad = len(self.notificaciones_usuario)
        if cantidad > 0:
            self.btn_notificaciones.config(text=f"🔔 Notificaciones ({cantidad})", bg=RED_COLOR)
        else:
            self.btn_notificaciones.config(text="🔔 Notificaciones (0)", bg=PURPLE_COLOR)
    
    def ver_notificaciones(self):
        """Muestra la ventana de notificaciones"""
        if not self.usuario_actual:
            messagebox.showwarning("Advertencia", "Debes iniciar sesión para ver notificaciones")
            return
        
        ventana = tk.Toplevel(self.master)
        ventana.title("Centro de Notificaciones")
        ventana.geometry("500x400")
        ventana.configure(bg=BG_COLOR)
        
        tk.Label(ventana, text="📬 Notificaciones", bg=BG_COLOR, fg=FG_COLOR, 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Área de texto con scroll para notificaciones
        text_area = scrolledtext.ScrolledText(ventana, bg="#2c2c2c", fg=FG_COLOR, 
                                              wrap=tk.WORD, height=15)
        text_area.pack(padx=10, pady=10, fill="both", expand=True)
        
        if self.notificaciones_usuario:
            for notif in self.notificaciones_usuario:
                icono = "ℹ️" if notif['tipo'] == 'info' else "✅" if notif['tipo'] == 'exito' else "⚠️"
                text_area.insert(tk.END, f"{icono} [{notif['timestamp']}] {notif['mensaje']}\n\n")
        else:
            text_area.insert(tk.END, "No tienes notificaciones nuevas.")
        
        text_area.config(state=tk.DISABLED)
        
        # Botón para limpiar notificaciones
        def limpiar_notificaciones():
            self.notificaciones_usuario.clear()
            self.actualizar_contador_notificaciones()
            messagebox.showinfo("Éxito", "Notificaciones limpiadas")
            ventana.destroy()
        
        tk.Button(ventana, text="Marcar todas como leídas", bg=GREEN_COLOR, fg=BG_COLOR, 
                 command=limpiar_notificaciones).pack(pady=10)

    # ==== REGISTRO ====
    def registrar_usuario(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Registrar Usuario")
        ventana.geometry("300x300")
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
        
        # Frame para Radio Buttons de Rol
        tk.Label(ventana, text="Rol:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        frame_rol = tk.Frame(ventana, bg=BG_COLOR)
        frame_rol.pack(pady=5)
        
        rol_var = tk.StringVar(value="General")
        tk.Radiobutton(frame_rol, text="General", variable=rol_var, value="General", 
                      bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).pack(side="left", padx=10)
        tk.Radiobutton(frame_rol, text="Admin", variable=rol_var, value="Admin", 
                      bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).pack(side="left", padx=10)
        
        # Frame para código de admin (oculto por defecto)
        frame_codigo = tk.Frame(ventana, bg=BG_COLOR)
        tk.Label(frame_codigo, text="Código Admin:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        entry_codigo = tk.Entry(frame_codigo, show="*")
        entry_codigo.pack(side="left", padx=5)
        
        def mostrar_codigo(*args):
            if rol_var.get() == "Admin":
                frame_codigo.pack(pady=5)
            else:
                frame_codigo.pack_forget()
        
        rol_var.trace('w', mostrar_codigo)

        def crear_usuario():
            nombre = entry_nombre.get().strip()
            correo = entry_correo.get().strip()
            contraseña = entry_pass.get().strip()
            rol = rol_var.get()
            
            if not nombre or not correo or not contraseña:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Verificar código de admin si es necesario
            if rol == "Admin":
                codigo = entry_codigo.get().strip()
                if codigo != "admin":
                    messagebox.showerror("Error", "Código de administrador incorrecto")
                    return
            
            if Usuario.buscar_por_correo(correo):
                messagebox.showerror("Error", f"El correo '{correo}' ya está registrado")
                return
            
            try:
                nuevo_usuario = Usuario(nombre, correo, contraseña, rol)
                nuevo_usuario.guardar_bd()
                self.base_de_usuarios.append(nuevo_usuario)
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' registrado correctamente como {rol}")
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
                self.agregar_notificacion(f"Bienvenido de nuevo, {u.nombre}!", 'exito')
                self.actualizar_lista_foros()
                self.actualizar_lista_comentarios()
                return
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # ==== FOROS ====
    def actualizar_lista_foros(self):
        self.listbox_foros.delete(0, tk.END)
        self.base_de_foros = Foro.obtener_todos()
        for f in self.base_de_foros:
            # Mostrar solo foros públicos o privados donde el usuario esté en whitelist
            if not f.es_privado:
                self.listbox_foros.insert(tk.END, f"{f.nombre_foro} (Público)")
            elif self.usuario_actual and (self.usuario_actual in f.whitelist or f.autor == self.usuario_actual or self.usuario_actual.rol == "Admin"):
                self.listbox_foros.insert(tk.END, f"{f.nombre_foro} (Privado)")

    def seleccionar_foro(self, event):
        idx = self.listbox_foros.curselection()
        if idx:
            # Obtener el foro correspondiente al índice visible
            foros_visibles = []
            for f in self.base_de_foros:
                if not f.es_privado:
                    foros_visibles.append(f)
                elif self.usuario_actual and (self.usuario_actual in f.whitelist or f.autor == self.usuario_actual or self.usuario_actual.rol == "Admin"):
                    foros_visibles.append(f)
            
            if idx[0] < len(foros_visibles):
                self.foro_actual = foros_visibles[idx[0]]
                self.actualizar_lista_comentarios()

    def crear_foro(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión para crear un foro")
            return
        
        ventana = tk.Toplevel(self.master)
        ventana.title("Crear Foro")
        ventana.geometry("300x250")
        ventana.configure(bg=BG_COLOR)
        
        tk.Label(ventana, text="Nombre del Foro:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack(pady=5)
        
        tk.Label(ventana, text="Descripción:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        entry_desc = tk.Entry(ventana)
        entry_desc.pack(pady=5)
        
        # Checkbox para foro privado
        es_privado_var = tk.BooleanVar(value=False)
        tk.Checkbutton(ventana, text="Foro Privado", variable=es_privado_var, 
                      bg=BG_COLOR, fg=FG_COLOR, selectcolor=BG_COLOR).pack(pady=10)

        def crear():
            nombre = entry_nombre.get().strip()
            descripcion = entry_desc.get().strip() or "Foro de discusión"
            es_privado = es_privado_var.get()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre del foro es obligatorio")
                return
            
            foro = Foro.crear(self.usuario_actual, nombre, descripcion)
            foro.es_privado = es_privado
            
            # Si es privado, agregar al autor a la whitelist automáticamente
            if es_privado:
                foro.agregar_a_whitelist(self.usuario_actual)
            
            foro.actualizar_whitelist_bd()
            self.actualizar_lista_foros()
            ventana.destroy()
            
            tipo = "privado" if es_privado else "público"
            messagebox.showinfo("Éxito", f"Foro '{nombre}' creado correctamente como {tipo}")
            self.agregar_notificacion(f"Has creado el foro '{nombre}' ({tipo})", 'exito')

        tk.Button(ventana, text="Crear Foro", bg=GREEN_COLOR, fg=BG_COLOR, command=crear).pack(pady=10)

    def cerrar_foro(self):
        if not self.foro_actual:
            messagebox.showerror("Error", "Selecciona un foro")
            return
        if self.foro_actual.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
            nombre_foro = self.foro_actual.nombre_foro
            # Borrar todos los comentarios antes de borrar el foro
            for c in self.foro_actual.comentarios:
                c.borrar(self.usuario_actual)
            self.foro_actual.cerrar_foro()
            self.actualizar_lista_foros()
            self.foro_actual = None
            messagebox.showinfo("Éxito", "Foro cerrado correctamente")
            self.agregar_notificacion(f"Has cerrado el foro '{nombre_foro}'", 'info')
        else:
            messagebox.showerror("Error", "Solo el propietario o un admin puede cerrar el foro")

    # ==== WHITELIST ====
    def agregar_whitelist(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión")
            return
        
        if not self.foro_actual:
            messagebox.showerror("Error", "Selecciona un foro")
            return
        
        if not self.foro_actual.es_privado:
            messagebox.showwarning("Advertencia", "Este foro es público, no requiere whitelist")
            return
        
        if self.foro_actual.autor != self.usuario_actual and self.usuario_actual.rol != "Admin":
            messagebox.showerror("Error", "Solo el propietario o un admin puede modificar la whitelist")
            return
        
        ventana = tk.Toplevel(self.master)
        ventana.title("Agregar Usuario a Whitelist")
        ventana.geometry("350x200")
        ventana.configure(bg=BG_COLOR)
        
        tk.Label(ventana, text=f"Foro: {self.foro_actual.nombre_foro}", 
                bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Label(ventana, text="Selecciona un usuario:", bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        
        listbox_usuarios = tk.Listbox(ventana, bg="#2c2c2c", fg=FG_COLOR, height=5)
        listbox_usuarios.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Mostrar solo usuarios que NO están en la whitelist
        usuarios_disponibles = []
        for u in self.base_de_usuarios:
            if u not in self.foro_actual.whitelist:
                usuarios_disponibles.append(u)
                listbox_usuarios.insert(tk.END, f"{u.nombre} ({u.correo})")
        
        def agregar():
            idx = listbox_usuarios.curselection()
            if idx:
                usuario_seleccionado = usuarios_disponibles[idx[0]]
                self.foro_actual.agregar_a_whitelist(usuario_seleccionado)
                self.foro_actual.actualizar_whitelist_bd()
                
                # NOTIFICACIÓN: Usuario agregado a whitelist
                self.sistema_notificaciones.notificar_usuario_agregado(
                    self.foro_actual, 
                    usuario_seleccionado, 
                    self.usuario_actual
                )
                
                # Agregar notificación local
                self.agregar_notificacion(
                    f"Has agregado a {usuario_seleccionado.nombre} al foro '{self.foro_actual.nombre_foro}'",
                    'exito'
                )
                
                messagebox.showinfo("Éxito", f"Usuario '{usuario_seleccionado.nombre}' agregado a la whitelist")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "Selecciona un usuario")
        
        tk.Button(ventana, text="Agregar", bg=GREEN_COLOR, fg=BG_COLOR, command=agregar).pack(pady=10)

    def ver_whitelist(self):
        if not self.foro_actual:
            messagebox.showerror("Error", "Selecciona un foro")
            return
        
        if not self.foro_actual.es_privado:
            messagebox.showinfo("Info", "Este foro es público, no tiene whitelist")
            return
        
        ventana = tk.Toplevel(self.master)
        ventana.title("Whitelist del Foro")
        ventana.geometry("400x300")
        ventana.configure(bg=BG_COLOR)
        
        tk.Label(ventana, text=f"Whitelist de: {self.foro_actual.nombre_foro}", 
                bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold")).pack(pady=10)
        
        listbox_whitelist = tk.Listbox(ventana, bg="#2c2c2c", fg=FG_COLOR)
        listbox_whitelist.pack(pady=5, padx=10, fill="both", expand=True)
        
        if self.foro_actual.whitelist:
            for u in self.foro_actual.whitelist:
                listbox_whitelist.insert(tk.END, f"{u.nombre} ({u.correo}) - {u.rol}")
        else:
            listbox_whitelist.insert(tk.END, "No hay usuarios en la whitelist")
        
        # Botón para eliminar de whitelist (solo para propietario o admin)
        if self.foro_actual.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
            def eliminar():
                idx = listbox_whitelist.curselection()
                if idx and self.foro_actual.whitelist:
                    usuario_seleccionado = self.foro_actual.whitelist[idx[0]]
                    self.foro_actual.eliminar_de_whitelist(usuario_seleccionado)
                    self.foro_actual.actualizar_whitelist_bd()
                    
                    self.agregar_notificacion(
                        f"Has eliminado a {usuario_seleccionado.nombre} del foro '{self.foro_actual.nombre_foro}'",
                        'info'
                    )
                    
                    messagebox.showinfo("Éxito", f"Usuario '{usuario_seleccionado.nombre}' eliminado de la whitelist")
                    ventana.destroy()
                    self.ver_whitelist()
                else:
                    messagebox.showerror("Error", "Selecciona un usuario")
            
            tk.Button(ventana, text="Eliminar Seleccionado", bg=RED_COLOR, fg=BG_COLOR, command=eliminar).pack(pady=10)

    # ==== COMENTARIOS ====
    def actualizar_lista_comentarios(self):
        self.listbox_comentarios.delete(0, tk.END)
        if self.foro_actual:
            # Verificar acceso a foro privado
            if self.foro_actual.es_privado:
                if not self.usuario_actual:
                    self.listbox_comentarios.insert(tk.END, "Debes iniciar sesión para ver este foro privado")
                    return
                if self.usuario_actual not in self.foro_actual.whitelist and self.foro_actual.autor != self.usuario_actual and self.usuario_actual.rol != "Admin":
                    self.listbox_comentarios.insert(tk.END, "No tienes acceso a este foro privado")
                    return
            
            self.foro_actual.comentarios = Comentario.obtener_por_foro(self.foro_actual.id_foro)
            for c in self.foro_actual.comentarios:
                autor_nombre = c.autor.nombre if c.autor else "Desconocido"
                self.listbox_comentarios.insert(tk.END, f"{autor_nombre}: {c.contenido}")

    def agregar_comentario(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "Debes iniciar sesión")
            return
        
        if not self.foro_actual:
            messagebox.showerror("Error", "Selecciona un foro")
            return
        
        # Verificar acceso a foro privado
        if self.foro_actual.es_privado:
            if self.usuario_actual not in self.foro_actual.whitelist and self.foro_actual.autor != self.usuario_actual and self.usuario_actual.rol != "Admin":
                messagebox.showerror("Error", "No tienes acceso a este foro privado")
                return
        
        contenido = self.entry_comentario.get().strip()
        if contenido:
            ahora = datetime.now()
            fecha = Fecha(dia=ahora.day, mes=ahora.month, anio=ahora.year, hora=ahora.strftime("%H:%M:%S"))
            fecha.guardar_bd()
            
            comentario = Comentario(self.usuario_actual, self.foro_actual, contenido, fecha)
            comentario.guardar_bd()
            
            # NOTIFICACIÓN: Nuevo comentario para usuarios en la whitelist
            if self.foro_actual.es_privado:
                for usuario in self.foro_actual.whitelist:
                    if usuario != self.usuario_actual:  # No notificar al autor del comentario
                        self.sistema_notificaciones.notificar_nuevo_comentario(
                            comentario, 
                            self.foro_actual, 
                            usuario
                        )
            
            # Notificación local
            self.agregar_notificacion(
                f"Has comentado en '{self.foro_actual.nombre_foro}': {contenido[:50]}...",
                'exito'
            )
            
            self.entry_comentario.delete(0, tk.END)
            self.actualizar_lista_comentarios()
        else:
            messagebox.showerror("Error", "El comentario no puede estar vacío")

    def eliminar_comentario(self):
        idx = self.listbox_comentarios.curselection()
        if idx and self.foro_actual:
            comentario = self.foro_actual.obtener_comentario(idx[0])
            if comentario.autor == self.usuario_actual or self.usuario_actual.rol == "Admin":
                comentario.borrar(self.usuario_actual)
                self.agregar_notificacion(f"Has eliminado un comentario en '{self.foro_actual.nombre_foro}'", 'info')
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
                    self.agregar_notificacion(f"Has editado un comentario en '{self.foro_actual.nombre_foro}'", 'info')
                    self.entry_comentario.delete(0, tk.END)
                    self.actualizar_lista_comentarios()
            else:
                messagebox.showerror("Error", "No puedes editar este comentario")


if __name__ == "__main__":
    root = tk.Tk()
    app = ForoGUI(root)
    root.mainloop()