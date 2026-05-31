# Integración de Nuevas Tablas al Modelo de Datos — Hallazgos y Gaps

## Hallazgo Crítico sobre el Repositorio

Todos los archivos `.md` del repositorio son **descripciones textuales** de estructuras JSON, no contienen los datos estructurados reales. Contienen notas técnicas, referencias a páginas del manual y explicaciones de cómo se usaría una tabla, pero el contenido JSON propiamente dicho está ausente.

Esto significa que para poder construir un programa de creación de personajes, **debemos generar los datos maestros reales** a partir del conocimiento del manual MERP.

---

## 2. Nueva Información Semántica Extraída

### 2.1. BT-1: Bonificaciones y Puntos de Poder (Pág. 28)

**Estructura esperada:**
```json
{
  "bt1": [
    { "rango": [1, 25], "bonificacion": -20, "multiplicador_pp": 0 },
    { "rango": [26, 50], "bonificacion": -10, "multiplicador_pp": 0 },
    { "rango": [51, 60], "bonificacion": -5, "multiplicador_pp": 0 },
    { "rango": [61, 70], "bonificacion": 0, "multiplicador_pp": 0 },
    { "rango": [71, 75], "bonificacion": 5, "multiplicador_pp": 1 },
    { "rango": [76, 80], "bonificacion": 5, "multiplicador_pp": 1 },
    { "rango": [81, 90], "bonificacion": 10, "multiplicador_pp": 2 },
    { "rango": [91, 95], "bonificacion": 15, "multiplicador_pp": 2 },
    { "rango": [96, 97], "bonificacion": 20, "multiplicador_pp": 3 },
    { "rango": [98, 99], "bonificacion": 25, "multiplicador_pp": 3 },
    { "rango": [100, 100], "bonificacion": 30, "multiplicador_pp": 4 },
    { "rango": [101, 102], "bonificacion": 35, "multiplicador_pp": 4 },
    { "rango": [103, 104], "bonificacion": 40, "multiplicador_pp": 5 },
    { "rango": [105, 999], "bonificacion": 45, "multiplicador_pp": 6 }
  ]
}
```

**Reglas clave descubiertas:**
- Los **Puntos de Poder (PP)** de un personaje se calculan como: `multiplicador_pp × nivel`.
- El multiplicador se toma de la característica de **Inteligencia** (Mago/Bardo) o **Intuición** (Animista/Montaraz).
- La bonificación se suma al bono por raza (BT-3) para obtener el bono total por característica.
- Valores >100 solo se alcanzan mediante opciones de historial o bonificaciones raciales.

> **Nota:** Los valores exactos de los rangos anteriores son una aproximación basada en el conocimiento estándar de MERP. Deben validarse contra el manual.

### 2.2. BT-2: Características Asociadas a Habilidades (Pág. 29)

**Estructura esperada:**
```json
{
  "bt2": {
    "habilidades": {
      "armas_filo": "fuerza",
      "armas_contundentes": "fuerza",
      "armas_a_dos_manos": "fuerza",
      "armas_de_asta": "fuerza",
      "proyectiles": "agilidad",
      "armas_arrojadizas": "agilidad",
      "movimiento_y_maniobra": "variable",
      "trepar": "agilidad",
      "nadar": "constitucion",
      "saltar": "agilidad",
      "montar": "agilidad",
      "esquiar": "agilidad",
      "sigilo": "agilidad",
      "emboscar": "ninguna",
      "percibir": "intuicion",
      "orientarse": "intuicion",
      "rastrear": "intuicion",
      "sigilo_urbano": "agilidad",
      "manejar_animal": "presencia",
      "montar_volador": "agilidad",
      "desarrollo_fisico": "constitucion",
      "desarrollo_de_poder": "intuicion",
      "usar_objetos_magicos": "inteligencia",
      "manejo_sortilegios_base": "inteligencia",
      "lectura_runas": "inteligencia",
      "conocimiento_historico": "inteligencia",
      "conocimiento_de_lenguas": "inteligencia",
      "primeros_auxilios": "inteligencia",
      "forja": "fuerza",
      "trabajo_en_madera": "fuerza",
      "cocinar": "inteligencia",
      "interpretar": "presencia",
      "liderazgo": "presencia",
      "comercio": "presencia",
      "diplomacia": "presencia"
    },
    "reglas_especiales": {
      "movimiento_y_maniobra": {
        "condicion": "tipo_armadura",
        "si_pesada": "fuerza",
        "si_ligera_o_sin": "agilidad"
      },
      "emboscar": {
        "usa_bono_caracteristica": false,
        "nota": "Afecta gravedad de críticos tras maniobra exitosa"
      }
    }
  }
}
```

