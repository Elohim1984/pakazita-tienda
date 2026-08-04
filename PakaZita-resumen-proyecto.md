# PakaZita — Resumen del proyecto (para GitHub Copilot)

## ⚠️ Importante
Este proyecto es Node.js + Express, NO Python/Flask. Si recibes sugerencias que mencionen `requirements.txt`, `gunicorn`, `Flask`, `SQLAlchemy` o `Alembic`, son de otro proyecto y no aplican — ignóralas.

## Qué es
PakaZita es una tienda en línea de fruta fresca con:
- Catálogo público de productos
- Carrito y formulario de pedido (sin pago en línea; el cliente paga en efectivo al recibir y el pedido se confirma vía WhatsApp)
- Panel de administración protegido por una contraseña compartida

## Stack tecnológico
- Backend: Node.js + Express (`server.js`, carpeta `routes/`)
- Frontend: HTML/CSS/JS plano (sin framework) en `public/`
- Base de datos: Supabase (PostgreSQL gestionado), usando `@supabase/supabase-js`
- Hosting: Render.com (Web Service, plan Free)
- Repositorio: GitHub — `Elohim1984/pakazita-tienda`
- Dominio: `pakazita.com` (registrado en HostGator). La app está hospedada en Render — HostGator no aloja la app.

## Estructura de archivos (resumen)
```
pakazita-node/
├── server.js              # Servidor Express principal: rutas para /api/productos y /api/pedidos
├── package.json           # Dependencias: express, @supabase/supabase-js, cookie-session, dotenv, etc.
├── supabase-schema.sql    # SQL para crear tablas: productos, pedidos, pedido_items
├── .env.example           # Plantilla para variables de entorno
├── lib/
│   ├── supabase.js        # Cliente de Supabase (usa SUPABASE_URL y SUPABASE_SERVICE_KEY en el servidor)
│   ├── auth.js            # Middleware requireAdmin (protege /admin)
│   └── styles.js          # Helpers de CSS compartido
├── routes/
│   └── admin.js           # Rutas del panel admin: login, pedidos, productos (CRUD)
└── public/
    └── index.html         # Sitio público: catálogo + carrito + formulario de pedido
```

## Variables de entorno requeridas (configurar en Render, no commitear)
| Variable | Propósito |
|---|---|
| `SUPABASE_URL` | URL del proyecto Supabase (Project Settings → API) |
| `SUPABASE_SERVICE_KEY` | Clave "service_role" (secreta) de Supabase — solo en servidor, nunca exponer al navegador |
| `SUPABASE_ANON_KEY` | Clave pública anon para uso en frontend (si es necesario) |
| `ADMIN_PASSWORD` | Contraseña compartida para acceder al panel admin (`/admin`) |
| `SESSION_SECRET` | String largo aleatorio para firmar cookies de sesión |
| `NODE_ENV` | Poner `production` en deploy |
| `PORT` | Opcional — Render gestiona el puerto automáticamente |

Notas de seguridad
- Nunca comitees `SUPABASE_SERVICE_KEY` ni `SESSION_SECRET`. Guárdalos solo como variables de entorno en Render.
- Usa `SUPABASE_SERVICE_KEY` únicamente en el servidor (rutas backend). Para llamadas desde el cliente usa `SUPABASE_ANON_KEY` con políticas RLS adecuadas.

## Deploy en Render — comandos recomendados
- Build Command: `npm install`
- Start Command: `npm start`
- Asegúrate de que `package.json` incluye:
  "scripts": { "start": "node server.js" }

(Si usas Procfile en lugar del Start Command, usa: `web: node server.js`.)

## Estado actual del despliegue
- ✅ Código subido a GitHub (`Elohim1984/pakazita-tienda`)
- ✅ Proyecto Supabase creado (nombre: `pakazita`) y `supabase-schema.sql` aplicado
- ⏳ Render Web Service (`pakazita-tienda`) casi listo — pendientes las variables de entorno
- ⏳ `pakazita.com` actualmente apunta a un servicio antiguo en Render; el dominio personalizado debe moverse al nuevo servicio después de verificarlo

## Qué ayuda se necesita para terminar
1. Añadir las variables de entorno requeridas en Render (SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_ANON_KEY, ADMIN_PASSWORD, SESSION_SECRET, NODE_ENV=production).
2. Confirmar que Build Command (`npm install`) y Start Command (`npm start`) son correctos.
3. Verificar que el servidor puede conectar a Supabase (sin errores de conexión en logs).
4. Realizar una prueba end-to-end básica: crear un producto en la BD y colocar un pedido desde el sitio público.
5. Mover el dominio personalizado `pakazita.com` del servicio viejo al nuevo:
   - Quitar el dominio del servicio antiguo (Dashboard → old service → Settings → Custom Domains → Remove).
   - Añadir el dominio al servicio nuevo (Dashboard → new service → Settings → Custom Domains → Add).
   - Actualizar registros DNS en HostGator si Render lo indica (CNAME/A records).
6. Opcional: habilitar HTTPS, cookies seguras, rate limiting, validación de inputs, helmet y logging.

## Checklist rápido (para quien termine el despliegue)
- [ ] Añadir variables de entorno en Render
- [ ] Confirmar `npm install` y `npm start` en Build & Start commands
- [ ] Revisar logs en vivo para conexión exitosa a Supabase
- [ ] Ejecutar flujo crear-producto + realizar-pedido
- [ ] Mover el dominio `pakazita.com` al nuevo servicio en Render
- [ ] Comitear cualquier migración o archivos de configuración necesarios y pushearlos

---
