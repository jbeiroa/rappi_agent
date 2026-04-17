# Data Dictionary: Rappi Operational Metrics

This document defines the metrics available in the `dummy_data.xlsx` dataset and their business logic.

| Metric | Description |
| :--- | :--- |
| **% PRO Users Who Breakeven** | Pro subscribers whose generated value (comissions, etc.) covers their membership cost / Total Pro users. |
| **% Restaurants Sessions With Optimal Assortment** | Sessions with at least 40 restaurants / Total sessions. |
| **Gross Profit UE** | Gross Profit Margin / Total Orders. |
| **Lead Penetration** | Enabled stores / (Prospect leads + Enabled stores + Churned stores). |
| **MLTV Top Verticals Adoption** | Users with orders in multiple verticals (Restaurantes, Super, Pharmacy, Liquors) / Total users. |
| **Non-Pro PTC > OP** | Conversion from "Proceed to Checkout" to "Order Placed" for Non-Pro users. |
| **Perfect Orders** | Orders without cancellations, defects, or delays / Total orders. |
| **Pro Adoption** | Pro subscribers / Total Rappi users. |
| **Restaurants Markdowns / GMV** | Total discounts in restaurant orders / Total Gross Merchandise Value (GMV) for Restaurants. |
| **Restaurants SS > ATC CVR** | Conversion in restaurants from "Select Store" to "Add to Cart". |
| **Restaurants SST > SS CVR** | % of users who select a specific restaurant after selecting the Restaurant vertical. |
| **Retail SST > SS CVR** | % of users who select a specific store after selecting the Supermarkets vertical. |
| **Turbo Adoption** | Total Turbo users / Total users with Turbo available in their zone. |
| **Orders** | Total volume of orders placed in the zone. |

## Data Structure (Weekly)
All metrics and orders are provided for the last 8 weeks:
- **L8W:** 8 weeks ago
- **L7W:** 7 weeks ago
- ...
- **L1W:** Last week
- **L0W:** Current week (active)

## Geographic Dimensions
- **COUNTRY:** AR, BR, CL, CO, CR, EC, MX, PE, UY.
- **CITY:** City name.
- **ZONE:** Operational zone or neighborhood.
- **ZONE_TYPE:** Wealthy / Non Wealthy.
- **ZONE_PRIORITIZATION:** High Priority / Prioritized / Not Prioritized.
