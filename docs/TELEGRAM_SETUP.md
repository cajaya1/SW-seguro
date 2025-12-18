# Configuración del Bot de Telegram

## Pasos para crear y configurar el bot:

### 1. Crear el Bot con BotFather

1. Abre Telegram y busca `@BotFather`
2. Envía el comando `/newbot`
3. Sigue las instrucciones:
   - Nombre del bot: `SecureDevOps Bot` (o el que prefieras)
   - Username: `tu_nombre_securedevops_bot` (debe terminar en `bot`)
4. Guarda el **TOKEN** que te proporciona

### 2. Obtener tu Chat ID

1. Busca el bot `@userinfobot` en Telegram
2. Envíale `/start`
3. Te responderá con tu **Chat ID**, guárdalo

### 3. Configurar GitHub Secrets

Ve a tu repositorio en GitHub:
1. Settings → Secrets and variables → Actions
2. Click en "New repository secret"
3. Agrega estos dos secrets:

**Secret 1:**
- Name: `TELEGRAM_BOT_TOKEN`
- Value: El token que te dio BotFather (ej: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

**Secret 2:**
- Name: `TELEGRAM_CHAT_ID`
- Value: Tu Chat ID (ej: `123456789`)

### 4. Verificar que funciona

Envía un mensaje de prueba desde terminal:

```bash
curl -s -X POST https://api.telegram.org/bot<TU_TOKEN>/sendMessage \
  -d chat_id=<TU_CHAT_ID> \
  -d text="✅ Bot de Telegram configurado correctamente!"
```

## Mensajes que recibirás:

- 🔍 Inicio de escaneo de seguridad
- ✅ Código seguro / ❌ Código vulnerable  
- 🧪 Inicio de tests
- ✅ Tests pasados / ❌ Tests fallidos
- 🔀 Merge completado
- 🚀 Despliegue iniciado
- ✅ Despliegue exitoso

## Ejemplo de uso manual:

```python
import requests

TOKEN = "tu_token_aqui"
CHAT_ID = "tu_chat_id"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

send_telegram("🎉 ¡Hola desde Python!")
```
