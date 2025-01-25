import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import yaml
import json
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

############################
# Funciones de Generación
############################
def generate_sam_template(config):
    """Genera el template SAM basado en la configuración proporcionada."""
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Transform": "AWS::Serverless-2016-10-31",
        "Description": "Lambda generada con AWS Lambda Generator Pro",
        "Resources": {
            "MyFunction": {
                "Type": "AWS::Serverless::Function",
                "Properties": {
                    "Handler": f"handler.{config['handler_name']}",
                    "Runtime": "python3.9",
                    "MemorySize": config["memory"],
                    "Timeout": config["timeout"],
                    "Environment": {
                        "Variables": {}
                    }
                }
            }
        }
    }
    
    # Agregar configuración específica según el trigger
    if config.get("trigger_type") == "S3 Upload":
        template["Resources"]["MyFunction"]["Properties"]["Events"] = {
            "S3Event": {
                "Type": "S3",
                "Properties": {
                    "Bucket": {"Ref": config.get("bucket_name")},
                    "Events": ["s3:ObjectCreated:*"]
                }
            }
        }
    elif config.get("trigger_type") == "API Gateway":
        template["Resources"]["MyFunction"]["Properties"]["Events"] = {
            "ApiEvent": {
                "Type": "Api",
                "Properties": {
                    "Path": config.get("route", "/"),
                    "Method": config.get("http_method", "GET")
                }
            }
        }
    
    # Agregar variables de entorno
    if config.get("env_vars"):
        template["Resources"]["MyFunction"]["Properties"]["Environment"]["Variables"] = config["env_vars"]
    
    return yaml.dump(template, sort_keys=False)