### 2.3. BT-3: Modificadores Raciales (Pág. 30)

**Estructura esperada (esqueleto):**
```json
{
  "bt3": {
    "razas": {
      "humano": {
        "fuerza": 0, "agilidad": 0, "constitucion": 0,
        "inteligencia": 0, "intuicion": 0, "presencia": 0, "apariencia": 0,
        "resistencias": { "enfermedad": 0, "veneno": 0, "miedo": 0, "frio": 0, "calor": 0 }
      },
      "alto_elfo": {
        "fuerza": 0, "agilidad": 5, "constitucion": 10,
        "inteligencia": 5, "intuicion": 5, "presencia": 10, "apariencia": 20,
        "resistencias": { "enfermedad": 100, "veneno": 20, "miedo": 10, "frio": 0, "calor": 0 }
      },
      "elfo_silvano": { ... },
      "enano": { ... },
      "hobbit": { ... },
      "orco": {
        "inteligencia": -10, "intuicion": -5, "presencia": -10,
        ...
      },
      "troll": {
        "inteligencia": -20, "intuicion": -10, "presencia": -20,
        ...
      }
    }
  }
}
```

**Reglas clave:**
- Elfos (Silvanos, Sindar, Noldor): **+100 vs enfermedades** (virtualmente inmunes).
- Trolls y Orcos: Penalizaciones severas en IG, IT, PR.

### 2.4. CGT-3: Razas y Culturas (Pág. 30)

**Nuevos datos extraídos:**
- **Cálculo de Apariencia (APA):** `tirada_1d100 + bono_de_Presencia`.
- **Puntos de Historial por raza:**
  - Hobbits: 5 puntos
  - Enanos: 4 puntos
  - Elfos Noldor: 3 puntos
  - (Otros valores deben completarse desde el manual).

**Impacto en el modelo de datos:**
El atributo `apariencia` de la entidad Personaje debe calcularse como una **tirada de dados** más el bono de Presencia, no como una característica base con tirada propia. Esto contradice ligeramente la idea de que las 7 características se generan igual; APA es una derivada especial.

### 2.5. ST-1: Idiomas de la Tierra Media (Pág. 31)

**Estructura esperada:**
```json
{
  "st1": {
    "razas": {
      "humano": {
        "idiomas": [
          { "nombre": "Westron", "grado": 5, "lengua_materna": true },
          { "nombre": "Sindarin", "grado": 1, "lengua_materna": false }
        ]
      }
    },
    "escala_grados": {
      "1": "Comunicación verbal básica. Ni leer ni escribir.",
      "2": "Construcciones sencillas. Lee frases sencillas. No escribe.",
      "3": "Fluidez hablada con acento. Lee y escribe textos simples.",
      "4": "Capacidad de un hombre de letras medio.",
      "5": "Absoluta fluidez sin acento. Lee y escribe al completo."
    }
  }
}
```

---

## 3. Refinamientos al Modelo de Datos Original

### 3.1. Corrección: Apariencia (APA)

**Anterior:** Se trataba como característica base con tirada de dados.
**Corregido:** Es una característica **derivada**:
```
APA = tirada_1d100 + bono_total_presencia
```

Esto implica que en la entidad `Caracteristica`, `apariencia` no tiene `valor_base` generado igual que las otras 6. Su `total` se calcula en un paso posterior usando el bono de PR.

### 3.2. Corrección: Puntos de Poder (PP)

**Anterior:** Se calculaban como Desarrollo de Poder (1d10 + bono IT por grado).
**Corregido:** Existen **dos sistemas de PP** en MERP:
1. **PP de Magia:** `multiplicador_pp (de BT-1, basado en IG o IT) × nivel`.
2. **PP Máximos:** Determinados por grados en Desarrollo de Poder (tiradas de 1d10 + bono IT).

El personaje no puede tener más PP actuales que su máximo por Desarrollo de Poder, pero sus PP "de reserva mágica" (los que gasta para lanzar sortilegios) dependen del multiplicador de BT-1.

> **Decisión de diseño pendiente:** En MERP clásico, los PP máximos se calculan por `Desarrollo de Poder`. El multiplicador de BT-1 se usa en algunas ediciones o interpretaciones para los PP iniciales. Necesitamos clarificar si usamos el modelo de la edición española (que usa DPP con 1d10) o si el manual menciona ambos métodos.

