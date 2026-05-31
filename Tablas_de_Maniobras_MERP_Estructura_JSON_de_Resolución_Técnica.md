# Tablas de Maniobras MERP: Estructura JSON de Resolución Técnica

### Tablas de Maniobras MERP: Estructura JSON de Resolución Técnica

Aquí tienes la estructura **JSON** para las tablas de maniobras (**MT-1 y MT-2**), las cuales se utilizan para resolver acciones bajo presión que no son ataques directos, basándose en la información de las páginas 179 a 182 del manual [1, 2].

Esta estructura incluye el desglose de porcentajes de éxito para movimiento y las descripciones narrativas para maniobras estáticas.

### Notas técnicas para la implementación:

**MT-1**: Los valores numéricos representan la efectividad [2]. Por ejemplo, un 80 significa que has completado el 80% del movimiento o que tienes un 80% de probabilidades de éxito total según decida el Director de Juego.

**Modificadores de Agilidad/Fuerza**: Dependiendo de la maniobra (Trepar usa Agilidad, por ejemplo), debes sumar el bono de la característica a la tirada abierta [21].

**Penalización por Armadura**: Recuerda restar la penalización por el tipo de armadura que lleve el personaje a la tirada de movimiento (MM) [22].