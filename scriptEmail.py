from __future__ import print_function
import os
import base64
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """
    Autentica y crea el servicio Gmail API.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(to, subject, message_text, name, files=[]):
    """
    Crea un mensaje MIME en formato Gmail API con contenido HTML y adjuntos.
    """
    msg = MIMEMultipart()
    msg['to'] = to
    msg['subject'] = subject

    body = message_text.replace("[Nombre de la autoridad o título del destinatario]", name)
    
    msg.attach(MIMEText(body, "html", "utf-8"))
    
    for file_path in files:
        with open(file_path, "rb") as f:
            attach_part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            attach_part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(attach_part)

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    return {'raw': raw.decode()}

def send_message(service, user_id, message):
    """
    Envía el mensaje a través del servicio Gmail API.
    """
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Mensaje enviado con ID: {sent_message['id']}")
        return sent_message
    except Exception as error:
        print(f"Error al enviar el mensaje: {error}")

def read_recipients_from_csv(csv_filename):
    """
    Lee la lista de destinatarios desde un archivo CSV con las columnas 'Nombre del director' y 'Correo de contacto'.
    """
    recipients = []
    try:
        with open(csv_filename, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                print(f"Fila leída: {row}")
                name = row.get('Nombre del director')
                email = row.get('Correo de contacto')
                if name and email:
                    recipients.append((name.strip(), email.strip()))
                else:
                    print("Error: Nombre o correo faltante en la fila.")
    except FileNotFoundError:
        print(f"Archivo {csv_filename} no encontrado.")
    except Exception as e:
        print(f"Error leyendo {csv_filename}: {e}")
    
    print(f"Destinatarios leídos: {recipients}")
    return recipients



def main():
    """
    Función principal para enviar correos masivos.
    """
    service = gmail_authenticate()

    recipients = read_recipients_from_csv('directores.csv')

    if not recipients:
        print("No se encontraron destinatarios. Verifica el archivo directores.csv.")
        return

    subject = "Invitación para Difundir el Workshop Internacional en Investigación de Inteligencia Artificial - PhawAI+TaReCDa 2025"
    
    body = """
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
        <p>Estimado/a [Nombre de la autoridad o título del destinatario],</p>
        <p>
          Es un placer dirigirme a usted en mi calidad de community manager para invitarle a considerar la difusión del PhawAI+TaReCDa 2025, un evento educativo de gran relevancia internacional para los estudiantes de pregrado de su universidad.
        </p>
        <p>
          Este workshop tiene como objetivo proporcionar una formación de alta calidad en el campo de la Inteligencia Artificial, a través de un enfoque teórico-práctico que incluirá cursos online y la posibilidad de participar en un workshop presencial con expertos internacionales. Además, los estudiantes más destacados tendrán la oportunidad de recibir becas de viaje para asistir a la fase onsite, lo que representa una excelente oportunidad para expandir sus conocimientos y ampliar su red profesional.
        </p>
        <p>A continuación, incluyo algunos detalles clave sobre el evento:</p>
        <ul>
          <li><strong>Fechas Importantes:</strong><br>
            Cierre de postulaciones: 10 de julio de 2025<br>
            Fase virtual (cursos online): Julio – Agosto 2025<br>
            <a href="https://forms.gle/Cr1Sr2S1Zven89SW6">Formulario de postulación</a><br>
            Sesión informativa: Viernes 04 de julio de 2025, 6:00 p.m. (hora Perú) 
            <a href="https://cedia.zoom.us/meeting/register/BBUjP54IQ5SqAKqu2kWFVQ#/registration">Registro</a>
          </li>
          <li><strong>Áreas de estudio durante la fase virtual:</strong><br>
            • Introducción a Python + Data Science<br>
            • Machine Learning<br>
            • Deep Learning<br>
            • Computer Vision<br>
            • Natural Language Processing
          </li>
          <li><strong>Beneficios para los estudiantes seleccionados:</strong><br>
            • Acceso a charlas técnicas y motivacionales con expertos internacionales.<br>
            • Becas completas de viaje para la fase onsite.<br>
            • Oportunidad de recibir retroalimentación y asesoría sobre proyectos de investigación.
          </li>
        </ul>
        <p>Nos encantaría contar con su apoyo para difundir este evento entre los estudiantes de su institución.</p>
        <p>Atentamente,<br>
          Sebastian Linares Liendo<br>
          Community Manager<br>
          PhawAi Perú<br>
          <a href="https://www.phawai.org">www.phawai.org</a>
        </p>
      </body>
    </html>
    """

    files_to_attach = ['SesionInformativa.pdf', 'Postula.pdf']

    for name, recipient in recipients:
        msg = create_message(recipient, subject, body, name, files=files_to_attach)
        send_message(service, "me", msg)

if __name__ == '__main__':
    main()