# Algoritmo de Resolución de Combate en la Tierra Media

### Algoritmo de Resolución de Combate en la Tierra Media

Basado en las reglas detalladas en el manual y las notas técnicas, la resolución de un asalto de combate en El Señor de los Anillos: El Juego de Rol sigue un proceso estructurado. Aquí tienes el algoritmo paso a paso para resolver un encuentro táctico:

### 1. Fase de Declaración y Secuencia

Al inicio de cada asalto (que dura 10 segundos), cada jugador y el Director de Juego (DJ) deben decidir qué acción realizará cada personaje [1, 2]. Las acciones se resuelven normalmente en este orden:

**Sortilegios:** Preparación o lanzamiento [2].

**Proyectiles:** Ataques con arcos, ballestas o armas arrojadizas [2].

**Maniobras de movimiento:** Acciones físicas complejas [2].

**Cuerpo a cuerpo:** Ataques y paradas con armas de mano [2].

**Movimiento:** Desplazamiento normal [2].

**Maniobras estáticas:** Acciones que no implican desplazarse [2].

### 2. Algoritmo de Resolución de un Ataque

Para cada ataque individual (ya sea físico o de sortilegio dirigido), se sigue este procedimiento:

**Tirada de Dados:** El atacante realiza una **tirada abierta de 1d100** [3, 4].

**Comprobación de Pifia:** Se verifica si el resultado sin modificar (SM) está en el rango de pifia del arma (consultar tabla **CST-1**; generalmente entre 01-08) [4, 5]. Si es pifia, se ignora el resto del ataque y se tira en la tabla de pifias correspondiente (**FT-1** para armas, **FT-2** para proyectiles o **FT-3** para magia) [4, 6].

**Cálculo del Resultado Final:** Se suma la **Bonificación Ofensiva (BO)** del atacante y se resta la **Bonificación Defensiva (BD)** del defensor [4, 7].

**Fórmula:** `Resultado = Tirada + BO - BD - (Parada del defensor)` [4, 7].

**Modificadores Situacionales:** Aplicar bonos adicionales si corresponde:

Ataque por el flanco: **+15** [8].

Ataque por la espalda: **+20** [8].

Defensor sorprendido: **+20** [8].

**Consulta de la Tabla de Ataque:** Se busca el resultado final en la tabla de ataque correspondiente al arma o sortilegio (p. ej., **AT-1** para espadas, **AT-4** para arcos, **AT-7** para rayos) cruzándolo con el **Tipo de Armadura** del blanco [9-11].

**Determinación del Daño:**

**Puntos de Vida (PV):** El número obtenido indica cuántos puntos de vida pierde el defensor [7].

**Impacto Crítico:** Si el resultado incluye una letra (A, B, C, D o E), se ha producido un crítico [7].

### 3. Resolución de Impactos Críticos

Si el ataque genera un crítico, se deben seguir estos pasos adicionales:

**Determinar el tipo de crítico:** Según el arma (**CST-1**), el animal (**CST-2**) o el sortilegio (**CST-3**) (ej. Tajo, Perforación, Calor, etc.) [12-14].

**Tirada de Crítico:** El atacante lanza **1d100** (esta tirada **no es abierta**) [7].

**Aplicar Modificador de Gravedad:** Se ajusta la tirada según la letra obtenida en la tabla de ataque [15, 16]:

**A:** -20

**B:** -10

**C:** +0

**D:** +10

**E:** +20

**Consultar Tabla de Críticos:** Se busca el resultado final en la tabla específica (ej. **CT-1** Aplastamiento, **CT-2** Tajo, etc.) y se aplican los efectos descritos [17, 18].

Los efectos pueden incluir más PV, hemorragias (PV por asalto), aturdimiento, penalizaciones a la actividad o muerte inmediata [7, 17].

### 4. Resolución de Sortilegios Básicos (No dirigidos)

Si el sortilegio no es de rayo ni de bola, se usa la tabla **AT-9**:

El atacante tira **1d100 + BO - Nivel del Sortilegio** [19, 20].

El resultado de la tabla **AT-9** actúa como un **modificador a la Tirada de Resistencia (TR)** del defensor [7].

El defensor tira **1d100 + su bonificación por característica** y debe superar el número indicado en la Tabla de Resistencia (**TTR**) para el nivel del atacante y del defensor [7, 21].