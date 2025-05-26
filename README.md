# IA Adaptiera

Sistema de inteligencia artificial para la gestión y automatización de procesos de adaptación.

## Estructura del Proyecto

```
ia_adaptiera/
│
├── 📁 app/              # Aplicación principal
├── 📁 agents/           # Agentes de IA
├── 📁 services/         # Servicios externos
├── 📁 core/             # Núcleo del sistema
├── 📁 tools/            # Herramientas de utilidad
├── 📁 utils/            # Utilidades generales
├── 📁 tests/            # Pruebas unitarias
└── 📁 data/             # Datos y configuraciones
```

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

1. Copiar `.env.example` a `.env`
2. Configurar las variables de entorno necesarias

## Ejecución

```bash
python run.py
```

## Desarrollo

- Ejecutar pruebas: `pytest`
- Formatear código: `black .`
- Verificar tipos: `mypy .`
- Linting: `flake8` 