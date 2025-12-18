"""
Script Interactivo para Configurar Bot de Telegram
Prueba tu bot antes de configurar GitHub Secrets
"""

import sys
import requests
from urllib.parse import quote

def test_telegram_bot():
    print("=" * 80)
    print("🤖 CONFIGURACIÓN DE BOT DE TELEGRAM")
    print("=" * 80)
    
    print("\n📝 IMPORTANTE: No compartas tu token públicamente")
    print("   Este script solo se ejecuta localmente\n")
    
    # Obtener TOKEN
    print("Paso 1: TOKEN del Bot")
    print("-" * 80)
    token = input("Pega aquí tu TOKEN (de @BotFather): ").strip()
    
    if not token or len(token) < 20:
        print("❌ Token inválido. Debe ser algo como: 123456789:ABCdefGHIjklMNOpqrs")
        return
    
    # Obtener CHAT_ID
    print("\nPaso 2: Chat ID")
    print("-" * 80)
    chat_id = input("Pega aquí tu CHAT_ID (de @userinfobot): ").strip()
    
    if not chat_id or not chat_id.isdigit():
        print("❌ Chat ID inválido. Debe ser un número como: 123456789")
        return
    
    # Probar el bot
    print("\n" + "=" * 80)
    print("🧪 PROBANDO CONEXIÓN CON TELEGRAM...")
    print("=" * 80)
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    messages = [
        "✅ ¡Conexión exitosa! Tu bot de Telegram funciona correctamente.",
        "🔒 SW Seguro CI/CD Bot configurado",
        "📊 Listo para recibir notificaciones del pipeline"
    ]
    
    success_count = 0
    for i, message in enumerate(messages, 1):
        try:
            response = requests.post(
                url,
                data={"chat_id": chat_id, "text": message},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Mensaje {i}/3 enviado correctamente")
                success_count += 1
            else:
                print(f"❌ Error al enviar mensaje {i}: {response.text}")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            break
    
    print("\n" + "=" * 80)
    
    if success_count == len(messages):
        print("🎉 ¡ÉXITO! Tu bot está funcionando perfectamente")
        print("\n📱 Revisa tu Telegram, deberías ver 3 mensajes del bot\n")
        
        # Mostrar información para GitHub
        print("=" * 80)
        print("📋 CONFIGURACIÓN PARA GITHUB SECRETS")
        print("=" * 80)
        print("\nVe a: https://github.com/cajaya1/SW-seguro/settings/secrets/actions")
        print("\nCrea estos 2 secrets:\n")
        print("1. Secret Name: TELEGRAM_BOT_TOKEN")
        print(f"   Secret Value: {token[:10]}...{token[-5:]} (completo)")
        print(f"\n2. Secret Name: TELEGRAM_CHAT_ID")
        print(f"   Secret Value: {chat_id}")
        print("\n" + "=" * 80)
        
        # Guardar configuración (sin el token completo por seguridad)
        print("\n💾 ¿Quieres guardar esta configuración localmente?")
        print("   (Solo guardará el Chat ID, NO el token por seguridad)")
        save = input("   (s/n): ").lower().strip()
        
        if save == 's':
            with open('.telegram_config', 'w') as f:
                f.write(f"TELEGRAM_CHAT_ID={chat_id}\n")
                f.write(f"# TOKEN configurado pero no guardado por seguridad\n")
            print("✅ Configuración guardada en .telegram_config")
            
            # Agregar a .gitignore
            with open('.gitignore', 'a') as f:
                f.write("\n# Telegram config\n.telegram_config\n")
            print("✅ .telegram_config agregado a .gitignore")
        
    else:
        print("❌ Hubo problemas. Verifica:")
        print("   - El TOKEN es correcto (de @BotFather)")
        print("   - El CHAT_ID es correcto (de @userinfobot)")
        print("   - Tienes conexión a internet")
    
    print("\n" + "=" * 80)

def test_with_curl():
    """Genera comando curl para probar en terminal"""
    print("\n" + "=" * 80)
    print("🔧 MÉTODO ALTERNATIVO: Probar con curl")
    print("=" * 80)
    
    token = input("TOKEN: ").strip()
    chat_id = input("CHAT_ID: ").strip()
    
    if sys.platform == "win32":
        # PowerShell
        cmd = f'Invoke-RestMethod -Uri "https://api.telegram.org/bot{token}/sendMessage" -Method Post -Body @{{chat_id="{chat_id}"; text="Test desde PowerShell"}}'
        print("\n📋 Copia y pega este comando en PowerShell:\n")
        print(cmd)
    else:
        # Linux/Mac
        cmd = f'curl -s -X POST https://api.telegram.org/bot{token}/sendMessage -d chat_id={chat_id} -d text="Test desde terminal"'
        print("\n📋 Copia y pega este comando en tu terminal:\n")
        print(cmd)
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("\n¿Qué método prefieres?")
    print("1. Script interactivo (Python)")
    print("2. Comando curl/PowerShell")
    
    choice = input("\nElige (1/2): ").strip()
    
    if choice == "1":
        # Verificar requests
        try:
            import requests
            test_telegram_bot()
        except ImportError:
            print("\n❌ Necesitas instalar 'requests'")
            print("   Ejecuta: pip install requests")
            print("\n   O usa la opción 2 (curl/PowerShell)")
    elif choice == "2":
        test_with_curl()
    else:
        print("Opción inválida")
