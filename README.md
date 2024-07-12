# Kamachiq TELEC2




## C2 en Telegram: ¡Cómo los Hackers Controlan Tu PC y Cómo Protegerte!

*
**Este script de Python permite a un usuario controlar remotamente una computadora a través de Telegram. **

Incluye funcionalidades como:*

-   Listado de archivos del directorio actual
-   Escaneo de puertos y conexiones activas
-   Cambio de directorio
-   Ejecución de comandos del sistema
-   Obtención de la ubicación geográfica basada en la IP pública
-   Inicio y detención de un keylogger
-   Envío de registros del keylogger
-   Captura de pantalla
-   Grabación y envío de video de la pantalla
-   Obtención de la dirección IP pública
-   Monitoreo del portapapeles y envío de notificaciones a Telegram
-   Congelado y descongelado del mouse
  
## Requisitos
- El script requiere las siguientes bibliotecas de Python:
- telebot
- requests
- pyautogui
- pynput
- urllib
- glob
- pyperclip
- psutil
- numpy
- opencv-python-headless
**Estas bibliotecas se instalarán automáticamente al ejecutar el script, si no están presentes en el sistema.**

## Instrucciones de uso
Asegúrate de tener un bot de Telegram creado y obtén el token de acceso.
Reemplaza el valor de BOT_TOKEN y CHAT_ID en el script con tus credenciales.
Ejecuta el script de Python.

Una vez establecida la conexión, podrás enviar los siguientes comandos al bot de Telegram:

- hola: Saluda al bot.
- dir: Lista los archivos del directorio actual.
- scan_ports: Escanea los puertos de la máquina.
- cd ..: Retrocede al directorio padre.
- cd [ruta]: Cambia al directorio especificado.
- exec [comando]: Ejecuta comandos del sistema.
- geo: Ejecuta la geolocalización.
- keylog_start: Inicia el keylogger.
- send_reg: Envía los registros del keylogger.
- keylog_stop: Detiene el keylogger.
- send_file [ruta]: Envía un archivo específico.
- screenshot: Captura una imagen de la pantalla.
- video_start: Inicia la grabación de la pantalla.
- video_stop: Detiene la grabación y envía el video.
- ip_publica: Muestra la dirección IP pública.
- help: Muestra la lista de comandos disponibles.
- whoami: Muestra información del usuario actual.
- pwd: Muestra la ruta del directorio actual.
- iniciar_monitoreo: Inicia el monitoreo del portapapeles.
- detener_monitoreo: Detiene el monitoreo del portapapeles.
- disable_mouse: Congela el mouse.
- enable_mouse: Descongelar el mouse.
- Seguridad y Consideraciones

**Este script puede ser utilizado con fines maliciosos, por lo que se recomienda tener precaución al usarlo. Asegúrate de tener el consentimiento del propietario de la computadora antes de ejecutar este script.
Además, se recomienda mantener el software actualizado, utilizar antivirus y habilitar la autenticación de dos factores para proteger tu sistema.**

## Contacto y Licencia


Este script se distribuye bajo la Licencia Pública General Limitada de GNU (LGPL).
