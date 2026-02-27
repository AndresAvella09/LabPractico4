# Dependencias del Pipeline de Procesamiento de Ventas

## Visión General

Este documento describe todas las dependencias entre los componentes del pipeline de procesamiento de datos de ventas.

---

## Dependencias del Pipeline

### 1. **Validación**
**Requiere:**
- Esquema versionado (`data/schemas/sales_schema_v1.json`)
- Archivo de datos de ventas (`sales_data.csv`)
- Archivo de catálogo de productos (`product_catalog.csv`)
- Configuración de validación desde `pipeline_config.yaml`

**Produce:**
- Resultado de validación exitoso/fallido
- Datos listos para procesamiento

**Dependientes:**
- Transformación (depende de validación exitosa)

---

### 2. **Transformación**
**Requiere:**
- Datos validados de la fase anterior
- Configuración de pasos: `clean_duplicates`, `handle_missing_values`, `calculate_totals`
- Ruta de salida: `data/processed/`

**Produce:**
- Datos limpios y transformados
- Totales calculados
- Datos sin duplicados

**Dependientes:**
- Enriquecimiento (depende de procesamiento exitoso)

---

### 3. **Enriquecimiento**
**Requiere:**
- Datos procesados de la fase anterior
- Catálogo de productos actualizado (`data/reference/product_catalog.csv`)
- Tablas de referencia:
  - `region_mapping`
  - `product_categories`
- Configuración de rutas desde `pipeline_config.yaml`

**Produce:**
- Datos enriquecidos con información de regiones
- Datos categorizados por tipo de producto
- Dataset completo con todos los atributos

**Dependientes:**
- Controles de Calidad (depende de enriquecimiento exitoso)

---

### 4. **Controles de Calidad**
**Requiere:**
- Datos enriquecidos de la fase anterior
- Criterios de calidad:
  - Completitud: mínimo 95%
  - Frescura: máximo 24 horas
  - Variación de filas: ±10%

**Produce:**
- Validación de calidad (Pass/Fail)
- Métricas de calidad del dataset

**Dependientes:**
- Carga (depende de controles exitosos)
- Notificaciones (usa resultado de controles)

---

### 5. **Carga**
**Requiere:**
- Datos que hayan pasado controles de calidad
- Ruta de salida configurada: `data/processed/`
- Formato de salida definido

**Produce:**
- Archivo de datos procesados
- Reporte de carga

**Dependientes:**
- Reportes (depende de carga exitosa)

---

### 6. **Reportes**
**Requiere:**
- Datos cargados exitosamente
- Métricas de todas las fases anteriores
- Resultados de validación y controles de calidad

**Produce:**
- Reporte de ejecución
- Estadísticas del procesamiento
- Resumen de errores (si aplica)

**Dependientes:**
- Notificaciones finales

---

## Dependencias de Archivos Externos

| Archivo | Ubicación | Criticidad | Descripción |
|---------|-----------|-----------|-------------|
| Esquema de Ventas | `data/schemas/sales_schema_v1.json` | CRÍTICA | Define estructura de datos válida |
| Datos de Ventas | `sales_data.csv` | CRÍTICA | Fuente principal de datos |
| Catálogo de Productos | `product_catalog.csv` | CRÍTICA | Tabla de referencia para enriquecimiento |
| Mapeo Regional | `data/reference/region_mapping` | ALTA | Lookup table para regiones |
| Categorías Productos | `data/reference/product_categories` | ALTA | Lookup table para categorías |

---

## Dependencias de Configuración

Archivo Principal: `config/pipeline_config.yaml`

Dependencias de configuración:
- Rutas de entrada/salida
- Archivos requeridos
- Pasos de procesamiento
- Criterios de calidad
- Canales de notificación

**Cambios en configuración que requieren actualización:**
- Modificación de versión de esquema
- Cambio de rutas de datos
- Actualización de criterios de calidad
- Nuevos pasos de procesamiento

---

## Flujo de Dependencias

```
   Datos Brutos
       ↓
   VALIDACIÓN
       ↓
   TRANSFORMACIÓN
       ↓
   ENRIQUECIMIENTO
       ↓
   CONTROLES CALIDAD
       ↓
   CARGA
       ↓
   REPORTES
       ↓
   NOTIFICACIONES
```

---

## Puntos Críticos de Fallo

1. Validación: Si falta esquema o está versionado incorrectamente - Pipeline detiene
2. Datos de Entrada: Si archivos no existen o tienen formato inválido - Validación falla
3. Catálogo de Productos: Si está desactualizado - Enriquecimiento produce datos inconsistentes
4. Criterios de Calidad: Si son muy estrictos - Muchas ejecuciones fallan
5. Configuración: Si está malformada - Pipeline no inicia

---

## Mantenimiento de Dependencias

### Actualización de Esquema
- Versionar correctamente (`sales_schema_v1.1.json`)
- Actualizar `pipeline_config.yaml` con nueva versión
- Ejecutar pipeline en modo test antes de producción

### Cambios en Fuentes de Datos
- Validar nuevas fuentes contra esquema existente
- Actualizar documentación de ubicación de archivos
- Comunicar cambios a stakeholders
