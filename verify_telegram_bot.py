"""
Script de Verificación del Bot de Telegram
Verifica que el bot pueda enviar mensajes correctamente
"""

import sys
from pathlib import Path

# Configuración
TOKEN = "8383412326:AAHlVutXOpKFsK0_LgPJ2SsnypFeZc8Y6D4"
CHAT_ID = "8481801863"

def test_bot_powershell():
    """Genera comandos PowerShell para probar el bot"""
    
    print("=" * 80)
    print("🤖 VERIFICACIÓN DEL BOT DE TELEGRAM")
    print("=" * 80)
    
    print("\n📋 INFORMACIÓN DEL BOT:")
    print(f"   Bot Name: SW Seguro CI/CD Bot")
    print(f"   Username: @sw_seguro_cicd_bot")
    print(f"   Bot URL: https://t.me/sw_seguro_cicd_bot")
    print(f"   Token: {TOKEN[:15]}...{TOKEN[-5:]}")
    print(f"   Chat ID: {CHAT_ID}")
    
    print("\n" + "=" * 80)
    print("⚠️  PASO PREVIO REQUERIDO")
    print("=" * 80)
    print("\nAntes de enviar mensajes, debes:")
    print("1. Abrir Telegram")
    print("2. Buscar: @sw_seguro_cicd_bot")
    print("3. Click en 'START' o enviar /start")
    print("4. Volver aquí y presionar Enter")
    
    input("\n▶ Presiona Enter cuando hayas hecho START en el bot...")
    
    print("\n" + "=" * 80)
    print("🧪 ENVIANDO MENSAJES DE PRUEBA")
    print("=" * 80)
    
    # PowerShell commands para probar
    commands = [
        {
            "name": "Test 1: Mensaje simple",
            "cmd": f'$token = "{TOKEN}"; $chatId = "{CHAT_ID}"; Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body @{{chat_id=$chatId; text="✅ Test 1: Bot funcionando correctamente"}}'
        },
        {
            "name": "Test 2: Notificación de Pipeline",
            "cmd": f'$token = "{TOKEN}"; $chatId = "{CHAT_ID}"; $text = "🔍 Security Scan Started%0ARepository: SW-seguro%0ABranch: dev%0AAuthor: carlos"; Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body @{{chat_id=$chatId; text=$text}}'
        },
        {
            "name": "Test 3: Notificación de Éxito",
            "cmd": f'$token = "{TOKEN}"; $chatId = "{CHAT_ID}"; $text = "✅ DEPLOYMENT SUCCESSFUL%0AEnvironment: Production%0AStatus: Live%0AURL: https://sw-seguro.onrender.com"; Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body @{{chat_id=$chatId; text=$text}}'
        }
    ]
    
    print("\nEjecutando tests...\n")
    
    for i, test in enumerate(commands, 1):
        print(f"\n{test['name']}:")
        print("-" * 80)
        
        # Ejecutar con subprocess
        import subprocess
        try:
            result = subprocess.run(
                ["powershell", "-Command", test['cmd']],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Mensaje {i} enviado correctamente")
                print(f"   Respuesta: {result.stdout[:100]}")
            else:
                print(f"❌ Error al enviar mensaje {i}")
                print(f"   Error: {result.stderr[:200]}")
                
        except Exception as e:
            print(f"❌ Error de ejecución: {e}")
    
    print("\n" + "=" * 80)
    print("📱 REVISA TU TELEGRAM")
    print("=" * 80)
    print("\nDeberías ver 3 mensajes del bot.")
    print("Si no los ves, verifica que hiciste START en el bot.\n")

def generate_github_config():
    """Genera la configuración para GitHub"""
    
    print("\n" + "=" * 80)
    print("📋 CONFIGURACIÓN PARA GITHUB SECRETS")
    print("=" * 80)
    
    print("\n🔗 Ve a: https://github.com/cajaya1/SW-seguro/settings/secrets/actions")
    print("\nCrea estos 2 secrets:\n")
    
    print("─" * 80)
    print("SECRET 1:")
    print("─" * 80)
    print(f"Name:  TELEGRAM_BOT_TOKEN")
    print(f"Value: {TOKEN}")
    print()
    
    print("─" * 80)
    print("SECRET 2:")
    print("─" * 80)
    print(f"Name:  TELEGRAM_CHAT_ID")
    print(f"Value: {CHAT_ID}")
    print()
    
    print("=" * 80)
    print("\n✅ Una vez configurados, tu pipeline enviará notificaciones automáticamente\n")

if __name__ == "__main__":
    try:
        import subprocess
        test_bot_powershell()
        generate_github_config()
    except KeyboardInterrupt:
        print("\n\n⚠️ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPuedes probar manualmente con este comando en PowerShell:")
        print(f'\n$token = "{TOKEN}"; $chatId = "{CHAT_ID}"; Invoke-RestMethod -Uri "https://api.telegram.org/bot$token/sendMessage" -Method Post -Body @{{chat_id=$chatId; text="Test manual"}}')
