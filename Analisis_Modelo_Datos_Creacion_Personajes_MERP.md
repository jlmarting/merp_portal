# Análisis del Modelo de Datos para Creación de Personajes MERP

## 1. Resumen del Alcance

Este documento define el modelo de datos necesario para representar un **Personaje Jugador (PJ)** en MERP (*Middle-earth Role Playing*), con el objetivo de sustentar una futura aplicación de creación interactiva. Se basa en las estructuras descritas en el repositorio, especialmente la **Hoja de Personaje RS-1** y las tablas de bonificación **BT-1**, **BT-3** y **BT-5**.

**Principio rector:** Todo atributo computable debe almacenarse como dato derivado o calcularse en tiempo de ejecución a partir de fuentes de verdad únicas (grados, características, equipo, raza, profesión).

---

## 2. Entidades Principales

### 2.1. Personaje (PJ)

Entidad raíz que agrupa todo el estado del personaje.

| Atributo | Tipo | Descripción | Fuente |
|----------|------|-------------|--------|
| `nombre` | string | Nombre del personaje | Entrada usuario |
| `raza` | ref(Raza) | Raza seleccionada | Selección + tabla BT-3 |
| `profesion` | ref(Profesion) | Profesión/clase | Selección + progresión por nivel |
| `nivel` | int | Nivel actual (≥ 1) | Tabla ET-5 |
| `experiencia` | int | Puntos de experiencia acumulados | Tablas ET-1 a ET-5 |
| `caracteristicas` | map<string, Caracteristica> | Valores y bonos de FO, AG, CO, IG, IT, PR, AP | Tiradas + BT-1 + BT-3 |
| `habilidades` | map<string, Habilidad> | Conjunto completo de habilidades | Graduación + fórmulas RS-1 |
| `equipo` | Equipo | Armas, armaduras y objetos portados | Inventario + CST-1 |
| `puntos_vida` | EstadoPV | PV actuales y máximos | DF + bono CO (BT-1) |
| `puntos_poder` | EstadoPP | PP actuales y máximos | DPP + bono IT (BT-1) |
| `desarrollo_fisico` | int | Grado en Desarrollo Físico | Asignación inicial/progresión |
| `desarrollo_poder` | int | Grado en Desarrollo de Poder | Asignación inicial/progresión |
| `movimiento_base` | int | Movimiento base en metros/asalto | Tabla de raza |
| `resistencias` | map<string, int> | TR base contra veneno, enfermedad, miedo, etc. | Basado en CO + modificadores raza |

### 2.2. Característica

Cada una de las siete características principales del personaje.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `nombre` | string | Fuerza (FO), Agilidad (AG), Constitución (CO), Inteligencia (IG), Intuición (IT), Presencia (PR), Apariencia (AP) |
| `valor_base` | int | Valor tras tiradas iniciales (normalmente 20-100 en MERP) |
| `bonif_normal` | int | Bonificación según valor base (tabla **BT-1**) |
| `bonif_raza` | int | Modificador racial (tabla **BT-3**) |
| `total` | int | Valor final = base + bonif_raza |
| `bono_total` | int | Bonificación aplicable = bonif_normal + bonif_raza (según RS-1) |

> **Nota:** Según `Estructura_JSON_para_Hoja_de_Personaje_RS-1.md`, el `total` es la suma de `bonif_normal` y `bonif_raza`, pero contextualmente esto debe interpretarse como: el **bono aplicable** a tiradas es la suma del bono por valor (BT-1) y el modificador racial (BT-3).

### 2.3. Raza

Datos estáticos de configuración por raza.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `nombre` | string | Ej: Humano, Alto Elfo, Elfo Silvano, Enano, Hobbit, Mediano |
| `modificadores_caracteristicas` | map<string, int> | Valores a sumar/restar a cada característica (BT-3) |
| `bonif_habilidades_iniciales` | map<string, int> | Bonificaciones fijas a habilidades específicas |
| `resistencias_especiales` | map<string, int> | Modificadores a tiradas de resistencia |
| `df_base` | int | Desarrollo Físico base o modificador |
| `dpp_base` | int | Desarrollo de Poder base o modificador |
| `movimiento` | int | Movimiento base en metros por asalto |
| `vision` | string | Condiciones especiales de visión |

