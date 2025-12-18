# Configuración de Deployment en Render

## Pasos para configurar deployment automático:

### 1. Crear cuenta en Render
- Ve a: https://render.com/
- Sign up gratis con tu cuenta de GitHub

### 2. Crear nuevo Web Service
1. Click en "New +" → "Web Service"
2. Conecta tu repositorio: `cajaya1/SW-seguro`
3. Configuración:
   - **Name**: `sw-seguro-cicd`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: (dejar en blanco)
   - **Environment**: Docker
   - **Plan**: Free

### 3. Variables de entorno (opcional)
```
ENVIRONMENT=production
PORT=5000
```

### 4. Deploy automático
- Render detectará automáticamente el `Dockerfile`
- Cada push a `main` activará deployment automático
- URL pública: `https://sw-seguro-cicd.onrender.com`

### 5. Webhook para GitHub Actions (IMPORTANTE)
Después de crear el servicio:
1. Ve a Settings → Deploy Hook
2. Copia la URL del webhook
3. Agrégala como secret en GitHub: `RENDER_DEPLOY_HOOK`

### Alternativas:
- **Railway**: https://railway.app/
- **Fly.io**: https://fly.io/

## Verificación
Después del deployment, tu app estará en:
- Homepage: `https://tu-app.onrender.com/`
- Health: `https://tu-app.onrender.com/health`
- Status: `https://tu-app.onrender.com/api/status`

## Tiempo de deployment
- Primera vez: ~5-10 minutos
- Siguientes: ~2-3 minutos
- ⚠️ Free tier: La app "duerme" después de 15 min de inactividad
