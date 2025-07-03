# ✉️ Envío Masivo de Correos con Gmail API

Este repositorio contiene un script en Python que envía correos masivos en formato HTML utilizando la Gmail API. Está diseñado para compartir convocatorias, notificaciones académicas o información institucional de manera programada y estructurada.

## 📚 Descripción

El script realiza:

- Autenticación con la Gmail API mediante OAuth 2.0.
- Lectura de destinatarios desde un archivo CSV.
- Generación de correos HTML con asunto y cuerpo definidos.
- Envío individual de correos a cada destinatario.

---

## ⚠️ Advertencia de uso

✅ Uso académico y organizacional responsable.  
❌ No usar este script para SPAM, prácticas fraudulentas o contrarias a políticas de uso de Gmail y Google Cloud Platform.

---

## 🛠️ Requerimientos

### 1. API y librerías utilizadas

- **Google Gmail API**
- google-auth, google-auth-oauthlib, google-auth-httplib2, google-api-python-client
- Librerías estándar: os, base64, csv, email

Instala las dependencias ejecutando:

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

---

### 2. Configuración de Google Cloud Platform

1. Ingresa a Google Cloud Console.
2. Crea un nuevo proyecto o selecciona uno existente.
3. Habilita la Gmail API.
4. En APIs & Services > Credentials:
   - Haz click en Create Credentials > OAuth client ID.
   - Selecciona Desktop App.
   - Descarga el archivo credentials.json y colócalo en el directorio raíz de tu proyecto.
5. Configura los orígenes autorizados y las URIs de redireccionamiento como:
   - http://localhost:8080
6. En OAuth consent screen (Pantalla de consentimiento OAuth):
   - Selecciona el modo de prueba si aún no verificas la app.
   - Agrega como usuarios de prueba la cuenta de correo desde la cual enviarás los correos masivos (por ejemplo, tu cuenta personal o institucional). Esto es obligatorio mientras la aplicación esté en modo de prueba, ya que solo los usuarios añadidos podrán usar la app antes de su verificación oficial.

✅ Esta configuración habilita el puerto 8080 que el script usa para completar el flujo de autenticación OAuth localmente.

⚠️ Nota: La configuración puede tardar entre 5 minutos y algunas horas en aplicarse completamente.

---

### 3. Primer uso y generación de token

La primera vez que ejecutes el script:

- Se abrirá una ventana de autenticación para iniciar sesión con la cuenta Gmail que enviará los correos.
- Se generará un archivo token.json con el token de acceso y refresco.  
  Este archivo no debe compartirse públicamente.

---

### 4. Archivo de destinatarios

Crea un archivo correos.csv con la siguiente estructura mínima:

email
correo1@dominio.com
correo2@dominio.com
correo3@dominio.com

⚠️ Asegúrate de:

- Usar UTF-8 en el archivo.
- No incluir espacios adicionales ni caracteres especiales en los correos.

---

### 5. Ejecución

python scriptEmail.py

Cada destinatario recibirá el correo de forma individual.

---

### 6. Estructura del proyecto

.
├── credentials.json
├── token.json
├── correos.csv
├── script.py
└── README.md

---

## 🔑 Permisos y seguridad

- Este script solicita el scope:
  https://www.googleapis.com/auth/gmail.send
  que permite enviar correos en nombre del usuario autenticado.

- Buenas prácticas de seguridad:

  ✅ No subir credentials.json ni token.json a repositorios públicos.  
  ✅ Usa .gitignore para excluirlos:

  credentials.json
  token.json

  ✅ Revisa las políticas de uso de Gmail para envíos masivos.

---

## 🎓 Autor

- Nombre: Sebastian Linares Liendo
- Universidad: Universidad Nacional Jorge Basadre Grohmann

---

## 📄 Licencia

Este proyecto es de uso académico. Para otros usos, consulta con el autor y revisa las políticas de Google Cloud Platform.

---

### 📌 Referencias

- Gmail API Python Quickstart
- Google API Client for Python