def get_llm():
    """Configura y retorna la instancia de LangChain."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.secrets.get("OPENAI_API_KEY", None)
    
    if not api_key:
        st.error("No se ha configurado la API key de OpenAI. Por favor, configúrala en el archivo .env o en los secrets de Streamlit.")
        st.stop()
    
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key
    )

def show_help(title, content):
    """Muestra un expander con información de ayuda."""
    with st.expander(f"ℹ️ {title}"):
        st.markdown(content)

############################
# Configuración de la página
############################
st.set_page_config(
    page_title="AWS Lambda Generator Pro",
    page_icon="⚡",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF9900;
        color: white;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .env-var-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .step-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .help-text {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

############################
# Selección de Herramienta
############################
st.title("⚡ AWS Lambda Tools")

tool_selection = st.radio(
    "Selecciona la herramienta que necesitas:",
    ["🛠️ Generador de Lambdas", "🔍 Debugger de Lambdas"],
    help="Escoge entre crear una nueva Lambda o analizar/debuggear una existente"
)

if tool_selection == "🛠️ Generador de Lambdas":
    st.markdown("""
    ## Generador de AWS Lambda
    #### 🎯 ¿Qué es esto?
    Esta herramienta te ayuda a crear funciones AWS Lambda paso a paso, sin necesidad de ser un experto.
    Una Lambda es como una función en la nube que se ejecuta cuando algo específico sucede.
    """)
    
    ############################
    # 1. Selección de Trigger
    ############################
    with st.container():
        st.markdown("""
        ## Paso 1: ¿Cuándo quieres que se ejecute tu Lambda? 🎯
        Selecciona el evento que activará tu función:
        """)
        
        show_help("¿Qué es un Trigger?", """
        Un trigger es el evento que hace que tu Lambda se ejecute. Es como decir "cuando pase X, haz Y":

        🗂️ **S3 Upload**: 
        - Se ejecuta cuando alguien sube un archivo
        - Útil para procesar archivos (imágenes, documentos, etc.)
        
        🌐 **API Gateway**: 
        - Se ejecuta cuando alguien hace una petición web
        - Útil para crear APIs y servicios web
        
        ⏰ **Scheduled Event**: 
        - Se ejecuta en momentos específicos
        - Útil para tareas programadas (backups, limpieza, etc.)
        
        📨 **SNS**: 
        - Se ejecuta cuando llega un mensaje o notificación
        - Útil para procesar notificaciones
        
        📬 **SQS**: 
        - Se ejecuta cuando hay mensajes en una cola
        - Útil para procesar tareas en orden
        """)

        trigger_descriptions = {
            "S3 Upload": "📁 Cuando se sube un archivo",
            "API Gateway": "🌐 Cuando alguien hace una petición web",
            "Scheduled Event": "⏰ Cuando quieres que se ejecute periódicamente",
            "SNS": "📨 Cuando llega una notificación",
            "SQS": "📬 Cuando hay mensajes en una cola",
        }

        selected_trigger = st.selectbox(
            "Selecciona cuándo quieres que se ejecute tu Lambda:",
            list(trigger_descriptions.keys()),
            format_func=lambda x: trigger_descriptions[x]
        )

    ############################
    # 2. Configuración específica
    ############################
    config_values = {"trigger_type": selected_trigger}

    with st.container():
        st.markdown("""
        ## Paso 2: Configuración específica 🔧
        Configura los detalles específicos según el tipo de evento:
        """)

        if selected_trigger == "S3 Upload":
            show_help("¿Cómo configurar S3?", """
            📁 **Configuración para archivos:**
            
            1. **Bucket**: Es como una carpeta en la nube donde se guardan tus archivos
               - Debe ser un nombre único en todo AWS
               - Solo letras minúsculas, números y guiones
               - Ejemplo: `mi-empresa-archivos`
            
            2. **Prefijo**: Es como una subcarpeta (opcional)
               - Te permite procesar solo ciertos archivos
               - Ejemplo: `uploads/` o `imagenes/`
            
            ⚡ **Ejemplo de uso:**
            - Bucket: `mi-empresa-fotos`
            - Prefijo: `uploads/`
            - → La Lambda se ejecutará cuando se suban archivos a `uploads/` en el bucket `mi-empresa-fotos`
            """)
            
            config_values["bucket_name"] = st.text_input(
                "Nombre del Bucket (carpeta en la nube)",
                value="mi-empresa-archivos",
                help="Nombre único donde se guardarán tus archivos"
            )
            config_values["prefix"] = st.text_input(
                "Prefijo (subcarpeta - opcional)",
                help="Ejemplo: 'uploads/' solo procesará archivos en esa carpeta"
            )

        elif selected_trigger == "API Gateway":
            show_help("¿Cómo configurar el API?", """
            🌐 **Configuración para API web:**
            
            1. **Ruta**: Es la dirección web de tu API
               - Debe empezar con `/`
               - Ejemplo: `/api/usuarios` o `/procesar-datos`
            
            2. **Método**: Es el tipo de operación
               - GET: Para obtener datos
               - POST: Para crear/enviar datos
               - PUT: Para actualizar datos
               - DELETE: Para eliminar datos
            
            ⚡ **Ejemplo de uso:**
            - Ruta: `/api/usuarios`
            - Método: `POST`
            - → La Lambda se ejecutará cuando alguien envíe datos a `https://tu-api.com/api/usuarios`
            """)
            
            config_values["route"] = st.text_input(
                "Ruta de tu API",
                value="/api/v1/datos",
                help="La dirección web donde estará disponible tu API"
            )
            config_values["http_method"] = st.selectbox(
                "¿Qué tipo de operación quieres permitir?",
                ["GET", "POST", "PUT", "DELETE"],
                help="GET para obtener datos, POST para enviar datos"
            )

    ############################
    # 3. Configuración común
    ############################
    st.markdown("""
    ## Paso 3: Configuración básica ⚙️
    Estos son los ajustes básicos que necesita tu Lambda:
    """)

    show_help("¿Qué significan estos ajustes?", """
    ⚙️ **Configuración básica explicada:**

    1. **Memoria**: 
       - Cuánta memoria tendrá tu Lambda
       - Más memoria = más rápido pero más costoso
       - Para empezar, 128MB está bien para tareas simples

    2. **Tiempo máximo**: 
       - Cuánto tiempo puede ejecutarse tu Lambda
       - Para empezar, 30 segundos suele ser suficiente
       - Aumenta si tu tarea necesita más tiempo

    3. **Variables de entorno**:
       - Son como configuraciones que puedes cambiar sin tocar el código
       - Ejemplos comunes ya están preconfigurados
    """)

    config_values["handler_name"] = "lambda_handler"  # Simplificamos quitando esta opción

    col1, col2 = st.columns(2)
    with col1:
        config_values["memory"] = st.select_slider(
            "💾 Memoria (MB)",
            options=[128, 256, 512, 1024, 2048],
            value=256,
            help="Cuánta memoria necesita tu Lambda. Para empezar, 256MB está bien."
        )

    with col2:
        config_values["timeout"] = st.select_slider(
            "⏱️ Tiempo máximo (segundos)",
            options=[5, 10, 30, 60, 300],
            value=30,
            help="Cuánto tiempo puede ejecutarse tu Lambda como máximo"
        )

    # Simplificamos las variables de entorno
    st.markdown("### Variables de configuración")
    show_help("Variables de configuración", """
    Son valores que puedes cambiar sin modificar el código. Por ejemplo:
    - El ambiente (desarrollo/producción)
    - La región de AWS
    - El nivel de logs (qué tan detallados son)
    """)

    # Variables de entorno predefinidas más simples
    config_values["env_vars"] = {
        "ENVIRONMENT": st.selectbox("Ambiente", ["development", "production"], help="¿Es para desarrollo o producción?"),
        "AWS_REGION": "us-east-1",  # Simplificamos dejando un valor por defecto
        "LOG_LEVEL": "INFO"  # Simplificamos dejando un valor por defecto
    }

    ############################
    # 4. Lógica de negocio
    ############################
    st.markdown("""
    ## Paso 4: ¿Qué quieres que haga tu Lambda? 💡
    Describe en lenguaje natural qué quieres que haga tu función:
    """)

    show_help("Ejemplos de Lógica", """
    🎯 **Ejemplos según el tipo de trigger:**

    **Para S3 Upload:**
    - "Procesar imágenes y reducir su tamaño"
    - "Convertir archivos CSV a JSON"
    - "Analizar documentos PDF y extraer texto"

    **Para API Gateway:**
    - "Crear un endpoint que registre usuarios en una base de datos"
    - "Consultar el estado de un pedido"
    - "Procesar pagos y enviar confirmación"

    **Para Scheduled Events:**
    - "Hacer backup de una base de datos cada día"
    - "Enviar reportes por email semanalmente"
    - "Limpiar archivos temporales antiguos"
    """)

    logic_description = st.text_area(
        "Describe qué quieres que haga tu Lambda",
        help="Explica en español, con tus propias palabras, qué debe hacer la función",
        height=100
    )

    ############################
    # 5. Generación de código
    ############################
    if st.button("🚀 Generar Código"):
        with st.spinner("Generando código personalizado..."):
            # Primero, generamos la lógica específica con LangChain
            logic_prompt = f"""Genera el código Python para una función AWS Lambda que haga lo siguiente:
            
            Descripción: {logic_description}
            Tipo de trigger: {selected_trigger}
            
            La función debe:
            1. Seguir las mejores prácticas de AWS Lambda
            2. Incluir manejo de errores y logging apropiado
            3. Ser eficiente y clara
            4. Incluir las importaciones necesarias
            5. Incluir comentarios explicativos
            6. NO incluir código de ejemplo o plantillas
            7. Implementar SOLO la funcionalidad solicitada
            
            Importante:
            - El código debe ser una única implementación coherente
            - NO incluir múltiples versiones o ejemplos
            - NO incluir código comentado o alternativas
            - Asegurarse de que todas las funciones estén correctamente definidas
            - Incluir solo las dependencias estrictamente necesarias
            
            Estructura el código en este orden:
            1. Imports
            2. Configuración de logging
            3. Configuración de clientes AWS necesarios
            4. Función principal lambda_handler
            5. Funciones auxiliares necesarias
            """

            llm = get_llm()
            logic_response = llm.invoke(logic_prompt)
            
            # Generar el código completo
            code_template = logic_response.content

            # Generar template SAM
            sam_template = generate_sam_template(config_values)

            # Mostrar resultados
            st.markdown("## Resultado Final 🎉")
            
            # Análisis con LangChain
            with st.spinner("Analizando el código generado..."):
                review_template = """Analiza y explica el siguiente código de AWS Lambda:

                DESCRIPCIÓN DE LA FUNCIONALIDAD:
                {description}

                CÓDIGO PYTHON:
                {python_code}

                TEMPLATE SAM:
                {sam_template}

                Por favor, proporciona una explicación clara y estructurada:
                1. 📝 Explicación general del código y su funcionamiento
                2. 🔍 Desglose de cada parte importante
                3. 🎯 Cómo cumple con los requisitos solicitados
                4. ⚠️ Consideraciones importantes a tener en cuenta
                
                Usa un lenguaje simple y claro, enfocado a desarrolladores con conocimientos básicos."""

                prompt = ChatPromptTemplate.from_template(review_template)
                chain = prompt | llm

                response = chain.invoke({
                    "description": logic_description,
                    "python_code": code_template,
                    "sam_template": sam_template
                })

            # Mostrar el código y la explicación
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📄 Código Python (handler.py)")
                st.code(code_template, language="python")
                st.download_button(
                    "⬇️ Descargar handler.py",
                    code_template,
                    file_name="handler.py",
                    mime="text/plain"
                )

            with col2:
                st.subheader("🏗️ Template SAM (template.yaml)")
                st.code(sam_template, language="yaml")
                st.download_button(
                    "⬇️ Descargar template.yaml",
                    sam_template,
                    file_name="template.yaml",
                    mime="text/plain"
                )

            # Mostrar la explicación
            st.markdown("### 📚 Explicación del Código")
            st.info(response.content)

            # Agregar instrucciones de despliegue
            st.markdown("""
            ### 🚀 Próximos Pasos
            
            1. Descarga los archivos generados
            2. Colócalos en una carpeta de tu proyecto
            3. Abre una terminal en esa carpeta
            4. Ejecuta los siguientes comandos:
            ```bash
            sam build
            sam deploy --guided
            ```
            """)

elif tool_selection == "🔍 Debugger de Lambdas":
    st.markdown("""
    ## AWS Lambda Debugger
    #### 🎯 ¿Qué es esto?
    Esta herramienta te ayuda a analizar y mejorar tus funciones Lambda existentes.
    Puedes subir tu código o pegarlo directamente para obtener un análisis detallado y sugerencias de mejora.
    """)

    # Selector de método de entrada
    input_method = st.radio(
        "¿Cómo quieres proporcionar tu código?",
        ["📋 Pegar Código", "📁 Subir Archivos"],
        help="Escoge cómo quieres proporcionar el código para analizar"
    )

    handler_content = None
    template_content = None

    if input_method == "📋 Pegar Código":
        st.markdown("### Código Python (handler.py)")
        handler_content = st.text_area(
            "Pega tu código Python aquí",
            height=300,
            help="Pega el contenido de tu archivo handler.py"
        )

        st.markdown("### Template SAM (opcional)")
        template_content = st.text_area(
            "Pega tu template SAM aquí (opcional)",
            height=200,
            help="Pega el contenido de tu archivo template.yaml si lo tienes"
        )

    else:  # Subir Archivos
        uploaded_handler = st.file_uploader("Sube tu archivo handler.py", type=["py"])
        uploaded_template = st.file_uploader("Sube tu template.yaml (opcional)", type=["yaml", "yml"])

        if uploaded_handler is not None:
            handler_content = uploaded_handler.getvalue().decode("utf-8")
        if uploaded_template is not None:
            template_content = uploaded_template.getvalue().decode("utf-8")

    if handler_content:
        st.markdown("### 📄 Código a Analizar")
        st.code(handler_content, language="python")

        # Obtener instancia de LLM una sola vez
        llm = get_llm()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Analizar Código"):
                with st.spinner("Analizando tu código..."):
                    analysis_prompt = """Analiza el siguiente código de AWS Lambda y proporciona un informe detallado:

                    CÓDIGO PYTHON:
                    {handler_code}

                    {template_section}

                    Por favor, proporciona un análisis detallado que incluya:

                    1. 🔍 Análisis de Código
                       - Estructura y organización
                       - Manejo de errores
                       - Logging y monitoreo
                       - Seguridad

                    2. ⚠️ Problemas Potenciales
                       - Problemas de rendimiento
                       - Fugas de memoria
                       - Problemas de seguridad
                       - Malas prácticas

                    3. ✅ Recomendaciones
                       - Mejoras específicas de código
                       - Optimizaciones
                       - Mejores prácticas
                       - Patrones recomendados

                    4. 📊 Recursos y Costos
                       - Uso de memoria
                       - Tiempo de ejecución
                       - Costos estimados
                       - Optimización de recursos

                    Usa un lenguaje claro y proporciona ejemplos específicos cuando sea necesario."""

                    template_section = f"\nTEMPLATE SAM:\n{template_content}" if template_content else ""
                    
                    analysis = llm.invoke(analysis_prompt.format(
                        handler_code=handler_content,
                        template_section=template_section
                    ))

                    st.markdown("### 📋 Análisis Detallado")
                    st.info(analysis.content)

        with col2:
            if st.button("🔧 Generar Código Mejorado"):
                with st.spinner("Generando versión mejorada..."):
                    improvement_prompt = """Basándote en el código proporcionado, genera una versión mejorada que solucione los problemas identificados:

                    CÓDIGO ORIGINAL:
                    {code}

                    Genera una versión mejorada que:
                    1. Solucione los problemas identificados
                    2. Implemente las mejores prácticas
                    3. Optimice el rendimiento
                    4. Mejore la seguridad
                    
                    Proporciona el código completo y mejorado, junto con comentarios explicativos.
                    El código debe ser una única implementación coherente, sin alternativas ni código comentado."""

                    improved_code = llm.invoke(improvement_prompt.format(code=handler_content))
                    
                    st.markdown("### 📝 Código Mejorado Sugerido")
                    st.code(improved_code.content, language="python")
                    
                    # Botones para descargar y copiar
                    st.download_button(
                        "⬇️ Descargar Código Mejorado",
                        improved_code.content,
                        file_name="handler_improved.py",
                        mime="text/plain"
                    )
                    
                    if st.button("📋 Copiar al Portapapeles"):
                        st.write(
                            f'<script>navigator.clipboard.writeText(`{improved_code.content}`)</script>', 
                            unsafe_allow_html=True
                        )
                        st.success("¡Código copiado al portapapeles!")

if __name__ == "__main__":
    st.sidebar.markdown("""
    ### 📚 Documentación Útil
    - [AWS Lambda](https://docs.aws.amazon.com/lambda/)
    - [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/)
    - [API Gateway](https://docs.aws.amazon.com/apigateway/)
    """) 