### 2.4. Profesión

Datos estáticos de configuración por profesión/clase.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `nombre` | string | Ej: Guerrero, Explorador, Mago, Montaraz, Bardo, Animista |
| `descripcion` | string | Rol y capacidades |
| `bono_por_nivel` | map<string, int> | Puntos de habilidad automáticos por nivel (ej. +3/nivel en armas para Guerrero) |
| `costes_desarrollo` | map<string, int> | Coste en puntos de desarrollo para subir de grado cada habilidad |
| `sortilegios` | list<string> | Lista de listas de sortilegios disponibles por círculo/nivel |
| `progresion_nivel` | ref(ET-5) | Puntos de experiencia necesarios por nivel |

### 2.5. Habilidad

Cada habilidad del personaje, con su desglose completo según la hoja RS-1.

| Atributo | Tipo | Descripción | Fuente |
|----------|------|-------------|--------|
| `nombre` | string | Nombre de la habilidad | Manual |
| `categoria` | string | Armas, Movimiento y Maniobra, General, Subterfugio, Magia, Percepción, etc. | Manual |
| `caracteristica_asociada` | string | FO, AG, CO, IG, IT, PR, AP o ninguna | Manual |
| `grado` | int | Nivel de dominio (0-N) | Asignación/Experiencia |
| `bono_grado` | int | Bonificación por grado: +5×min(grado,10) + 2×max(0,min(grado-10,10)) + 1×max(0,grado-20). Si grado=0 → -25 | RS-1 [6,7] |
| `bono_carac` | int | Bonificación de la característica asociada (BT-1) | Característica del PJ |
| `bono_profesion` | int | Bono fijo por nivel de profesión | Profesión + nivel |
| `bono_objeto` | int | Bonificaciones por objetos mágicos o especiales | Equipo |
| `bono_especial` | int | Modificadores situacionales (ej. armadura para MM) | Contexto |
| `total` | int | Suma de todos los bonos: grado + carac + profesión + objeto + especial | Derivado |

> **Regla de Grado (RS-1):**
> - Grados 1-10: +5 por grado
> - Grados 11-20: +2 por grado adicional
> - Grados >20: +1 por grado adicional
> - Grado 0: **-25**

### 2.6. Equipo

Conjunto de objetos portados por el personaje.

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `armas` | list<Arma> | Armas empuñadas y de reserva |
| `armadura` | Armadura | Armadura equipada |
| `escudo` | Escudo | Escudo equipado (si aplica) |
| `objetos` | list<Objeto> | Equipo misceláneo, provisiones, herramientas |
| `peso_total` | float | Peso total en kg (excepto armadura puesta para cálculo de carga, según BT-5) |

#### 2.6.1. Arma

| Atributo | Tipo | Descripción | Fuente |
|----------|------|-------------|--------|
| `nombre` | string | Nombre del arma | Manual |
| `tipo` | string | Filo, Contundente, Asta, Proyectil, etc. | CST-1 |
| `tabla_ataque` | string | AT-1, AT-2, AT-3, AT-4, etc. | CST-1 |
| `tipo_critico` | string | Tajo, Aplastamiento, Perforación, etc. | CST-1 |
| `rango_pifia` | string | Rango de pifia (ej. 01-08) | CST-1 |
| `bono_ofensivo` | int | Modificador a BO por arma | CST-1 |
| `peso` | float | Peso en kg | Manual |
| `manos` | int | 1 o 2 manos | Manual |

#### 2.6.2. Armadura

| Atributo | Tipo | Descripción | Fuente |
|----------|------|-------------|--------|
| `nombre` | string | Tipo de armadura | Manual |
| `tipo_armadura` | int | Tipo 1-20 para consulta en tablas AT | Manual |
| `penalizacion_mm` | int | Penalización a Movimiento y Maniobra | Manual |
| `peso` | float | Peso en kg | Manual |
| `proteccion` | string | Descripción de cobertura | Manual |

### 2.7. EstadoPV y EstadoPP

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `actuales` | int | Valor actual |
| `maximos` | int | Valor máximo calculado |

