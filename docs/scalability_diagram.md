# Diagrama de Escalabilidad del Pipeline

## Arquitectura Escalable del Pipeline de Ventas

Estrategia para escalar el pipeline a medida que crece el volumen de datos:

```mermaid
graph TB
    subgraph Input["Entrada de Datos (Escalable)"]
        DS["Data Source"]
        Batch["Batch Processing"]
        Stream["Stream Processing"]
    end
    
    subgraph Queue["Cola de Mensajes (Load Balancing)"]
        MQ["Message Queue<br/>RabbitMQ/Kafka"]
    end
    
    subgraph Validation["Validación Distribuida"]
        V1["Worker 1"]
        V2["Worker 2"]
        V3["Worker N"]
    end
    
    subgraph Cache["Caché Distribuida"]
        Redis["Redis Cache<br/>Esquemas & LUT"]
    end
    
    subgraph Processing["Procesamiento Paralelo"]
        P1["Transform 1"]
        P2["Transform 2"]
        P3["Transform N"]
    end
    
    subgraph Enrichment["Enriquecimiento Distribuido"]
        E1["Region Mapping"]
        E2["Category Mapping"]
        E3["Reference Data"]
    end
    
    subgraph QA["Controles de Calidad"]
        Q1["Completitud Check"]
        Q2["Frescura Check"]
        Q3["Variación Check"]
    end
    
    subgraph Output["Salida Escalable"]
        DB[(Base de Datos<br/>Particionada)]
        DW["Data Warehouse"]
        S3["S3/Cloud Storage"]
    end
    
    subgraph Monitor["Monitoreo & Autoscaling"]
        Metrics["Prometheus"]
        Alert["Alertas"]
        Auto["Autoscaling Engine"]
    end
    
    DS --> MQ
    Batch --> MQ
    Stream --> MQ
    
    MQ --> V1
    MQ --> V2
    MQ --> V3
    
    Cache --> V1
    Cache --> V2
    Cache --> V3
    
    V1 --> P1
    V2 --> P2
    V3 --> P3
    
    P1 --> E1
    P2 --> E2
    P3 --> E3
    
    E1 --> Q1
    E2 --> Q2
    E3 --> Q3
    
    Q1 --> DB
    Q2 --> DW
    Q3 --> S3
    
    Q1 --> Metrics
    Q2 --> Metrics
    Q3 --> Metrics
    
    Metrics --> Alert
    Metrics --> Auto
    
    Auto -.->|Scale Up| V1
    Auto -.->|Scale Up| P1
    Auto -.->|Scale Up| E1
```

---

## Estrategias de Escalabilidad

### 1. **Escalabilidad Horizontal - Validación**
```
Antes:        Después:
┌─────────┐  ┌──────┬──────┬──────┐
│Worker   │  │W1    │W2    │W3    │
└─────────┘  └──────┴──────┴──────┘
 1 GB/min    3 GB/min (paralelo)
```
- Múltiples validadores en paralelo
- Load balancing con Message Queue
- Replicación de esquemas en caché compartida

### 2. **Escalabilidad de Procesamiento**
```
Datos:     100k filas  -  10M filas  -  100M filas
Workers:   1 worker   -  10 workers -  100 workers
Tiempo:    30 min     -  30 min     -  30 min
```
- Particionamiento de datos por región/producto
- Procesamiento en lotes (micro-batches)
- Streaming para datos en tiempo real

### 3. **Escalabilidad de Almacenamiento**
```
Single Database          Partitioned Database
┌─────────────────┐     ┌──────┬──────┬──────┐
│ +1M rows        │     │ DB1  │ DB2  │ DB3  │
│ Queries         │     │ 500k │ 500k │ 500k │
│ Performance     │     └──────┴──────┴──────┘
└─────────────────┘     Distributed Query
```
- Sharding por región o fecha
- Réplicas de lectura
- Data Warehouse para análisis

### 4. **Caché Distribuida**
```
Lookup Tables (Región Mapping, Productos)
         ↓
   Redis Cluster
   ┌─────────────────┐
   │ Node1: 10GB     │
   │ Node2: 10GB     │
   │ Node3: 10GB     │
   └─────────────────┘
   Acceso < 1ms
```
- Caché en memoria para tablas de referencia
- Replicación automática

---

## Matriz de Escalabilidad

| Scenario | Filas/Día | Workers | Tiempo | Storage |
|----------|-----------|---------|--------|---------|
| Pequeño | 100K | 1 | 5 min | 100MB |
| Mediano | 10M | 5 | 10 min | 10GB |
| Grande | 100M | 20 | 15 min | 100GB |
| Very Large | 1B+ | 50+ | 20-30 min | 1TB+ |

### Recomendaciones por Escala

**Escala Pequeña (< 1M filas/día)**
- Pipeline secuencial
- Base de datos única
- Caché local

**Escala Mediana (1M - 100M filas/día)**
- Validación paralela (5-10 workers)
- Message Queue
- Redis para referencias
- DB con índices optimizados

**Escala Grande (100M - 1B filas/día)**
- Validación altamente distribuida (20+ workers)
- Kafka para streaming
- Redis Cluster
- Sharding de DB
- Data Warehouse separado

**Escala Very Large (> 1B filas/día)**
- Spark/Hadoop cluster
- Kubernetes orchestration
- Multi-region deployment
- Cloud-native architecture
- Auto-scaling (HPA)

---

## Tecnologías Recomendadas

### Orquestación
- **Apache Airflow**: Scheduler y DAG management
- **Kubernetes**: Container orchestration
- **Docker**: Containerización de workers

### Mensajería
- **Apache Kafka**: High-throughput streaming
- **RabbitMQ**: Task queue distribuida
- **AWS SQS**: Queue administrada en cloud

### Caché
- **Redis**: In-memory data store
- **Memcached**: Distribuir caché simple

### Almacenamiento
- **PostgreSQL**: Transaccional
- **Snowflake**: Data warehouse cloud
- **BigQuery**: Data warehouse distribuido
- **S3/GCS**: Object storage

### Monitoreo
- **Prometheus**: Métricas
- **Grafana**: Visualización
- **ELK Stack**: Logs centralizados
- **DataDog/New Relic**: Monitoring APM

---

## Autoscaling Automático

```yaml
Trigger Rules:
- CPU > 70% → Scale Up (+2 workers)
- Memory > 80% → Scale Up (+1 worker)
- Queue Depth > 10k → Scale Up (+3 workers)
- CPU < 20% × 5min → Scale Down (-1 worker)

Min Workers: 1
Max Workers: 100
Scale-up Delay: 30s
Scale-down Delay: 5min
```

---

## Arquitectura Global (Multi-región)

```
┌─────────────────────────────────────┐
│      Global Load Balancer           │
├─────────────────────────────────────┤
│ US-EAST │ EU-WEST │ ASIA-PACIFIC    │
│  ┌────┐ │  ┌────┐ │  ┌────┐         │
│  │ P1 │ │  │ P2 │ │  │ P3 │         │
│  └────┘ │  └────┘ │  └────┘         │
├─────────────────────────────────────┤
│   Central Data Warehouse            │
└─────────────────────────────────────┘

Replication: Master-Master
Consistency: Eventually Consistent
Latency: < 100ms global
```
