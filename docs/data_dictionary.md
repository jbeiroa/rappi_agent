# Diccionario de Datos: Métricas Operacionales de Rappi

Este documento define las métricas disponibles en el dataset `dummy_data.xlsx` y las columnas enriquecidas generadas por el pipeline de IA y Machine Learning.

## Métricas Base
| Métrica | Descripción |
| :--- | :--- |
| **% PRO Users Who Breakeven** | Suscriptores Pro cuyo valor generado cubre el costo de su membresía / Total de usuarios Pro. |
| **% Restaurants Sessions With Optimal Assortment** | Sesiones con un mínimo de 40 restaurantes / Total de sesiones. |
| **Gross Profit UE** | Margen de beneficio bruto / Total de pedidos. |
| **Lead Penetration** | Tiendas habilitadas / (Leads prospectos + Tiendas habilitadas + Tiendas que salieron). |
| **MLTV Top Verticals Adoption** | Usuarios con pedidos en múltiples verticales / Total de usuarios. |
| **Non-Pro PTC > OP** | Conversión de "Proceed to Checkout" a "Order Placed" para usuarios No Pro. |
| **Perfect Orders** | Pedidos sin cancelaciones, defectos o retrasos / Total de pedidos. |
| **Pro Adoption** | Suscriptores Pro / Total de usuarios de Rappi. |
| **Restaurants Markdowns / GMV** | Descuentos totales en restaurantes / Valor Bruto de Mercancía (GMV). |
| **Restaurants SS > ATC CVR** | Conversión de "Select Store" a "Add to Cart" en restaurantes. |
| **Restaurants SST > SS CVR** | % de selección de restaurante específico tras entrar en la vertical. |
| **Retail SST > SS CVR** | % de selección de tienda específica tras entrar en la vertical de Supermercados. |
| **Turbo Adoption** | Usuarios de Turbo / Usuarios con Turbo disponible. |
| **Orders** | Volumen total de pedidos realizados. |

## Columnas Enriquecidas (Pipeline ML/IA)
Estas columnas se generan dinámicamente para potenciar el análisis de los agentes:

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| **WOW_CHANGE** | Float | Cambio porcentual de la métrica respecto a la semana anterior. |
| **IS_ANOMALY** | Boolean | Detectada por el modelo `IsolationForest` basándose en el valor y su cambio WoW. |
| **WORRYING_METRIC** | Boolean | `True` si la métrica ha presentado deterioro constante por 3 o más semanas. |
| **TYPE_AVG_VALUE** | Float | Valor promedio de la métrica para todas las zonas del mismo tipo (`ZONE_TYPE`). |
| **PCT_DIFF_FROM_TYPE_AVG**| Float | Diferencia porcentual respecto al promedio de su tipo (Benchmarking). |

## Dimensiones Geográficas y Temporales
- **COUNTRY:** AR, BR, CL, CO, CR, EC, MX, PE, UY.
- **CITY / ZONE:** Localización geográfica.
- **ZONE_TYPE:** Wealthy / Non Wealthy.
- **WEEK:** L8W (hace 8 semanas) a L0W (semana actual).
- **WEEK_NUM:** Índice numérico para cálculos temporales (0 es la actual).