**Cálculo PV máximos:**
- Por cada grado en **Desarrollo Físico**: tirar **1d10** + bono de Constitución (BT-1).
- Acumulativo por nivel/progresión.

**Cálculo PP máximos:**
- Por cada grado en **Desarrollo de Poder**: tirar **1d10** + bono de Intuición (BT-1).
- Acumulativo por nivel/progresión.

---

## 3. Tablas de Referencia Requeridas

Para que el sistema funcione, las siguientes tablas del manual deben estar disponibles como datos maestros:

| Código | Nombre | Uso en Creación |
|--------|--------|-----------------|
| **BT-1** | Tabla de Bonificaciones por Característica | Convertir valor de característica en bono aplicable |
| **BT-3** | Modificadores de Raza | Ajustar características según raza seleccionada |
| **BT-5** | Penalización por Carga | Calcular penalización a MM según peso transportado |
| **ET-5** | Puntos de Experiencia por Nivel | Determinar umbrales de nivel para profesión |
| **CST-1** | Características de Armas | Poblar arsenal y definir tipos de crítico |

---

## 4. Flujo de Creación de Personaje (Proceso)

### Paso 1: Selección de Raza
- Usuario elige raza.
- Se cargan los `modificadores_caracteristicas` de la raza (BT-3).
- Se establecen `df_base`, `dpp_base` y `movimiento_base`.

### Paso 2: Generación de Características
- Para cada una de las 7 características (FO, AG, CO, IG, IT, PR, AP):
  - Generar `valor_base` (tirada de dados o asignación de puntos).
  - Aplicar `modificador_raza`.
  - Calcular `total` = valor_base + modificador_raza.
  - Consultar **BT-1** para obtener `bonif_normal` según `total`.
  - Establecer `bono_total` = bonif_normal + bonif_raza (si aplica doble aplicación racial).

### Paso 3: Selección de Profesión
- Usuario elige profesión.
- Se cargan los `costes_desarrollo` y `bono_por_nivel`.
- Se establece `nivel = 1` y `experiencia = 0`.

### Paso 4: Asignación de Grados Iniciales
- Distribuir puntos de desarrollo iniciales entre habilidades según costes de profesión.
- Para cada habilidad asignada:
  - Establecer `grado`.
  - Calcular `bono_grado` según progresión (+5, +2, +1, -25 para 0).
  - Obtener `bono_carac` desde la característica asociada.
  - Calcular `bono_profesion` según nivel y tabla de profesión.
  - `bono_objeto = 0`, `bono_especial = 0` inicialmente.
  - Calcular `total` = suma de bonos.

### Paso 5: Cálculo de Desarrollo Físico y PV
- Tomar el grado asignado a Desarrollo Físico.
- Para cada grado: tirar 1d10 + bono CO.
- Acumular en `puntos_vida.maximos`.
- `puntos_vida.actuales = maximos`.

### Paso 6: Cálculo de Desarrollo de Poder y PP
- Tomar el grado asignado a Desarrollo de Poder.
- Para cada grado: tirar 1d10 + bono IT.
- Acumular en `puntos_poder.maximos`.
- `puntos_poder.actuales = maximos`.

### Paso 7: Equipamiento Inicial
- Seleccionar armadura: registrar `penalizacion_mm` y `peso`.
- Seleccionar armas: registrar en lista de armas según CST-1.
- Añadir equipo misceláneo.
- Calcular `peso_total`.
- Consultar **BT-5** para determinar si aplica penalización por carga.
- Ajustar `bono_especial` de MM: restar penalización de armadura + penalización por carga.
- Recalcular `total` de Movimiento y Maniobra.

### Paso 8: Verificación y Ajustes
- Validar que todas las habilidades obligatorias tengan grado asignado.
- Verificar que PV y PP sean ≥ 1.
- Confirmar que el peso total no exceda límites de carga (opcional, según reglas del DJ).

---

## 5. Propuesta de Estructura JSON

