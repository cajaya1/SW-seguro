import json
import logging
import re
from datetime import datetime

# Configuración de log (común en código seguro)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidadorDatos:
    """
    Clase utilitaria para validar estructuras de datos de usuarios.
    Utiliza expresiones regulares precompiladas para eficiencia y seguridad.
    """
    
    # Patrón seguro para email (solo caracteres permitidos)
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def __init__(self, data_json):
        self.raw_data = data_json
        self.clean_data = {}
        self.errors = []

    def parsear_json(self):
        """Intenta parsear el string JSON de forma segura."""
        try:
            if isinstance(self.raw_data, str):
                self.clean_data = json.loads(self.raw_data)
            elif isinstance(self.raw_data, dict):
                self.clean_data = self.raw_data
            else:
                self.errors.append("Formato de entrada no válido")
                return False
            return True
        except json.JSONDecodeError:
            logger.error("Error al decodificar JSON")
            self.errors.append("JSON malformado")
            return False

    def validar_email(self, campo='email'):
        """Valida el formato del correo sin usar eval() ni comandos."""
        email = self.clean_data.get(campo, '')
        
        if not email or not isinstance(email, str):
            self.errors.append(f"Campo {campo} faltante o inválido")
            return False
            
        # Validación con Regex (Segura y Estándar)
        if self.EMAIL_PATTERN.match(email):
            logger.info(f"Email válido: {email}")
            return True
        else:
            logger.warning(f"Intento de email inválido: {email}")
            self.errors.append("Formato de email incorrecto")
            return False

    def obtener_resultado(self):
        """Retorna el estado de la validación."""
        if not self.errors:
            return {"status": "ok", "data": self.clean_data}
        return {"status": "error", "errors": self.errors}

# Ejemplo de uso seguro (Entry point)
if __name__ == "__main__":
    entrada_usuario = '{"nombre": "Carlos", "email": "carlos@espe.edu.ec"}'
    
    validador = ValidadorDatos(entrada_usuario)
    if validador.parsear_json():
        validador.validar_email()
    
    print(validador.obtener_resultado())

    