
# Manual Técnico de PlanifiCash

## 1. Objetivos del proyecto
- **Facilitar el control financiero personal**  
  Permitir a jóvenes y trabajadores independientes llevar un registro claro y sencillo de sus ingresos y gastos.
- **Incentivar el uso constante**  
  Ofrecer una interfaz intuitiva, visualmente atractiva y personalizada, que motive la entrada de datos diaria.
- **Apoyar la toma de decisiones responsables**  
  Generar reportes y alertas que ayuden al usuario a identificar patrones de gasto y oportunidades de ahorro.

---

## 2. Descripción del proyecto
PlanifiCash es una aplicación web full‑stack que ofrece a cada usuario:
- **Front‑end en React**: SPA construida con Create React App, usando React Router para navegación y Hooks para estado. Estilos con Tailwind CSS y componentes accesibles.
- **Dashboard** con gráficos de evolución de saldo, categorías de gasto y tendencias.
- **Registro de transacciones** (ingresos y egresos) por categorías personalizables.
- **Alertas** por email o notificaciones push cuando se exceden límites predefinidos.
- **Exportación** de datos a CSV/PDF para análisis externo.
- **Back‑end en Python** (Flask/FastAPI) desplegado en Docker, expone una API REST segura con JWT.

---

## 3. Arquitectura implementada

```plaintext
┌────────────────────────────────────────────────────────────────────────┐
│                             PlanifiCash                                │
│                                                                        │
│  React Front‑end    ↔   Amazon API Gateway   ↔   Dockerized Python API │
│                                                                        │
│  (SPA, Tailwind)       (throttling, JWT)        (Flask/FastAPI)        │
│                                                                        │
│      ↓                        ↓                       ↓                │
│                                                                        │
│ AWS Lambda–Insertar  AWS Lambda–Analizar        AWS Lambda–Trigger S3  │
│      ↓                        ↓                       ↓                │
│   DynamoDB                DynamoDB           Amazon S3 (backups, imgs) │
│                                                       ↓                │
│                                           AWS Rekognition (opcional)   │
└────────────────────────────────────────────────────────────────────────┘


```

1.  **Front‑end (React)**
    
    -   SPA con Create React App.
        
    -   React Router para rutas, Context API para estado global.
        
    -   Conexión a API Gateway para CRUD de transacciones.
        
2.  **Docker**
    
    -   Imagen que empaqueta la API REST en Python con todas sus dependencias.
        
    -   Base para despliegues en AWS ECS, EC2 o servicios serverless que soporten contenedores.
        
3.  **Amazon API Gateway**
    
    -   Exposición de rutas `POST /transacciones`, `GET /reportes`, etc.
        
    -   Validación de JWT y límites de petición configurados (throttling).
        
4.  **AWS Lambda**
    
    -   **InsertarTransaccion**: procesa peticiones de inserción, valida datos y escribe en DynamoDB.
        
    -   **AnalizarPatrones**: ejecuta análisis de datos (por ejemplo, patrones de gasto) y guarda resultados en DynamoDB.
        
    -   **ProcesarS3** (Trigger): al subir archivos/respaldos en S3, dispara procesamiento (p. ej. extracción de recibos).
        
5.  **Amazon DynamoDB**
    
    -   Tabla principal: clave compuesta `(usuarioId, timestamp)`.
        
    -   Índices secundarios globales para consultas por categoría o monto.
        
6.  **Amazon S3**
    
    -   Almacenamiento de **backups**, imágenes de recibos y documentos del usuario.
        
    -   Evento de bucket dispara Lambda de procesamiento adicional.
        
7.  **Amazon Rekognition** (opcional)
    
    -   Extracción de texto y montos desde imágenes de recibos para registro automático.
        

----------


## 4. Presupuesto estimado

| Recurso                         | Cantidad/Mes              | Costo aprox. USD    |
|---------------------------------|---------------------------|---------------------|
| EC2 t3.micro (Docker API)       | 720 horas                 | 8,50 $              |
| Amazon API Gateway              | 2 millones de llamadas    | 7,00 $ (3,50/M)     |
| AWS Lambda                      | 3 millones de invocaciones| 0,60 $ (0,20/M)     |
| Amazon S3                       | 50 GB almacenamiento      | 1,15 $ (0,023/GB)   |
| Amazon DynamoDB                 | 5 WCU / 5 RCU, 10 GB      | 20,00 $             |
| Amazon Rekognition (opcional)   | 1,000 análisis            | 1,00 $              |
| Transferencia de datos (salida) | 50 GB                     | 4,50 $ (0,09/GB)    |
| **Total aprox. mensual**        |                           | **≈ 42 USD**        |

*Precios referenciales según tarifas AWS en la región US-East (N. Virginia) a junio 2025.*

---

## 5. Breve investigación de los servicios utilizados

| Servicio               | Descripción                                                                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **React**              | Biblioteca JavaScript utilizada para crear interfaces web reactivas y eficientes mediante componentes reutilizables y gestión sencilla del estado.|
| **Docker**             | Plataforma que permite empaquetar aplicaciones en contenedores, facilitando el despliegue y garantizando la misma operación en distintos entornos.|
| **Amazon API Gateway** | Servicio administrado por AWS para crear, mantener y proteger APIs REST, permitiendo manejo de autenticación, seguridad, throttling y monitoreo. |
| **AWS Lambda**         | Servicio de computación serverless de AWS que ejecuta funciones en respuesta a eventos sin necesidad de administrar infraestructura de servidores.|
| **Amazon S3**          | Almacenamiento en la nube altamente escalable, seguro y durable, ideal para guardar backups, documentos e imágenes del usuario.                  |
| **Amazon DynamoDB**    | Base de datos NoSQL de AWS, completamente gestionada, de alto rendimiento, escalabilidad y baja latencia, ideal para almacenar registros frecuentes como transacciones financieras.|
| **Amazon Rekognition** | Servicio de AWS basado en inteligencia artificial que permite analizar imágenes para extraer texto, objetos y patrones, facilitando procesos automatizados como la lectura de recibos.|

---


