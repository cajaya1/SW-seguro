# 🔒 SW Seguro - Sistema de Detección de Vulnerabilidades con IA

[![CI/CD Pipeline](https://github.com/cajaya1/SW-seguro/actions/workflows/ci-cd-pipeline.yml/badge.svg)](https://github.com/cajaya1/SW-seguro/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sistema de detección automática de vulnerabilidades de seguridad en código Python, JavaScript y Java utilizando Machine Learning y análisis basado en reglas. Desarrollado como parte del proyecto académico "Pipeline CI/CD Seguro con Integración de IA".

## 📋 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Documentación](#documentación)
- [CI/CD Pipeline](#cicd-pipeline)
- [Vulnerabilidades Detectadas](#vulnerabilidades-detectadas)
- [Licencia](#licencia)

## ✨ Características

- **Detección ML + Reglas**: Combina Random Forest con análisis basado en patrones regex
- **9 Tipos de Vulnerabilidades**: SQL Injection, XSS, Command Injection, Code Injection, Path Traversal, Deserialization, Weak Crypto, Hardcoded Secrets, Unsafe File Operations
- **Localización Exacta**: Indica línea de código específica y código vulnerable
- **Severidad Clasificada**: CRITICAL, HIGH, MEDIUM, LOW
- **Recomendaciones**: Sugerencias específicas de corrección
- **CI/CD Integrado**: GitHub Actions con bloqueo automático de PRs vulnerables
- **Notificaciones Telegram**: Alertas en tiempo real del pipeline
- **3 Lenguajes**: Python, JavaScript, Java

## 📁 Estructura del Proyecto

```
lab1p2v2/
├── src/                          # Código fuente principal
│   ├── model/                    # Entrenamiento del modelo ML
│   │   ├── entrenamiento.py      # Script de entrenamiento con Grid Search
│   │   └── mineria.py            # Extracción de datos de repositorios
│   ├── scanner/                  # Motor de escaneo
│   │   ├── scan_security.py      # Scanner principal para CI/CD
│   │   └── vulnerability_detector.py  # Detección detallada de vulnerabilidades
│   └── app/                      # Aplicación web demo
│       └── app.py                # Flask app para deployment
│
├── examples/                     # Ejemplos de código
│   ├── secure.py                 # Código seguro
│   └── vulnerable.py             # Código con vulnerabilidades
│
├── tests/                        # Suite de tests
│   ├── test_app.py               # Tests de la aplicación Flask
│   ├── test_sql_injection.py     # Casos de prueba SQL Injection
│   ├── test_xss_path.py          # Casos de prueba XSS y Path Traversal
│   └── test_command_crypto.py    # Casos de prueba Command Injection
│
├── demos/                        # Scripts de demostración
│   ├── demo_scanner.py           # Scanner interactivo
│   └── demo_comprehensive_scan.py # Demo completa multi-archivo
│
├── data/                         # Datos y modelos
│   ├── modelo_seguridad_final.pkl  # Modelo Random Forest entrenado
│   ├── dataset_contraste.csv     # Dataset balanceado (6580 registros)
│   └── vulnerability_report.txt  # Reporte de ejemplo
│
├── docs/                         # Documentación completa
│   ├── README.md                 # Documentación principal (español)
│   ├── USAGE.md                  # Guía de uso
│   ├── SETUP_GUIDE.md            # Guía de configuración
│   ├── TELEGRAM_SETUP.md         # Configuración del bot Telegram
│   └── VULNERABILITY_DETECTION.md # Detección detallada
│
├── notebooks/                    # Jupyter notebooks
│   └── Entrenamiento_Modelo.ipynb # Análisis y visualización
│
├── repos_descargados/            # Repositorios para entrenamiento
│   ├── django/                   # Framework web Python
│   ├── flask/                    # Microframework Python
│   ├── keras/                    # ML library
│   └── requests/                 # HTTP library
│
├── .github/workflows/            # GitHub Actions
│   └── ci-cd-pipeline.yml        # Pipeline completo de 3 etapas
│
├── .gitignore                    # Archivos ignorados
├── Dockerfile                    # Configuración Docker
├── requirements.txt              # Dependencias producción
├── requirements-dev.txt          # Dependencias desarrollo
└── reparar_dataset_contraste.py  # Script de limpieza de datos
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- Git
- pip

### Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/cajaya1/SW-seguro.git
cd SW-seguro

# Crear entorno virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Para desarrollo
pip install -r requirements-dev.txt
```

## 💻 Uso Rápido

### 1. Scanner Interactivo

```bash
python demos/demo_scanner.py
```

Ingresa la ruta del archivo a analizar y obtendrás un reporte detallado con:
- Estado del archivo (SECURE / HIGH RISK)
- Probabilidad de vulnerabilidad
- Métricas de complejidad
- Vulnerabilidades específicas encontradas
- Líneas exactas y recomendaciones

### 2. Escaneo de Directorio (CI/CD)

```bash
# Escanear archivo individual
python src/scanner/scan_security.py examples/vulnerable.py

# Escanear directorio completo
python src/scanner/scan_security.py src/

# Salida JSON para automatización
cat security_scan_results.json
```

### 3. Demo Completa

```bash
python demos/demo_comprehensive_scan.py
```

Analiza múltiples archivos de ejemplo y genera reporte completo.

### 4. Entrenar Modelo

```bash
# Con Grid Search (recomendado)
python src/model/entrenamiento.py

# El modelo se guardará en data/modelo_seguridad_final.pkl
```

## 📚 Documentación

La documentación completa está en la carpeta `docs/`:

- **[README.md](docs/README.md)** - Documentación completa en español
- **[USAGE.md](docs/USAGE.md)** - Guía de uso detallada
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Configuración paso a paso
- **[TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md)** - Configuración bot Telegram
- **[VULNERABILITY_DETECTION.md](docs/VULNERABILITY_DETECTION.md)** - Sistema de detección

## 🔄 CI/CD Pipeline

El proyecto incluye un pipeline completo de 3 etapas:

### Etapa 1: Security Scan
- Escaneo automático con IA
- Detección de vulnerabilidades
- Comentarios en PR con detalles
- Bloqueo de merge si hay vulnerabilidades

### Etapa 2: Tests & Merge
- Ejecución de tests unitarios
- Merge automático a rama `test`
- Notificaciones de fallas

### Etapa 3: Deploy
- Build de Docker
- Despliegue automático a producción
- Notificación de éxito/fallo

### Configuración

```bash
# 1. Configurar secrets en GitHub
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id

# 2. Crear ramas
git checkout -b dev
git push origin dev
git checkout -b test
git push origin test

# 3. Configurar branch protection
# Settings → Branches → Add rule para 'test' y 'main'
```

## 🐛 Vulnerabilidades Detectadas

| Tipo | Severidad | Ejemplo |
|------|-----------|---------|
| SQL Injection | HIGH | `cursor.execute(f"SELECT * FROM users WHERE id={user_id}")` |
| XSS | HIGH | `return f"<h1>Welcome {username}</h1>"` |
| Command Injection | CRITICAL | `os.system(f"ping {user_input}")` |
| Code Injection | CRITICAL | `eval(user_input)` |
| Path Traversal | HIGH | `open(request.args.get('file'))` |
| Deserialization | CRITICAL | `pickle.loads(untrusted_data)` |
| Weak Crypto | MEDIUM | `hashlib.md5(password)` |
| Hardcoded Secrets | HIGH | `API_KEY = "sk-1234567890"` |
| Unsafe File Ops | MEDIUM | `os.remove(user_file)` |

## 📊 Rendimiento del Modelo

- **Accuracy**: ~79.64% (objetivo: 82%+)
- **ROC-AUC**: ~88.01%
- **F1-Score**: ~79.79%
- **Registros de entrenamiento**: 6,580 (balanceado 50/50)
- **Features**: 7 métricas + TF-IDF (2500 features)
- **Algoritmo**: Random Forest con Grid Search

## 🤝 Contribución

Este es un proyecto académico. Para contribuciones:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

El pipeline CI/CD automáticamente analizará tu código.

## 👥 Autores

- **Carlos Jaya** - [cajaya1](https://github.com/cajaya1)

## 📄 Licencia

Este proyecto es parte de un trabajo académico de la ESPE (Escuela Politécnica del Ejército).

## 🎓 Proyecto Académico

**Título**: Desarrollo e Implementación de un Pipeline CI/CD Seguro con integración de IA para la Detección Automática de Vulnerabilidades

**Institución**: ESPE (Escuela Politécnica del Ejército)

**Fecha de Entrega**: 17 de Diciembre, 2025

**Restricciones**: No se permite uso de LLMs para detección (solo ML tradicional)

---

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!