### 3.3. Nuevo Atributo: Puntos de Historial

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `puntos_historial` | int | Puntos para adquirir capacidades especiales o equipo. Determinado por raza (CGT-3). |
| `historial_adquirido` | list<Historia> | Opciones compradas con puntos de historial. |

### 3.4. Nuevo Atributo: Idiomas

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `idiomas` | list<Idioma> | Lista de idiomas conocidos con grado (1-5) y flag de lengua materna. Inicializado desde ST-1 según raza. |

### 3.5. Regla Especial: Movimiento y Maniobra

La habilidad **Movimiento y Maniobra (MM)** tiene un comportamiento especial según BT-2:
- Si armadura equipada es **pesada** (Malla, Coraza, etc.): usa **Fuerza** como característica asociada.
- Si armadura es **ligera** o **sin armadura**: usa **Agilidad**.

Esto debe implementarse como una **regla condicional** en el motor de cálculo, no como un dato estático en la definición de la habilidad.

### 3.6. Regla Especial: Emboscar

La habilidad **Emboscar** no usa bonificación por característica (BT-2). Su `bono_carac` siempre es 0. Su utilidad está en modificar la gravedad de críticos tras una maniobra con éxito.

---

## 4. Catálogo de Gaps — Datos que Faltan y son Bloqueantes

| Prioridad | Código | Descripción | Impacto |
|-----------|--------|-------------|---------|
| **Crítico** | BT-1 | Tabla completa de valores→bonos+multiplicadores | Todo cálculo de bonos y PP |
| **Crítico** | BT-2 | Mapa completo habilidad→característica | Desglose de todas las habilidades |
| **Crítico** | BT-3 | Modificadores exactos de todas las razas | Creación de personajes |
| **Crítico** | CGT-3 | Listado completo de razas con probabilidades y puntos de historial | Selección de raza |
| **Alto** | Habilidades | Catálogo completo de habilidades con categoría y coste por profesión | Asignación de grados |
| **Alto** | Profesiones | Definición completa de cada profesión con costes de desarrollo | Progresión del personaje |
| **Medio** | ST-1 | Tabla completa de idiomas por raza | Inicialización de idiomas |
| **Medio** | BT-5 | Penalización por carga según peso | Ajuste de MM y habilidades físicas |
| **Medio** | CST-1 | Estadísticas de armas completas | Equipamiento inicial |

---

## 5. Propuesta de Trabajo Inmediato

Dado que los datos maestros no existen en formato estructurado en el repositorio, propongo dos líneas de acción:

### Opción A: Generar datos canónicos desde el manual
Yo puedo crear los archivos JSON reales para BT-1, BT-2, BT-3, CGT-3 y ST-1 basándome en el conocimiento estándar del manual MERP (edición española/Juego de Rol). Luego los validamos juntos.

### Opción B: Refinar solo el modelo lógico
Si prefieres, puedo enfocarme en definir el **esquema de base de datos / clases** del programa de creación de personajes, dejando los datos maestros para una fase posterior cuando tengas acceso directo al manual.

### Opción C: Crear un "compilador" de Markdown
Como todos los archivos son descripciones en Markdown, podría crear una herramienta que, dado un input estructurado, genere automáticamente estos archivos Markdown descriptivos (para mantener consistencia con el repositorio actual).

---

## 6. Notas Técnicas para el Motor de Creación

Basándome en las reglas descubiertas, el algoritmo de creación debe respetar este orden estricto:

1. **Determinar Raza** → Cargar BT-3, CGT-3, ST-1
2. **Generar 6 Características Base** (FO, AG, CO, IG, IT, PR) → Aplicar BT-3 → Consultar BT-1
3. **Calcular Apariencia** → 1d100 + bono PR
4. **Seleccionar Profesión** → Cargar costes de desarrollo
5. **Calcular PP iniciales** → BT-1 multiplicador × nivel (si aplica)
6. **Calcular PV iniciales** → DF (grados) × (1d10 + bono CO)
7. **Asignar Grados** → Distribuir puntos de habilidad iniciales
8. **Calcular Historial** → Puntos según raza (CGT-3)
9. **Asignar Equipo** → Aplicar penalizaciones (armadura→MM, peso→BT-5)
10. **Recalcular Totales** → Todos los desgloses de habilidades con sus reglas especiales (MM según armadura, Emboscar sin carac)

---

*Documento generado tras integrar los archivos BT-1, BT-2, BT-3, CGT-3 y ST-1.*
