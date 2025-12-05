"""
Módulo de envío de emails para el sistema FELA
"""

from django.core import mail
from django.conf import settings


def send_registration_notification_to_admin(user):
    """
    Envía un email al administrador cuando un nuevo usuario se registra.
    
    Args:
        user: Instancia de CustomUser recién registrado
    """
    subject = 'Nuevo usuario registrado en FELA'
    
    # URL del panel de administración
    admin_url = f"{settings.ALLOWED_HOSTS[0]}" if not settings.DEBUG else "https://gisserver.car.upv.es/fela_api"
    
    message = f"""
Hola Administrador,

Un nuevo usuario se ha registrado en el aplicativo de divulgación FELA y está pendiente de aprobación:

DATOS DEL USUARIO:

- Usuario: {user.username}
- Nombre: {user.first_name} {user.last_name}
- Email: {user.email}
- Organismo: {user.organismo or 'No especificado'}
- Fecha de registro: {user.created_at.strftime('%d/%m/%Y %H:%M')}

ACCIONES DISPONIBLES:

Para aprobar o gestionar este usuario, accede al panel de administración:

1. Panel Web: {admin_url}/admin/core/customuser/{user.id}/change/
2. O desde la pestaña "Superusuario" en la aplicación

Una vez aprobado, el usuario recibirá un email de confirmación automáticamente.

---
Aplicativo de divulgación FELA - Framework for Effective Land Administration
Universitat Politècnica de València
    """.strip()
    
    email_from = settings.EMAIL_FROM
    recipient_list = [admin[1] for admin in settings.ADMINS]  # Extraer emails de ADMINS
    
    # Eliminar duplicados
    recipient_list = list(dict.fromkeys(recipient_list))
    
    if settings.DEBUG:
        print('=' * 60)
        print('ENVIANDO EMAIL DE REGISTRO AL ADMINISTRADOR')
        print('=' * 60)
        print(f'Destinatarios: {recipient_list}')
        print(f'Subject: {subject}')
        print(f'Email from: {email_from}')
        print('-' * 60)
        print(message)
        print('=' * 60)
    
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            to=recipient_list,  # Usar 'to' en lugar de 'bcc' para admin
            connection=connection,
        ).send()
    
    if settings.DEBUG:
        print('✅ Email guardado en sent_emails/')
    else:
        print('✅ Email enviado exitosamente')


def send_approval_notification_to_user(user):
    """
    Envía un email al usuario cuando su cuenta ha sido aprobada.
    
    Args:
        user: Instancia de CustomUser aprobado
    """
    subject = 'Tu cuenta en FELA ha sido aprobada'
    
    # URL de login
    login_url = f"{settings.ALLOWED_HOSTS[0]}/login.html" if not settings.DEBUG else "https://gisserver.car.upv.es/fela/login.html"
    app_url = f"{settings.ALLOWED_HOSTS[0]}" if not settings.DEBUG else "https://gisserver.car.upv.es/fela/"
    
    message = f"""
Hola {user.first_name},

¡Buenas noticias! Tu cuenta en el aplicativo de divulgación FELA ha sido aprobada por el administrador.

DETALLES DE TU CUENTA:

- Usuario: {user.username}
- Email: {user.email}
- Organismo: {user.organismo or 'No especificado'}

PRÓXIMOS PASOS:

Ya puedes iniciar sesión y comenzar a colaborar con la divulgación del Marco para la Administración Efectiva del Territorio (FELA):

1. Accede a: {login_url}
2. Usa tu nombre de usuario y contraseña
3. Podrás crear y editar eventos en el mapa

FUNCIONALIDADES DISPONIBLES:

- Visualizar eventos en el mapa interactivo
- Crear eventos completos con presentaciones
- Agregar presentaciones a eventos
- Agregar ponentes a presentaciones
- Editar información existente


Si tienes alguna pregunta, no dudes en contactar con el administrador.

¡Bienvenido al aplicativo de divulgación FELA!

---
Aplicativo de divulgación FELA - Framework for Effective Land Administration
Universitat Politècnica de València
{app_url}
    """.strip()
    
    email_from = settings.EMAIL_FROM
    recipient_list = [user.email]
    
    if settings.DEBUG:
        print('=' * 60)
        print('ENVIANDO EMAIL DE APROBACIÓN AL USUARIO')
        print('=' * 60)
        print(f'Destinatario: {recipient_list}')
        print(f'Subject: {subject}')
        print(f'Email from: {email_from}')
        print('-' * 60)
        print(message)
        print('=' * 60)
    
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            to=recipient_list,
            connection=connection,
        ).send()
    
    if settings.DEBUG:
        print('✅ Email guardado en sent_emails/')
    else:
        print('✅ Email enviado exitosamente')