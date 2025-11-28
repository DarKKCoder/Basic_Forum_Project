class Notificacion:
    def __init__(self):
        self.cola_notificaciones = []

    def notificar_nuevo_comentario(self, comentario, foro, usuario_destino):
        mensaje = f"Nuevo comentario en '{foro.titulo}' por {comentario.autor.nombre}"
        notificacion = {
            'tipo': 'nuevo_comentario',
            'mensaje': mensaje,
            'usuario_destino': usuario_destino,
        }
        self.encolar_notificacion(notificacion)

    def notificar_usuario_agregado(self, foro_privado, usuario_agregado, usuario_admin):
        mensaje = f"Has sido agregado al foro privado '{foro_privado.titulo}' por {usuario_admin.nombre}"
        # ... lógica similar

    def encolar_notificacion(self, notificacion):
        self.cola_notificaciones.append(notificacion)
        self.procesar_cola()

    def procesar_cola(self):
        # Lógica para enviar emails, push notifications, etc.
        for notif in self.cola_notificaciones:
            print(f"[NOTIFICACIÓN para {notif['usuario_destino'].nombre}]: {notif['mensaje']}")