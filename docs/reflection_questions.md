# Reflexiones sobre Diseño y Gestión de Pipelines de Datos

## Introducción

Este documento presenta preguntas de reflexión sobre los conceptos clave aprendidos al diseñar y gestionar pipelines de datos.

---

## 1 Diseño de Pipelines: División en Componentes

### Pregunta Central
¿Cómo decidió dividir un pipeline en componentes? ¿Qué criterios usó para definir las dependencias?

### Reflexión

En nuestro pipeline de ventas, decidimos dividir el trabajo en fases claramente separadas:

**¿Por qué dividir?**
- **Simplicidad**: Cada fase hace una cosa bien, en lugar de tenerlo todo en un solo proceso
- **Reutilización**: Componentes independientes pueden usarse en otros proyectos
- **Entendimiento**: Es más fácil explicar qué hace cada parte a nuevos miembros del equipo
- **Mantenimiento**: Si algo falla, sabemos exactamente dónde buscar el problema

**Criterio para dividir:**

1. **Por responsabilidad**: Cada componente tiene un propósito claro
   - Validación: ¿Son los datos correctos?
   - Transformación: ¿Cómo los preparamos?
   - Enriquecimiento: ¿Qué más información necesitamos?

2. **Por dependencias lógicas**: Un componente depende del anterior
   - No tiene sentido enriquecer datos que aún no están validados
   - No podemos cargar datos sin verificar calidad primero

3. **Por cambio independiente**: Si una regla de negocio cambia, ¿afecta a otros componentes?
   - Cambiar criterios de calidad ≠ cambiar lógica de transformación

---

## 2 Orquestación vs Ejecución

### Pregunta Central
¿Cuál es la diferencia entre orquestar un pipeline y ejecutar sus componentes individualmente?

### Reflexión

**Ejecución Individual:**
- Ejecutas componentes como tareas independientes
- Es como hacer cada paso de un receta manualmente sin planificar previamente.
- Alguien debe recordar qué hacer y en qué orden.
- Si falla un paso, se tiene que decidir qué hacer después.

**Orquestación:**
- Un "director" coordina todo el proceso
- Los componentes se ejecutan según un plan predefinido
- El director sabe qué hacer si algo falla
- Es automático y predecible

---

## 3 Manejo de Fallos: Estrategias de Resiliencia

### Pregunta Central
¿Qué estrategias implementaría para reintentos automáticos, continuación desde fallo y notificaciones escalonadas?

### 3.1 Reintentos Automáticos

**¿Por qué reintentar?**
- A veces los fallos son **temporales** (conexión a internet, servidor ocupado)
- Es más eficiente reintentar que escalar inmediatamente al equipo
- Reduce falsos positivos

**Estrategia de Reintentos:**

```
Intento 1: Fallido
  - Esperar 1 minuto
  
Intento 2: Fallido
  - Esperar 5 minutos
  
Intento 3: Fallido
  - Esperar 15 minutos
  
Intento 4: Fallido
  - Notificar al equipo
```

**¿Cuándo NO reintentar?**
- Datos inválidos (no van a ser válidos al segundo intento)
- Errores de lógica en el código
- Archivos que no existen

---

### 3.2 Continuación desde el Punto de Fallo

**¿Por qué es importante?**
- No reiniciar todo desde cero
- Ahorrar tiempo y recursos
- Procesos más eficientes

**Escenarios:**

```
Procesando 10 millones de registros:

Sin punto de continuación:
   Falla en registro 8M → Vuelves a procesar desde 0
   Tiempo total: 2 horas
   
Con punto de continuación:
   Falla en registro 8M → Continúas desde 8M
   Tiempo total: 15 minutos
```

**¿Cómo implementarlo?**

1. **Guardar progreso**: "Hemos procesado hasta registro 8M"
2. **Marcar completado**: Solo procesa registros 8M-10M
3. **Validar continuo**: Asegúrate de que los primeros datos son válidos


---

### 3.3 Notificaciones Escalonadas

**Niveles de Escalamiento:**

```
Nivel 1: Fallo Menor (Automático)
├─ Acción: Reintentar automáticamente
├─ Notificación: Log silencioso
└─ Urgencia: Baja

Nivel 2: Fallo Intermedio (Equipo Técnico)
├─ Acción: Notificar al técnico después de 2 fallos
├─ Notificación: Email
└─ Urgencia: Media

Nivel 3: Fallo Crítico (Directa)
├─ Acción: Notificación inmediata
├─ Notificación: SMS + Email + Reunión
└─ Urgencia: Alta
```


**Ventajas:**
- No molesta al equipo por problemas menores
- Escalado rápido si es serio
- Menos fatiga de alertas
- Respuesta apropiada a cada problema

---

## 4 Monitoreo: Métricas de Salud del Pipeline

### Pregunta Central
¿Qué métricas monitorearía para evaluar la salud del pipeline?

### Reflexión

No se trata solo de su funcionamiento, sino de qué tan bien funciona.

### Categorías de Métricas

**1. Rendimiento**
- **Tiempo de ejecución**: ¿Cuánto tarda cada fase?
  - Normal: 10 minutos
  - Alarma: > 30 minutos
  
- **Velocidad de procesamiento**: ¿Cuántas filas por minuto?
  - Antes: 100k filas/minuto
  - Después: 50k filas/minuto → ¡Algo anda lento!

