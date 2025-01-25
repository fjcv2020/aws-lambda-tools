# Guía de Usuario: AWS Lambda Tools 🚀

## Índice
1. [Introducción](#introducción)
2. [Generador de Lambdas](#generador-de-lambdas)
3. [Debugger de Lambdas](#debugger-de-lambdas)
4. [Conceptos Básicos](#conceptos-básicos)
5. [Preguntas Frecuentes](#preguntas-frecuentes)

## Introducción

AWS Lambda Tools es un conjunto de herramientas que te ayuda a crear y mejorar funciones AWS Lambda. Está diseñada especialmente para desarrolladores que están comenzando con AWS Lambda.

### ¿Qué puedes hacer con esta herramienta?

1. **Crear nuevas funciones Lambda** paso a paso
2. **Analizar funciones existentes** para mejorarlas
3. **Generar código optimizado** siguiendo las mejores prácticas

## Generador de Lambdas

### Paso 1: Selección del Trigger

Un trigger es lo que hace que tu Lambda se ejecute. Es como decir "cuando pase X, haz Y".

#### Tipos de Triggers disponibles:

1. **S3 Upload (📁)**
   - Se usa cuando: Quieres procesar archivos automáticamente
   - Ejemplo: Redimensionar imágenes cuando se suben
   - Configuración necesaria: Nombre del bucket y prefijo (opcional)

2. **API Gateway (🌐)**
   - Se usa cuando: Quieres crear una API web
   - Ejemplo: Crear un endpoint para registrar usuarios
   - Configuración necesaria: Ruta y método HTTP

3. **Scheduled Event (⏰)**
   - Se usa cuando: Quieres que algo se ejecute periódicamente
   - Ejemplo: Hacer backups diarios
   - Configuración necesaria: Expresión cron o frecuencia

4. **SNS (📨)**
   - Se usa cuando: Quieres procesar notificaciones
   - Ejemplo: Enviar emails cuando llegan alertas
   - Configuración necesaria: ARN del topic SNS

5. **SQS (📬)**
   - Se usa cuando: Quieres procesar mensajes en cola
   - Ejemplo: Procesar pedidos en orden
   - Configuración necesaria: ARN de la cola SQS

### Paso 2: Configuración Específica

Cada trigger tiene sus propias opciones de configuración. La herramienta te guiará según el trigger que hayas elegido.

### Paso 3: Configuración Básica

#### Memoria (💾)
- **¿Qué es?** Cuánta RAM tendrá tu función
- **¿Cómo elegir?** 
  - 128MB: Tareas muy simples
  - 256MB: La mayoría de los casos
  - 512MB+: Procesamiento pesado

#### Tiempo máximo (⏱️)
- **¿Qué es?** Cuánto tiempo puede ejecutarse tu función
- **¿Cómo elegir?**
  - 30 segundos: Valor típico
  - 5-10 segundos: Respuestas rápidas (APIs)
  - 60+ segundos: Procesamiento largo

#### Variables de Entorno
- **¿Qué son?** Configuraciones que pueden cambiar sin tocar el código
- **Valores comunes:**
  - ENVIRONMENT: development/production
  - AWS_REGION: región donde se ejecuta
  - LOG_LEVEL: nivel de detalle de los logs

### Configuración Avanzada

#### 1. Concurrencia y Escalado
- **Reserved Concurrency:** Límite de ejecuciones simultáneas
- **Provisioned Concurrency:** Instancias pre-calentadas
- **¿Cuándo usar?** Cuando necesitas control preciso del rendimiento

#### 2. Manejo de Errores
- **Dead Letter Queue (DLQ):** Donde van los eventos fallidos
- **Reintentos:** Cuántas veces intentar si falla
- **¿Cuándo configurar?** Siempre que los errores sean críticos

#### 3. Observabilidad
- **X-Ray:** Para rastrear la ejecución
- **Logs:** Cuánto tiempo guardarlos
- **¿Por qué importante?** Para debuggear problemas

#### 4. Red (VPC)
- **Subnets:** Dónde se ejecuta la Lambda
- **Security Groups:** Reglas de firewall
- **¿Cuándo necesario?** Para acceder a recursos privados

#### 5. Empaquetado
- **ZIP vs Container:** Cómo empaquetar el código
- **Layers:** Bibliotecas compartidas
- **¿Cómo elegir?** ZIP para casos simples, Container para más control

## Debugger de Lambdas

### ¿Cómo usar el debugger?

1. **Subir/Pegar Código**
   - Puedes subir archivos o pegar el código directamente
   - Incluye el template SAM si lo tienes

2. **Análisis**
   - El sistema analizará:
     - Estructura del código
     - Problemas potenciales
     - Oportunidades de mejora
     - Uso de recursos

3. **Mejoras**
   - Recibirás sugerencias específicas
   - Código mejorado y optimizado
   - Explicaciones detalladas

## Conceptos Básicos

### ¿Qué es AWS Lambda?
- Servicio de computación serverless
- Ejecuta código sin gestionar servidores
- Pagas solo por el tiempo de ejecución

### ¿Qué es SAM?
- Serverless Application Model
- Framework para definir aplicaciones serverless
- Facilita el despliegue de Lambdas

## Preguntas Frecuentes

### ¿Cuánta memoria necesito?
Comienza con 256MB y ajusta según el rendimiento.

### ¿Qué timeout configurar?
Comienza con 30 segundos y ajusta según tus pruebas.

### ¿Necesito VPC?
Solo si necesitas acceder a recursos privados (ej: base de datos RDS).

### ¿Qué es un cold start?
El tiempo adicional la primera vez que se ejecuta tu Lambda.

### ¿Cómo reducir costos?
- Optimiza la memoria
- Reduce el tiempo de ejecución
- Usa Provisioned Concurrency si es necesario

## Recursos Adicionales

- [Documentación oficial de AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Guía de AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)
- [Mejores prácticas para Lambda](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) 