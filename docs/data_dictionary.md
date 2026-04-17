# Diccionario de Datos: Métricas Operacionales de Rappi

Este documento define las métricas disponibles en el dataset `dummy_data.xlsx` y su lógica de negocio.

| Métrica | Descripción |
| :--- | :--- |
| **% PRO Users Who Breakeven** | Suscriptores Pro cuyo valor generado para la empresa (comisiones, etc.) cubre el costo de su membresía / Total de usuarios Pro. |
| **% Restaurants Sessions With Optimal Assortment** | Sesiones con un mínimo de 40 restaurantes / Total de sesiones. |
| **Gross Profit UE** | Margen de beneficio bruto / Total de pedidos. |
| **Lead Penetration** | Tiendas habilitadas / (Leads prospectos + Tiendas habilitadas + Tiendas que salieron de Rappi). |
| **MLTV Top Verticals Adoption** | Usuarios con pedidos en múltiples verticales (Restaurantes, Super, Farmacia, Licores) / Total de usuarios. |
| **Non-Pro PTC > OP** | Conversión de "Proceed to Checkout" a "Order Placed" para usuarios No Pro. |
| **Perfect Orders** | Pedidos sin cancelaciones, defectos o retrasos / Total de pedidos. |
| **Pro Adoption** | Suscriptores Pro / Total de usuarios de Rappi. |
| **Restaurants Markdowns / GMV** | Descuentos totales en pedidos de restaurantes / Valor Bruto de Mercancía (GMV) total de restaurantes. |
| **Restaurants SS > ATC CVR** | Conversión en restaurantes de "Select Store" a "Add to Cart". |
| **Restaurants SST > SS CVR** | % de usuarios que seleccionan un restaurante específico tras seleccionar la vertical de Restaurantes. |
| **Retail SST > SS CVR** | % de usuarios que seleccionan una tienda específica tras seleccionar la vertical de Supermercados. |
| **Turbo Adoption** | Usuarios totales de Turbo / Usuarios totales con Turbo disponible en su zona. |
| **Orders** | Volumen total de pedidos realizados en la zona. |

## Estructura de Datos (Semanal)
Todas las métricas y pedidos se proporcionan para las últimas 8 semanas:
- **L8W:** Hace 8 semanas.
- **L7W:** Hace 7 semanas.
- ...
- **L1W:** Semana pasada.
- **L0W:** Semana actual (activa).

## Dimensiones Geográficas
- **COUNTRY:** AR, BR, CL, CO, CR, EC, MX, PE, UY.
- **CITY:** Nombre de la ciudad.
- **ZONE:** Zona operacional o barrio.
- **ZONE_TYPE:** Wealthy / Non Wealthy.
- **ZONE_PRIORITIZATION:** High Priority / Prioritized / Not Prioritized.