**2. Calidad de Datos**
- **Completitud**: ¿Hay datos faltantes?
  - Meta: 95% de datos válidos
  - Si cae a 80% → Problema en datos origen
  
- **Duplicados**: ¿Se limpian correctamente?
  - Registros antes: 10M
  - Registros después: 9.8M
  - Duplicados encontrados: 200k
  
- **Variación**: ¿Los números cambian mucho?
  - Ventas ayer: $1M
  - Ventas hoy: $1.2M
  - Ventas pasado: $0.5M

**3. Confiabilidad**
- **Tasa de éxito**: ¿Qué % de ejecuciones son exitosas?
  - Meta: > 99%
  - Real: 98% → Casi bien, pero hay espacio para mejorar
  
- **Tiempo de reparación**: ¿Cuánto tarda en recuperarse de un fallo?
  - Fallo a las 9:00
  - Recuperado a las 9:15
  - MTTR (Mean Time To Repair): 15 minutos
  
- **Frecuencia de fallos**: ¿Con qué frecuencia falla?
  - 1 fallo por mes → Aceptable
  - 5 fallos por día → Crisis

**4. Negocio**
- **Coste por GB procesado**: ¿Estamos siendo eficientes?
  - Presupuesto: $0.10 por GB
  - Real: $0.08 por GB
  
- **Data Freshness**: ¿Cuán actualiza está la información?
  - Los datos son de:
    - Hoy (fresco)
    - Ayer (aceptable)
    - Semana pasada (problema)
  
- **Impacto de negocio**: ¿Afecta las decisiones?
  - Si reportes se retrasan - Decisiones incorrectas
  - Si datos tienen errores - Pérdida de dinero


---

## 5 Costos: Optimización en la Nube

### Pregunta Central
¿Cómo optimizaría los costos de ejecución en la nube?

### Reflexión

La nube es poderosa pero puede ser cara si no se gestiona bien. Es como tener un taxi que te lleva a donde quieras, pero pagas por cada minuto que funciona.

### 5.1 Entender Dónde Va el Dinero

```
Presupuesto Mensual: $1000

Distribución típica:
├─ Almacenamiento (Data): 20% = $200
├─ Procesamiento (CPUs): 60% = $600
├─ Transferencia de datos: 10% = $100
├─ Servicios adicionales: 10% = $100
```

**Pregunta:** ¿Dónde gastamos más?
 - **Respuesta:** Procesamiento es el 60%
 - **Conclusión:** Ahí debemos optimizar primero

---

### 5.2 Estrategias de Optimización

**Estrategia 1: Procesar Solo lo Necesario**

```
Antes: Procesar 100 millones de registros cada día
   - Tiempo: 1 hora
   - Costo: $50/día = $1500/mes
   - Necesidad: 90% de esos datos es histórico
   
Después: Solo procesar últimas 24h de datos
   - Tiempo: 10 minutos
   - Costo: $5/día = $150/mes
   - Ahorro: $1350/mes
```

**Estrategia 2: Automatizar Según Demanda**

```
Escala automática:
├─ 6:00-9:00 AM (Pico): 50 computadoras (máximo)
├─ 9:00-17:00 (Normal): 10 computadoras
├─ 17:00-6:00 (Mínimo): 2 computadoras
│
Beneficio: Solo pagas por lo que usas
```

**Estrategia 3: Usar Almacenamiento Más barato**

```
Datos recientes (< 30 días):
   → Almacenamiento rápido: $0.02/GB/mes
   $200/mes para 10 TB
   
Datos históricos (> 30 días):
   → Almacenamiento lento pero barato: $0.004/GB/mes
   $40/mes para 10 TB
   
Ahorro: $160/mes solo en almacenamiento
```

**Estrategia 4: Reservas a Largo Plazo**

```
Pago bajo demanda: $100/mes
vs
Compra anual: $70/mes (30% de descuento)

Con 12 meses: $100×12 = $1200 vs $70×12 = $840
Ahorro: $360/año
(Si sabes que lo necesitarás 12 meses)
```

---

### 5.3 Preguntas para Auditoría de Costos

Hacer estas preguntas regularmente:

1. **¿Necesitamos toda esta capacidad?**
   - ¿Están todos los servidores siendo usados?
   - ¿Hay picos específicos o es estable?

2. **¿Podemos comprar diferente?**
   - Instancias reservadas vs bajo demanda
   - Spot instances para trabajos no críticos

3. **¿Estamos almacenando basura?**
   - ¿Logs de hace 2 años?
   - ¿Datos de prueba sin limpiar?

4. **¿Hay ineficiencias de código?**
   - ¿Queries pobres que usan más poder?
   - ¿Duplicación de procesamiento?

5. **¿Qué es lo más caro?**
   - Priorizar optimizar lo que cuesta más



## Declaración de uso de IA:

Se utilizó inteligencia artificial durante la realización del laboratorio para saber cúal es la estructura de los diagramas requerido, pues fue un tema que no se tocó en clase, y por lo tanto, fueron conceptos nuevos. De ahí en adelante, el contenido de estos fue creado con apoyo de la IA para temas de tecnologías, lenguaje técnico e información que tuviese sentido en cuanto a números o valores correspondientes estrategias de escalabilidad (Que era lo que se pedía).