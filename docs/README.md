# Escáner de Vulnerabilidades de Seguridad

Una herramienta impulsada por IA para detectar vulnerabilidades de seguridad en código fuente utilizando técnicas de aprendizaje automático.

## Descripción General

Este proyecto implementa un escáner de vulnerabilidades basado en aprendizaje automático que analiza archivos de código fuente y predice la probabilidad de vulnerabilidades de seguridad. El sistema utiliza análisis de código estático combinado con aprendizaje automático para identificar patrones de código potencialmente peligrosos.

## Características

- **Análisis impulsado por IA**: Utiliza clasificador Random Forest para predecir la probabilidad de vulnerabilidades
- **Soporte multi-lenguaje**: Compatible con archivos Python, JavaScript, TypeScript y Java
- **Análisis de código estático**: Aprovecha Lizard para métricas de complejidad y coincidencia de patrones
- **Escaneo local**: Realiza análisis en archivos locales sin enviar código a servidores externos
- **Pipeline de entrenamiento**: Pipeline completo para entrenar modelos en conjuntos de datos de vulnerabilidades
- **Minería de datos**: Herramientas para extraer datos de vulnerabilidades de repositorios Git

## Estructura del Proyecto

```
├── demo_scanner.py      # Escáner interactivo de vulnerabilidades
├── entrenamiento.py     # Pipeline de entrenamiento del modelo
├── mineria.py          # Minería de datos de repositorios
├── seguro.py           # Ejemplo de prácticas de código seguro
├── vulnerable.py       # Ejemplo de patrones de código vulnerable
├── dataset_local.csv   # Dataset de entrenamiento (ignorado por tamaño)
├── repos_descargados/  # Repositorios clonados para análisis
└── modelo_seguridad_final.pkl  # Archivo del modelo entrenado
```

## Instalación

1. Clona este repositorio:
```bash
git clone <repository-url>
cd lab1p2v2
```

2. Instala las dependencias requeridas:
```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn tqdm lizard pydriller flask
```

## Uso

### Inicio Rápido - Escáner de Vulnerabilidades

Ejecuta el escáner interactivo para analizar archivos individuales:

```bash
python demo_scanner.py
```

Ingresa la ruta a un archivo de código fuente cuando se solicite. El escáner mostrará:
- Estado de riesgo (SECURE/HIGH RISK)
- Porcentaje de probabilidad de vulnerabilidad
- Métricas detalladas

### Entrenar un Nuevo Modelo

Para entrenar un nuevo modelo con tu propio conjunto de datos:

```bash
python entrenamiento.py
```

Esto hará:
1. Cargar el conjunto de datos desde `dataset_local.csv`
2. Extraer características usando análisis estático
3. Entrenar un clasificador Random Forest
4. Guardar el modelo como `modelo_seguridad_final.pkl`
5. Generar métricas de rendimiento y matriz de confusión

### Minería de Datos de Vulnerabilidades

Para recopilar datos de entrenamiento de repositorios de código abierto:

```bash
python mineria.py
```

Esto hará:
- Clonar repositorios especificados
- Analizar mensajes de commit para palabras clave relacionadas con seguridad
- Extraer muestras de código antes/después de correcciones de seguridad
- Generar conjunto de datos etiquetado para entrenamiento

## Características del Modelo

El escáner analiza las siguientes características del código:

- **Líneas de Código (NLOC)**: Número de líneas sin comentarios
- **Complejidad Ciclomática**: Métricas de complejidad del código
- **Palabras Clave de Riesgo**: Presencia de funciones potencialmente peligrosas
- **Contenido del Código**: Vectorización TF-IDF del código fuente

### Patrones de Riesgo Detectados

- **Python**: `eval()`, `exec()`, `subprocess`, `os.system`, ejecución SQL
- **JavaScript**: `eval()`, `innerHTML`, `document.write`, `dangerouslySetInnerHTML`
- **Java**: Declaraciones SQL dinámicas, `Runtime.exec()`, concatenación de parámetros

## Ejemplos

### Código Seguro vs Vulnerable

El proyecto incluye archivos de ejemplo que demuestran:

- **seguro.py**: Prácticas de código seguro (consultas parametrizadas, validación de entrada, etc.)
- **vulnerable.py**: Patrones comunes de vulnerabilidades (inyección SQL, inyección de comandos, etc.)

## Rendimiento

El modelo entrenado logra:
- **Precisión**: Varía según el conjunto de datos (típicamente 85%+ en conjuntos balanceados)
- **Umbral de Riesgo**: Umbral de probabilidad del 40% para clasificación de ALTO RIESGO
- **Velocidad de Procesamiento**: Analiza archivos en milisegundos después de cargar el modelo

## Consideraciones de Seguridad

- Todo el análisis se realiza localmente
- No se transmite código a servicios externos
- Las predicciones del modelo son probabilísticas y deben verificarse manualmente
- La herramienta está diseñada para propósitos educativos y de pruebas de seguridad

## Contribuir

1. Haz fork del repositorio
2. Crea una rama de características
3. Realiza tus cambios
4. Agrega pruebas si es aplicable
5. Envía un pull request

## Licencia

Este proyecto es para propósitos educativos. Por favor, asegúrate de cumplir con las regulaciones de pruebas de seguridad relevantes en tu jurisdicción.

## Limitaciones

- El análisis estático no puede detectar todos los tipos de vulnerabilidades
- Las predicciones de aprendizaje automático pueden tener falsos positivos/negativos
- Requiere modelo pre-entrenado para operar
- Limitado a lenguajes de programación soportados

## Mejoras Futuras

- Soporte para lenguajes de programación adicionales
- Integración con pipelines CI/CD
- Análisis de código en tiempo real en IDEs
- Modelos de aprendizaje profundo mejorados
- Endpoint API para análisis remoto

## Solución de Problemas

### Problemas Comunes

1. **Archivo de modelo no encontrado**: Ejecuta `entrenamiento.py` para entrenar un nuevo modelo
2. **Dependencias faltantes**: Instala los paquetes requeridos usando pip
3. **Conjunto de datos muy grande**: Usa muestreo en el script de entrenamiento
4. **Problemas de memoria**: Reduce `SAMPLE_SIZE` en la configuración

### Consejos de Rendimiento

- Usa almacenamiento SSD para conjuntos de datos grandes
- Aumenta la RAM para procesar repositorios grandes
- Usa sistemas multi-núcleo para entrenamiento más rápido
- Cachea repositorios clonados para minería repetida

## Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio.