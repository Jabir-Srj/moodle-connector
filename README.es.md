---
name: moodle-connector
description: "Cliente Moodle REST API, descargador masivo y servidor MCP para integración con Claude Code"
metadata: { "author": "Jabir Iliyas Suraj-Deen, Sebastian Guevara M.", "license": "MIT", "homepage": "https://github.com/Jabir-Srj/moodle-connector", "repository": "https://github.com/Jabir-Srj/moodle-connector.git", "tags": ["moodle", "education", "lms", "api", "batch-download", "mcp", "claude-code"] }
---

> [English](README.md) | **Español**

# Moodle Connector

**Cliente Moodle REST API completo con descarga masiva y soporte del protocolo MCP para Claude Code y OpenCode.**

## Características

**Acceso completo a la API de Moodle**
- Listar cursos, consultar notas, seguir tareas
- Obtener materiales, fechas límite, anuncios
- Descargar archivos con caché agresiva

**Soporte Microsoft SSO / MFA**
- Mobile Launch Flow automatizado (el mismo que usa la app oficial de Moodle)
- Compatible con cualquier proveedor SSO: Microsoft Azure AD, Google, SAML, etc.
- El navegador se abre para el login interactivo y se cierra automáticamente al capturar el token

**Múltiples modos de integración**
- **CLI:** `python moodle_connector.py courses`
- **Librería Python:** `from moodle_connector import MoodleConnector`
- **Protocolo MCP:** Integración nativa con Claude Code, OpenCode y OpenClaw

**Descargador masivo genérico**
- Configuración basada en JSON (sin modificar código)
- Compatible con cualquier módulo de Moodle
- Organización automática por nombre de curso

**Seguridad**
- Credenciales cifradas (PBKDF2 + Fernet)
- Gestión de tokens integrada
- Sin secretos en el historial de git
- Licencia MIT

## Instalación

Una vez instalado con `clawhub install moodle-connector`:

```bash
cd ./skills/moodle-connector
pip install -r requirements.txt
python -m playwright install chromium
```

## Inicio rápido

### 1. Configurar

```bash
cp config.template.json config.json
# Editar config.json: establecer base_url con la URL de tu Moodle
```

### 2. Login (SSO / MFA)

```bash
MOODLE_CRED_PASSWORD=cualquier-password python moodle_connector.py login
```

Se abrirá una ventana del navegador. Completa tu login de Microsoft (u otro SSO) y el MFA normalmente - la ventana se cierra automáticamente al capturar el token. Deberías ver:

```
# ✅ Authentication Successful
- User: Tu Nombre
- Site: Tu Sitio Moodle
- Moodle version: 4.x.x
```

> Si tu instancia permite login con usuario/contraseña directamente (sin SSO), también puedes usar:
> `python moodle_connector.py login --username tu@email.com --user-password tucontraseña`

### 3. Usar la CLI

```bash
python moodle_connector.py courses        # Listar todos los cursos
python moodle_connector.py grades         # Consultar notas
python moodle_connector.py assignments    # Ver tareas con fechas límite
python moodle_connector.py announcements  # Anuncios de los cursos
python moodle_connector.py materials --course-id 12345
python moodle_connector.py deadlines      # Eventos próximos del calendario
python moodle_connector.py download "https://tu-moodle.ejemplo.com/..." --output archivo.pdf
python moodle_connector.py summary        # Exportación completa en markdown
```

### 4. Usar como librería Python

```python
from moodle_connector import MoodleConnector
from pathlib import Path

connector = MoodleConnector(
    config_path=Path('config.json'),
    password='contraseña-de-cifrado'
)

courses = connector.courses()
grades = connector.grades()
assignments = connector.assignments()
materials = connector.materials()
deadlines = connector.deadlines()
announcements = connector.announcements()
content = connector.summary()

# Descarga con caché
file_content = connector.download("https://...")
```

### 5. Descarga masiva (cualquier módulo)

```bash
cp downloads.example.json downloads.json
# Editar downloads.json para agregar módulos y URLs de archivos
python batch_downloader.py
```

**Estructura de salida:**
```
downloads/
├── Nombre_Modulo_1/
│   ├── archivo1.pdf
│   ├── archivo2.zip
│   └── ...
└── Nombre_Modulo_2/
    ├── clase.pdf
    └── ...
```

## Tampermonkey Token Helper

Si el conector corre en un servidor headless (sin pantalla), obtén el token desde un PC o Mac con navegador y copialo al servidor. Instala el userscript incluido en esa máquina:

