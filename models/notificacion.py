# models/notificacion.py
from usuario import Usuario
from foro import Foro
from comentario import Comentario

class Notificacion:
    def __init__(self):
        self.cola_notificaciones = []

    def notificar_nuevo_comentario(self, comentario: Comentario, foro: Foro, usuario_destino: Usuario):
        mensaje = f"Nuevo comentario en '{foro.nombre_foro}' por {comentario.autor}"
        notificacion = {
            'tipo': 'nuevo_comentario',
            'mensaje': mensaje,
            'usuario_destino': usuario_destino,
        }
        self.encolar_notificacion(notificacion)

    def notificar_usuario_agregado(self, foro: Foro, usuario_agregado: Usuario, usuario_admin: Usuario):
        mensaje = f"Has sido agregado al foro privado '{foro.nombre_foro}' por {usuario_admin.nombre}"
        notificacion = {
            'tipo': 'usuario_agregado',
            'mensaje': mensaje,
            'usuario_destino': usuario_agregado,
        }
        self.encolar_notificacion(notificacion)

    def encolar_notificacion(self, notificacion: dict):
        self.cola_notificaciones.append(notificacion)
        self.procesar_cola()

    def procesar_cola(self):
        """Simula envío de notificaciones. En Tinker puedes usar esto para actualizar widgets."""
        for notif in self.cola_notificaciones:
            print(f"[NOTIFICACIÓN para {notif['usuario_destino'].nombre}]: {notif['mensaje']}")
        # Una vez procesadas, limpiar la cola
        self.cola_notificaciones.clear()
