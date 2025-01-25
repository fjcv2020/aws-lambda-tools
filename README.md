# AWS Lambda Tools 🚀

Una herramienta todo en uno para crear, analizar y mejorar funciones AWS Lambda. Diseñada para hacer el desarrollo serverless más accesible para todos los niveles de experiencia.

## ¿Qué es esto? 🤔

AWS Lambda Tools es un conjunto de herramientas que incluye:

1. **🛠️ Generador de Lambdas**
   - Creación guiada paso a paso
   - Múltiples tipos de triggers
   - Configuración avanzada simplificada
   - Generación de código optimizado

2. **🔍 Debugger de Lambdas**
   - Análisis de código existente
   - Detección de problemas
   - Sugerencias de mejora
   - Optimización automática

## Características ✨

- 📝 Generación de código Python para AWS Lambda
- 🏗️ Plantillas SAM (Serverless Application Model)
- 🎯 Múltiples tipos de triggers soportados
- 🤖 Análisis de código con IA
- 📚 Documentación detallada y ejemplos
- 🎨 Interfaz intuitiva y amigable

## Requisitos Previos 📋

1. Python 3.9 o superior
2. Cuenta de AWS
3. AWS CLI configurado
4. SAM CLI instalado
5. API Key de OpenAI

## Instalación 🔧

1. Clonar el repositorio:
```bash
git clone https://github.com/fjcv2020/aws-lambda-tools.git
cd aws-lambda-tools
```

2. Crear y activar entorno virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   - Crea un archivo `.env` en la raíz del proyecto
   - Añade tu API key de OpenAI:
```
OPENAI_API_KEY=tu_api_key_aquí
```

## Uso 🚀

1. Iniciar la aplicación:
```bash
streamlit run app.py
```

2. Acceder a través del navegador:
```
http://localhost:8501
```

3. Seleccionar la herramienta que necesitas:
   - Generador de Lambdas: Para crear nuevas funciones
   - Debugger de Lambdas: Para analizar y mejorar código existente

4. Seguir el asistente paso a paso

## Documentación 📚

- [Guía de Usuario](docs/GUIA_USUARIO.md)
- [Documentación de AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Guía de AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)

## Contribuir 🤝

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto 📧

Francisco Javier Camacho Vargas - [LinkedIn](https://www.linkedin.com/in/franciscojaviercamachovargas/)

Link del proyecto: [https://github.com/fjcv2020/aws-lambda-tools](https://github.com/fjcv2020/aws-lambda-tools)

## Agradecimientos 🙏

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://langchain.com/)
- [OpenAI](https://openai.com/) 