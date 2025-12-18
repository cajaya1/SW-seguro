# 🛡️ Setup Guide - Secure CI/CD Pipeline

## Configuración Completa del Proyecto

### Paso 1: Configuración de Ramas en GitHub

1. Ve a tu repositorio en GitHub
2. Crea las ramas necesarias:

```bash
# En tu repositorio local
git checkout -b dev
git push origin dev

git checkout -b test  
git push origin test

git checkout main
```

3. Configura **Branch Protection Rules**:

**Para rama `test`:**
- Settings → Branches → Add rule
- Branch name pattern: `test`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- Selecciona: `security-scan`, `test-and-merge`

**Para rama `main`:**
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass
- ✅ Require review from Code Owners

### Paso 2: Configurar Bot de Telegram

Sigue las instrucciones en [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md)

Agrega los secrets en GitHub:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### Paso 3: Configurar Despliegue Automático

#### Opción A: Render (Recomendado)

1. Crea cuenta en [render.com](https://render.com)
2. New → Web Service
3. Conecta tu repositorio de GitHub
4. Configuración:
   - **Name**: `secure-devops-demo`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

Render detectará automáticamente el Dockerfile.

#### Opción B: Railway

1. Crea cuenta en [railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo
3. Selecciona tu repositorio
4. Railway detectará automáticamente el Dockerfile
5. La app se desplegará en cada push a `main`

#### Opción C: Fly.io

```bash
# Instalar flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Desplegar
flyctl launch
flyctl deploy
```

### Paso 4: Subir el Modelo Entrenado

```bash
# Asegúrate de que el modelo esté en el repositorio
git add modelo_seguridad_final.pkl
git commit -m "Add trained ML model"
git push origin main
```

### Paso 5: Flujo de Trabajo

```bash
# 1. Trabaja en rama dev
git checkout dev
# ... haz cambios en app.py ...
git add app.py
git commit -m "Add new feature"
git push origin dev

# 2. Crea Pull Request de dev → test
gh pr create --base test --head dev --title "New feature" --body "Description"

# 3. El pipeline se ejecutará automáticamente:
# - ✅ Escaneo de seguridad con IA
# - ✅ Tests unitarios
# - ✅ Merge automático a test
# - ✅ Si todo pasa, merge a main
# - ✅ Despliegue automático

# 4. Recibirás notificaciones en Telegram en cada paso
```

### Paso 6: Verificar que Todo Funciona

1. **Test local del scanner:**
```bash
python scan_security.py app.py
```

2. **Test local de la app:**
```bash
python app.py
# Abre http://localhost:5000
```

3. **Test unitarios:**
```bash
pytest test_app.py -v
```

4. **Crear PR de prueba:**
```bash
# Modifica app.py con código seguro
git checkout dev
echo "# Safe comment" >> app.py
git add app.py
git commit -m "Test: safe change"
git push origin dev
gh pr create --base test --head dev
```

## Estructura del Proyecto

```
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml    # Pipeline CI/CD
├── app.py                         # Aplicación Flask
├── scan_security.py               # Scanner de seguridad con IA
├── modelo_seguridad_final.pkl     # Modelo ML entrenado
├── entrenamiento.py               # Script de entrenamiento
├── test_app.py                    # Tests unitarios
├── requirements.txt               # Dependencias de producción
├── requirements-dev.txt           # Dependencias de desarrollo
├── Dockerfile                     # Para despliegue
└── README.md                      # Documentación principal
```

## Troubleshooting

### El pipeline no se ejecuta
- Verifica que el archivo `.github/workflows/ci-cd-pipeline.yml` existe
- Asegúrate de que el PR es de `dev` → `test`

### Security scan falla
- Verifica que `modelo_seguridad_final.pkl` está en el repositorio
- Asegúrate de que las dependencias están instaladas

### Tests fallan
- Ejecuta `pytest test_app.py -v` localmente
- Verifica que Flask está instalado

### Telegram no envía mensajes
- Verifica los secrets `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`
- Prueba manualmente con curl

### Despliegue falla
- Verifica que `requirements.txt` está correcto
- Asegúrate de que el Dockerfile es válido
- Revisa los logs en Render/Railway

## Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Render Documentation](https://render.com/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