```json
{
  "personaje": {
    "nombre": "Théodred",
    "raza": "humano",
    "profesion": "guerrero",
    "nivel": 1,
    "experiencia": 0,
    "caracteristicas": {
      "fuerza": { "valor_base": 85, "bonif_raza": 5, "total": 90, "bono": 15 },
      "agilidad": { "valor_base": 70, "bonif_raza": 0, "total": 70, "bono": 5 },
      "constitucion": { "valor_base": 80, "bonif_raza": 10, "total": 90, "bono": 15 },
      "inteligencia": { "valor_base": 60, "bonif_raza": 0, "total": 60, "bono": 0 },
      "intuicion": { "valor_base": 55, "bonif_raza": 0, "total": 55, "bono": 0 },
      "presencia": { "valor_base": 75, "bonif_raza": 0, "total": 75, "bono": 5 },
      "apariencia": { "valor_base": 65, "bonif_raza": 0, "total": 65, "bono": 0 }
    },
    "habilidades": {
      "manejo_espada": {
        "categoria": "armas",
        "caracteristica_asociada": "fuerza",
        "grado": 2,
        "desglose": {
          "grado": 10,
          "carac": 15,
          "profesion": 3,
          "objeto": 0,
          "especial": 0,
          "total": 28
        }
      },
      "movimiento_maniobra": {
        "categoria": "movimiento",
        "caracteristica_asociada": "agilidad",
        "grado": 1,
        "desglose": {
          "grado": 5,
          "carac": 5,
          "profesion": 2,
          "objeto": 0,
          "especial": -30,
          "total": -18
        }
      }
    },
    "equipo": {
      "armas": [
        {
          "nombre": "Espada Ancha",
          "tipo": "filo",
          "tabla_ataque": "AT-1",
          "tipo_critico": "tajo",
          "rango_pifia": "01-08",
          "peso": 1.5,
          "manos": 1
        }
      ],
      "armadura": {
        "nombre": "Cota de Malla",
        "tipo_armadura": 14,
        "penalizacion_mm": -30,
        "peso": 8.0
      },
      "peso_total": 12.5
    },
    "estado": {
      "puntos_vida": { "actuales": 45, "maximos": 45 },
      "puntos_poder": { "actuales": 15, "maximos": 15 }
    },
    "desarrollo_fisico": 3,
    "desarrollo_poder": 1,
    "movimiento_base": 10
  }
}
```

---

## 6. Dependencias de Datos Maestros

Para implementar el flujo completo, el sistema necesita las siguientes tablas como configuración estática:

1. **Tabla BT-1 completa:** Mapeo valor de característica → bono.
2. **Tabla BT-3 completa:** Mapeo raza → modificadores por característica.
3. **Tabla BT-5 completa:** Mapeo peso transportado → penalización a MM.
4. **Tabla ET-5 completa:** Mapeo nivel → experiencia requerida.
5. **Tabla CST-1 completa:** Estadísticas de todas las armas.
6. **Listado de habilidades:** Con su categoría y característica asociada.
7. **Listado de razas:** Con todos sus atributos base.
8. **Listado de profesiones:** Con costes de desarrollo y bonos por nivel.

---

## 7. Próximos Pasos Recomendados

1. **Transcribir BT-1, BT-3 y BT-5** a JSON real (estos son los bloqueantes para cualquier cálculo automático).
2. **Definir el catálogo de habilidades** con sus categorías y características asociadas.
3. **Definir el catálogo de razas y profesiones** con valores canónicos del manual.
4. **Implementar un motor de cálculo** que reciba los inputs del usuario y genere el JSON de personaje aplicando las fórmulas del RS-1.
5. **Validar el modelo** contra la Hoja de Personaje RS-1 del manual para asegurar que no falta ningún campo.

---

## Referencias Cruzadas del Repositorio

- `Estructura_JSON_para_Hoja_de_Personaje_RS-1.md`: Estructura de desglose de habilidades y cálculo de grado.
- `Sistema_de_Experiencia_y_Progresión_MERP_en_JSON.md`: Estructura ET-1 a ET-5 para progresión de niveles.
- `Todas_las_notas_del_31_5_2026.md`: Tablas CST-1, CST-2, CST-3 para tipos de crítico y estadísticas de armas.
- `Algoritmo_de_Resolución_de_Combate_en_la_Tierra_Media.md`: Uso de BO, BD, parada y tiradas abiertas (relevante para verificar habilidades de combate).
