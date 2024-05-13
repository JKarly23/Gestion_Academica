from django.core.mail.message import EmailMessage

def send_username(username, password,correo):
    asunto = "StickAcademy a aprobado su registro al sitio"
    body = f"Su username de acceso es: {username}"+"\n"+f"Password para ingresar al sitio: {password}"
    from_message = "javierc.ps16@gmail.com"
    destinatary = [str(correo)]
    owne = ["javierc.ps16@gmail.com"]
    email = EmailMessage(subject=asunto,body=body,from_email=from_message,to=destinatary,reply_to=owne)
    email.send()