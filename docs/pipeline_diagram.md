# Pipeline de Procesamiento de Datos de Ventas

Diagrama del flujo completo del pipeline de procesamiento de datos de ventas:

```mermaid
graph TD
    A["Entrada de Datos"] --> B["sales_data.csv"]
    A --> C["product_catalog.csv"]
    
    B --> D{"Validación"}
    C --> D
    
    D -->|Schema Válido| E["Procesamiento"]
    D -->|Error| F["Notificar Fallo"]
    
    E --> E1["Limpiar Duplicados"]
    E1 --> E2["Manejar Valores Faltantes"]
    E2 --> E3["Calcular Totales"]
    
    E3 --> G["Enriquecimiento de Datos"]
    
    G --> G1["Mapeo por Región"]
    G1 --> G2["Categorías de Productos"]
    
    G2 --> H["Controles de Calidad"]
    
    H --> H1["Completitud: 95%"]
    H1 --> H2["Frescura: < 24h"]
    H2 --> H3["Variación de Filas: ±10%"]
    
    H3 -->|Todos Pasan| I["Procesamiento Exitoso"]
    H3 -->|Alguno Falla| F
    
    I --> J["data/processed/"]
    I --> K["Notificar Éxito"]
    F --> L["Registrar en Log"]
```

## Descripción de Fases

### 1. **Validación**
- Verifica que los archivos requeridos existan
- Valida el esquema contra `sales_schema_v1.json`

### 2. **Procesamiento**
- Limpiar Duplicados: Elimina registros duplicados
- Manejar Valores Faltantes: Procesa datos incompletos
- Calcular Totales: Computa agregaciones necesarias

### 3. **Enriquecimiento**
- Integra datos del catálogo de productos
- Aplica mapeos de regiones
- Clasifica productos por categorías

### 4. **Controles de Calidad**
- Completitud: Mínimo 95% de datos válidos
- Frescura: Datos con antigüedad máxima de 24 horas
- Variación: Tolerancia de ±10% en cambios de volumen

### 5. **Notificaciones**
- Genera alertas en caso de éxito o fallo
- Registra eventos en archivos de log