1. Instala [Tampermonkey](https://www.tampermonkey.net/) en tu navegador
2. Abre Tampermonkey - Crear nuevo script - pega el contenido de [`moodle_token_helper.user.js`](moodle_token_helper.user.js)
3. Navega a tu sitio Moodle con sesion activa
4. Haz click en el boton **"Get Token"** (esquina inferior derecha)
5. Copia el token y pegalo en `config.json` bajo `web_service_token`

El script usa `GM_xmlhttpRequest` para llamar al endpoint Mobile Launch con tus cookies de sesion activas e intercepta el redirect `moodlemobile://` sin salir de la pagina.

Para agregar otras instancias Moodle, agrega lineas `@match` y `@connect` en el header del script.

## Cómo funciona la autenticación

Este conector usa el **Mobile Launch Flow** de Moodle, el mismo mecanismo que usa la app oficial de Moodle. Funciona con cualquier proveedor SSO sin necesitar credenciales de API ni configuración especial en el servidor.

**Flujo:**
1. El navegador navega a `/admin/tool/mobile/launch.php`
2. Si no hay sesión activa, Moodle redirige al proveedor SSO (ej: Microsoft)
3. El usuario completa el login + MFA de forma interactiva
4. El SSO devuelve a Moodle, que emite un redirect `moodlemobile://token=<base64>`
5. El conector intercepta este redirect, decodifica el token y cierra el navegador

El token se guarda en un archivo cifrado (`credentials.enc`) y se reutiliza hasta que expira.

## Integración MCP (Claude Code / OpenCode / OpenClaw)

**REQUERIDO:** Configurar la variable de entorno `MOODLE_CRED_PASSWORD` antes de iniciar Claude Code.

Agregar a tu `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "moodle-connector": {
      "command": "python",
      "args": ["./skills/moodle-connector/mcp_server.py"],
      "env": {
        "MOODLE_CRED_PASSWORD": "tu-contraseña-de-cifrado"
      }
    }
  }
}
```

**Importante:** Reemplazar `tu-contraseña-de-cifrado` con la misma contraseña usada al correr `login`.

Reiniciar Claude Code. Las 8 funciones de Moodle estarán disponibles como herramientas MCP nativas:
- `courses()` - Listar cursos inscritos
- `grades()` - Obtener notas
- `assignments()` - Obtener tareas
- `materials()` - Obtener materiales del curso
- `deadlines()` - Obtener próximas fechas límite
- `announcements()` - Obtener novedades del curso
- `download(url, output?)` - Descargar archivos
- `summary()` - Exportación completa de datos

## Configuración

### Token de Moodle (`config.json`)
```json
{
  "moodle": {
    "base_url": "https://tu-moodle.ejemplo.com",
    "web_service_token": ""
  },
  "cache": {
    "api_ttl_seconds": 300
  }
}
```

Dejar `web_service_token` vacío para usar el flujo SSO automatizado. Completarlo manualmente solo si ya tienes un token.

### Descarga masiva (`downloads.json`)
```json
{
  "downloads": [
    {
      "module": "Aprendizaje Automático",
      "course_id": 44864,
      "files": [
        {
          "name": "Semana1.zip",
          "url": "https://tu-moodle.ejemplo.com/webservice/pluginfile.php/..."
        }
      ]
    }
  ]
}
```

## Requisitos

- Python 3.10+
- requests ≥2.31.0
- cryptography ≥41.0.0
- playwright ≥1.40.0
- mcp ≥0.1.0 (para el servidor MCP)

## Instancias de Moodle compatibles

Probado con:
- Taylor's University (mytimes.taylors.edu.my)
- Universidad Técnica Federico Santa María (aula.usm.cl) - SSO Microsoft Azure AD
- Debería funcionar con cualquier instancia Moodle 3.x+

## Notas de seguridad

- `MOODLE_CRED_PASSWORD` es **obligatorio** - sin valores por defecto hardcodeados
- **Sanitización de errores:** El servidor MCP sanitiza los errores, sin filtración de detalles internos
- **Credenciales cifradas:** PBKDF2 (480K iteraciones) + cifrado Fernet
- **Apto para headless:** Usar la variable de entorno `MOODLE_CRED_PASSWORD` para automatización
- **Seguro para git:** Nunca hacer commit de `config.json` con tokens reales
- **Sin telemetría:** Sin transmisión de datos externos ni de logs

## Solución de problemas

### El navegador se abre pero nunca se cierra
El redirect del token no fue capturado. Verifica que tu universidad o institución educativa tenga activada la aplicación movil

### "Invalid parameter value detected" en la API de calendario
Usar `assignments()` en su lugar, obtiene la misma información de fechas límite.

### Token expirado / se pide login de nuevo
Eliminar `credentials.enc` y ejecutar `python moodle_connector.py login` nuevamente.

### Descarga de archivo detenida
Verifica tu conexión a internet . Aumentar el timeout en el código o limpiar la caché: `rm -rf cache/`

## Licencia

MIT - Ver el archivo LICENSE para más detalles. Eres libre de usar, modificar y distribuir este software.

## Contribuir

¡Las contribuciones son bienvenidas! Por favor:
1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad
3. Envía un pull request
4. Acepta licenciar tu trabajo bajo GPLv3

## Autores

**Jabir Iliyas Suraj-Deen** - autor original
- GitHub: https://github.com/Jabir-Srj
- Email: jabirsrj8@protonmail.com
- Taylor's University, Kuala Lumpur, Malaysia

**Sebastian Guevara M.** - SSO Mobile Launch Flow, soporte multi-instancia
- GitHub: https://github.com/SebaG20xx
- Email: contacto@sebag20xx.cl
- Universidad Técnica Federico Santa María, Viña del Mar, Chile

---

**GitHub:** https://github.com/Jabir-Srj/moodle-connector
**Release:** v1.1.0 (26 de marzo de 2026)
