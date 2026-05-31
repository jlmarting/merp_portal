# Estructura JSON para Hoja de Personaje RS-1

### Estructura JSON para Hoja de Personaje RS-1

Basado en la **Hoja de Personaje RS-1** [1] y el ejemplo detallado de la página 38 [2], he diseñado una estructura **JSON** exhaustiva que refleja fielmente todos los campos, tablas de bonificaciones y secciones de equipo del manual.

Esta estructura está organizada para capturar tanto los valores base como el desglose de bonificaciones (grado, característica, profesión, etc.) tal como aparecen en el documento físico.

### 📝 Notas sobre el uso de esta estructura:

**Características:** Los campos `bonif_normal` y `bonif_raza` se extraen de las tablas **BT-1** [3] y **BT-3** [4]. El `total` es la suma de ambos [5].

**Desglose de Habilidades:** La estructura sigue las columnas de la hoja oficial (**Grado, Carac, Profesión, Objeto, Especial, Total**) [1].

**Grado:** Se calcula según la progresión: +5 (grados 1-10), +2 (11-20), +1 (>20). Si es grado 0, aplica -25 [6, 7].

**Profesión:** Es el bono fijo por nivel que otorga cada clase (ej. Guerrero gana +3/nivel en armas) [8, 9].

**Movimiento y Maniobra (MM):** Incluye penalizaciones fijas por tipo de armadura (ej. Coraza -60) que deben restarse en la columna "Especial" [6, 10].

**Penalización por Carga:** Se calcula sumando el peso del equipo (excepto armadura puesta) y comparándolo con la tabla **BT-5** [7].

**Puntos de Vida (PV):** El máximo se determina por la habilidad de **Desarrollo Físico**. Cada grado permite tirar **1d10** y sumar el bono de Constitución [11].