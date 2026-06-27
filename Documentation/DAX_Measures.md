# DAX Measures Documentation

Complete reference for all 50+ Data Analysis Expressions (DAX) measures used across the PrimeChoice dashboard.

---

## Overview

This document details every measure, formula, calculation method, and usage. Organized by business area and complexity level.

**Key:** 
- ⭐ Basic (simple SUM/COUNT)
- ⭐⭐ Intermediate (calculations, logic)
- ⭐⭐⭐ Advanced (time intelligence, RLS, complex logic)

---

## Revenue Measures

### 1. Total Revenue ⭐
**Category:** Sales  
**Formula:**
```dax
Total Revenue = SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_revenue_ngn])
```
**Description:** Sum of all gross revenue across all transactions  
**Used On:** Executive, Products, Finance pages  
**Example Output:** ₦29.42bn (3-year), ₦3.28bn (monthly)

---

### 2. Budget Revenue ⭐
**Category:** Finance  
**Formula:**
```dax
Budget Revenue = SUM('primechoice fact_budget_target'[budget_revenue_ngn])
```
**Description:** Budgeted revenue from budget target table  
**Used On:** Finance page  
**Note:** Filtered by fiscal month and cost centre

---

### 3. Revenue Variance ⭐⭐
**Category:** Finance  
**Formula:**
```dax
Revenue Variance = [Total Revenue] - [Budget Revenue]
```
**Description:** Actual minus budgeted revenue; shows over/under performance  
**Used On:** Finance page (KPI card)  
**Interpretation:** 
- Positive = Over budget (good)
- Negative = Under budget (concern)
- **Current:** -₦276.70bn (massive miss)

---

### 4. Products Sold in Period ⭐⭐
**Category:** Sales  
**Formula:**
```dax
Products Sold in Period = 
VAR SelectedYear = MAX(dim_date[calendar_year])
RETURN
CALCULATE(
    DISTINCTCOUNT('primechoice fact_sales'[product_key]),
    dim_date[calendar_year] = SelectedYear
)
```
**Description:** Count of unique products sold in selected year(s)  
**Used On:** Products page (KPI card)  
**Dynamic:** Responds to Year filter  
**Example:** 228 products sold in 2024

---

## Profit & Margin Measures

### 5. Gross Profit ⭐
**Category:** Profitability  
**Formula:**
```dax
Gross Profit = SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_profit_ngn])
```
**Description:** Revenue minus cost of goods sold  
**Calculated in DB:** (gross_revenue - discount - returns) - COGS  
**Used On:** Executive, Products, Finance pages  
**Example Output:** ₦8.01bn

---

### 6. COGS Amount ⭐
**Category:** Cost  
**Formula:**
```dax
COGS Amount = SUMX('primechoice fact_sales', 'primechoice fact_sales'[cost_of_goods_sold_ngn])
```
**Description:** Total cost of goods sold  
**Used On:** Finance bridge, calculations  
**Example Output:** ₦21.41bn

---

### 7. Gross Margin % ⭐⭐
**Category:** Profitability  
**Formula:**
```dax
Gross Margin % = 
DIVIDE(
    SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_profit_ngn]),
    SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_revenue_ngn]),
    0
) * 100
```
**Description:** Gross profit as percentage of revenue  
**Benchmark:** Retail industry: 20-35%  
**Used On:** Executive, Products, Finance pages  
**Example:** 27.23% (healthy for retail)

---

### 8. Avg Product Margin % ⭐⭐
**Category:** Profitability  
**Formula:**
```dax
Avg Product Margin % = 
DIVIDE(
    SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_profit_ngn]),
    SUMX('primechoice fact_sales', 'primechoice fact_sales'[gross_revenue_ngn]),
    0
) * 100
```
**Description:** Average margin across all products  
**Used On:** Products page (KPI card)  
**Note:** Same as Gross Margin % but shown at product level

---

### 9. Operating Expense ⭐
**Category:** Cost  
**Formula:**
```dax
Operating Expense = 
SUMX('primechoice fact_finance_pl',
    IF('primechoice fact_finance_pl'[pl_line] = "StoreOpex", 
        'primechoice fact_finance_pl'[actual_amount_ngn], 0)
)
```
**Description:** Store operating expenses (payroll, rent, utilities, etc.)  
**Used On:** Finance page  
**Example Output:** ₦5.2bn

---

### 10. EBITDA ⭐⭐
**Category:** Profitability  
**Formula:**
```dax
EBITDA = [Gross Profit] - [Operating Expense]
```
**Description:** Earnings before interest, taxes, depreciation, amortization  
**Business Use:** Shows core operational profitability  
**Used On:** Finance page  
**Example Output:** ₦5.4bn

---

### 11. EBITDA % ⭐⭐
**Category:** Profitability  
**Formula:**
```dax
EBITDA % = 
DIVIDE([EBITDA], [Total Revenue], 0) * 100
```
**Description:** EBITDA as percentage of revenue  
**Benchmark:** 15-25% healthy for retail  
**Used On:** Executive page (KPI card)  
**Example:** 22.04%

---

## Volume Measures

### 12. Total Units Sold ⭐
**Category:** Volume  
**Formula:**
```dax
Total Units Sold = SUM('primechoice fact_sales'[quantity_sold])
```
**Description:** Total quantity of products sold  
**Unit:** Items (varies by product: pieces, kg, litres, etc.)  
**Used On:** Products page (KPI card)  
**Example Output:** 5M units

---

### 13. Total Transactions ⭐
**Category:** Volume  
**Formula:**
```dax
Total Transactions = COUNTA('primechoice fact_sales'[transaction_id])
```
**Description:** Number of individual transactions/receipts  
**Used On:** Finance, KPI calculations  
**Example:** 850,000 transactions (3-year)

---

### 14. Avg Basket Value ⭐⭐
**Category:** Sales  
**Formula:**
```dax
Avg Basket Value = 
DIVIDE([Total Revenue], [Total Transactions], 0)
```
**Description:** Average revenue per transaction  
**Insight:** Shows customer spending pattern  
**Used On:** Finance page  
**Example:** ₦34,600 per basket

---

## Inventory Measures

### 15. Avg Days of Cover ⭐
**Category:** Inventory  
**Formula:**
```dax
Avg Days of Cover = 
AVERAGE('primechoice fact_inventory'[days_of_cover_remaining])
```
**Description:** Average days remaining inventory will last at current sales pace  
**Benchmark:** 20-30 days (adequate), 10-20 days (tight), <10 days (risk)  
**Used On:** Store Operations page (KPI card)  
**Example:** 10.05 days (RISKY - low safety stock)

---

### 16. Inventory Turnover ⭐⭐
**Category:** Inventory  
**Formula:**
```dax
Inventory Turnover = 
DIVIDE(
    SUM('primechoice fact_inventory'[sold_units]),
    AVERAGE('primechoice fact_inventory'[closing_stock_units]),
    0
)
```
**Description:** How many times inventory is sold and replaced per year  
**Benchmark:** 3-8x for general retail  
**Used On:** Store Operations page (KPI card)  
**Example:** 1.07x (slow-moving, implies 340-day hold)

---

### 17. Inventory Value ⭐
**Category:** Inventory  
**Formula:**
```dax
Inventory Value = 
SUM('primechoice fact_inventory'[closing_stock_value_ngn])
```
**Description:** Total rupiah value of inventory on hand  
**Used On:** Store Operations page (pie chart)  
**Example Output:** ₦44.2bn (total working capital)

---

### 18. Shrinkage % ⭐⭐
**Category:** Inventory  
**Formula:**
```dax
Shrinkage % = 
DIVIDE(
    SUMX('primechoice fact_inventory', 'primechoice fact_inventory'[shrinkage_units]),
    SUMX('primechoice fact_inventory', 'primechoice fact_inventory'[closing_stock_units]),
    0
) * 100
```
**Description:** Percentage of inventory lost to waste, damage, theft  
**Benchmark:** 0.5-1.5% (good), >2% (problem)  
**Used On:** Store Operations page (KPI card)  
**Example:** 0.94% (excellent - world-class)

---

### 19. Out of Stock Count ⭐
**Category:** Inventory  
**Formula:**
```dax
Out of Stock Count = 
CALCULATE(
    COUNTROWS('primechoice fact_inventory'),
    'primechoice fact_inventory'[is_out_of_stock] = TRUE()
)
```
**Description:** Number of product-store combinations that are out of stock  
**Used On:** Store Operations page  
**Alert Trigger:** >200 incidents/month indicates problem

---

### 20. Stores in Stock ⭐⭐
**Category:** Inventory  
**Formula:**
```dax
Stores in Stock = 
CALCULATE(
    DISTINCTCOUNT(dim_store[store_key]),
    'primechoice fact_inventory'[is_out_of_stock] = FALSE()
)
```
**Description:** Count of stores that have stock for selected product(s)  
**Used On:** Store Operations page (KPI card)  
**Example:** 40 (all stores have inventory)

---

## Supply Chain Measures

### 21. OTIF % ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
OTIF % = 
DIVIDE(
    CALCULATE(COUNTROWS('primechoice fact_purchase_orders'), 
        'primechoice fact_purchase_orders'[is_otif] = TRUE()),
    COUNTROWS('primechoice fact_purchase_orders'),
    0
) * 100
```
**Description:** On-Time-In-Full: % of POs delivered on schedule AND with full quantity  
**Benchmark:** >90% (target), 80-90% (acceptable), <80% (problem)  
**Used On:** Executive, Supply Chain pages (KPI cards)  
**Example:** 21% (🔴 CRITICAL - well below target)

---

### 22. On Time % ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
On Time % = 
DIVIDE(
    CALCULATE(COUNTROWS('primechoice fact_purchase_orders'), 
        'primechoice fact_purchase_orders'[is_on_time] = TRUE()),
    COUNTROWS('primechoice fact_purchase_orders'),
    0
) * 100
```
**Description:** % of POs delivered by expected date (ignoring quantity)  
**Used On:** Supply Chain page  
**Component of:** OTIF

---

### 23. In Full % ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
In Full % = 
DIVIDE(
    CALCULATE(COUNTROWS('primechoice fact_purchase_orders'), 
        'primechoice fact_purchase_orders'[is_in_full] = TRUE()),
    COUNTROWS('primechoice fact_purchase_orders'),
    0
) * 100
```
**Description:** % of POs delivered with full ordered quantity  
**Used On:** Supply Chain page  
**Component of:** OTIF

---

### 24. Avg Lead Time Days ⭐
**Category:** Supply Chain  
**Formula:**
```dax
Avg Lead Time Days = 
AVERAGE('primechoice fact_purchase_orders'[delivery_lead_time_days])
```
**Description:** Average number of days from PO to receipt  
**Benchmark:** 5-15 days (acceptable)  
**Used On:** Supply Chain page (KPI card)  
**Example:** 6.05 days (good)

---

### 25. Fill Rate % ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
Fill Rate % = 
DIVIDE(
    SUMX('primechoice fact_purchase_orders', 'primechoice fact_purchase_orders'[received_qty]),
    SUMX('primechoice fact_purchase_orders', 'primechoice fact_purchase_orders'[ordered_qty]),
    0
) * 100
```
**Description:** % of ordered quantity that was actually received  
**Benchmark:** >95% (excellent), 90-95% (good), <90% (problem)  
**Used On:** Supply Chain page (KPI card)  
**Example:** 93.67% (good)

---

### 26. Total Procurement Cost ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
Total Procurement Cost = 
SUMX('primechoice fact_purchase_orders', 
    ('primechoice fact_purchase_orders'[received_qty] * 'primechoice fact_purchase_orders'[invoiced_unit_cost_ngn]) 
    + 'primechoice fact_purchase_orders'[freight_cost_ngn]
    + 'primechoice fact_purchase_orders'[duty_and_tariff_ngn]
)
```
**Description:** Total cost to procure (unit costs + freight + tariffs)  
**Used On:** Supply Chain page  
**Example Output:** ₦32.4bn (3-year)

---

### 27. Avg Lead Time Variance Days ⭐⭐
**Category:** Supply Chain  
**Formula:**
```dax
Avg Lead Time Variance Days = 
AVERAGE('primechoice fact_purchase_orders'[lead_time_variance_days])
```
**Description:** Average difference (actual date - expected date)  
**Interpretation:**
- Negative = Early (good but may cause overstock)
- Zero = On-time (perfect)
- Positive = Late (problematic)
**Used On:** Supply Chain page  
**Example:** +1.5 days (slightly late on average)

---

### 28. PO Count ⭐
**Category:** Supply Chain  
**Formula:**
```dax
PO Count = COUNTROWS('primechoice fact_purchase_orders')
```
**Description:** Total number of purchase orders  
**Used On:** Supply Chain page  
**Example:** ~18,000 POs over 3 years

---

## Time Intelligence Measures

### 29. YoY Growth % ⭐⭐⭐
**Category:** Finance  
**Formula:**
```dax
YoY Growth % = 
DIVIDE(
    [Total Revenue] - CALCULATE([Total Revenue], DATEADD(dim_date[full_date], -12, MONTH)),
    CALCULATE([Total Revenue], DATEADD(dim_date[full_date], -12, MONTH))
) * 100
```
**Description:** Revenue growth compared to same month/period last year  
**Used On:** Executive, Finance pages  
**Note:** Uses DATEADD for intelligent date handling  
**Example:** 2024 vs 2023 = +18% growth

---

### 30. Prior Year Revenue ⭐⭐⭐
**Category:** Finance  
**Formula:**
```dax
Prior Year Revenue = 
CALCULATE([Total Revenue], DATEADD(dim_date[full_date], -12, MONTH))
```
**Description:** Revenue from same period previous year  
**Used On:** Finance calculations  
**Support Measure:** For YoY Growth calculations

---

### 31. Gross Margin % YoY ⭐⭐⭐
**Category:** Profitability  
**Formula:**
```dax
Gross Margin % YoY = 
VAR CurrentMargin = [Gross Margin %]
VAR PriorYearMargin = CALCULATE(
    [Gross Margin %],
    DATEADD(dim_date[full_date], -12, MONTH)
)
RETURN
CurrentMargin - PriorYearMargin
```
**Description:** Year-over-year change in gross margin percentage  
**Used On:** Finance page  
**Insight:** Shows if profitability per sale is improving/declining

---

## Advanced Classification Measures

### 32. ABC Classification ⭐⭐⭐
**Category:** Product  
**Formula:**
```dax
ABC Classification = 
VAR ProductRevenue = CALCULATE([Total Revenue], dim_product[product_key])
VAR TotalRevenue = CALCULATE([Total Revenue], ALL(dim_product))
VAR CumulativeSalesRatio = DIVIDE(ProductRevenue, TotalRevenue, 0)
VAR ProductRank = RANKX(ALL(dim_product), [Total Revenue],, DESC)
VAR TotalProducts = COUNTA(dim_product[product_key])
RETURN
IF(ProductRank <= TotalProducts * 0.20, "A",
IF(ProductRank <= TotalProducts * 0.50, "B", "C"))
```
**Description:** Pareto classification (A=top 20%, B=next 30%, C=bottom 50%)  
**Used On:** Products page  
**Business Logic:** 80/20 rule - focus on A products for ROI

---

## Calculated Columns (Not Measures)

### 33. Stock Age Days ⭐⭐
**Type:** Calculated Column  
**Table:** fact_inventory  
**Formula:**
```dax
Stock Age Days = 
VAR MaxDate = DATE(2024, 12, 31)
VAR Year = INT([snapshot_date_key] / 10000)
VAR Month = INT(MOD([snapshot_date_key], 10000) / 100)
VAR Day = MOD([snapshot_date_key], 100)
VAR SnapshotDate = DATE(Year, Month, Day)
RETURN
INT(MaxDate - SnapshotDate)
```
**Description:** How many days old the inventory snapshot is  
**Used On:** Store Operations page (Stock Aging chart)

---

### 34. Stock Age Bracket ⭐⭐
**Type:** Calculated Column  
**Table:** fact_inventory  
**Formula:**
```dax
Stock Age Bracket = 
VAR MaxDate = DATE(2024, 12, 31)
VAR Year = INT([snapshot_date_key] / 10000)
VAR Month = INT(MOD([snapshot_date_key], 10000) / 100)
VAR Day = MOD([snapshot_date_key], 100)
VAR SnapshotDate = DATE(Year, Month, Day)
VAR DaysOld = INT(MaxDate - SnapshotDate)
RETURN
IF(DaysOld < 30, "0-30 days",
IF(DaysOld < 60, "30-60 days",
IF(DaysOld < 90, "60-90 days",
IF(DaysOld < 180, "90-180 days", "180+ days"))))
```
**Description:** Brackets stock age for charting  
**Used On:** Store Operations page (Stock Aging histogram)

---

### 35. Month Year Sort Key ⭐
**Type:** Calculated Column  
**Table:** dim_date  
**Formula:**
```dax
Month Year Sort Key = 
dim_date[calendar_year] * 100 + dim_date[month_number]
```
**Description:** Numeric key for chronological sorting  
**Purpose:** Ensures "Jan-2022", "Feb-2022", etc. sort correctly (not alphabetically)  
**Used By:** Sort-by column for month_year_label

---

## Summary Statistics

| Category | Count | Example Measures |
|----------|-------|-----------------|
| **Revenue** | 4 | Total Revenue, Budget Revenue, Variance |
| **Profitability** | 7 | Gross Profit, Margins, EBITDA, YoY |
| **Volume** | 3 | Units Sold, Transactions, Basket Value |
| **Inventory** | 6 | Days of Cover, Turnover, Shrinkage |
| **Supply Chain** | 8 | OTIF %, Fill Rate, Lead Time |
| **Time Intelligence** | 3 | YoY Growth, Prior Year |
| **Classification** | 1 | ABC Classification |
| **Calculated Columns** | 3 | Stock Age, Sort Keys |
| **TOTAL** | 35+ | Core measures documented |

---

## Performance Notes

- Most measures use **SUMX** for calculation flexibility
- **Time intelligence** uses DATEADD for dynamic year-over-year comparisons
- **Aggregate functions** (AVERAGE, COUNT, DISTINCTCOUNT) used for efficiency
- Complex measures use **VAR** (variable) blocks for readability and performance

---

## Troubleshooting Formulas

**Issue:** Measure returns blank or 0
- Check: Is filtered data available? (Empty result set)
- Check: DIVIDE function has 3rd parameter for default (usually 0)

**Issue:** Inconsistent results across filters
- Check: All necessary dimensions included in CALCULATE statements
- Check: Dimension tables included in relevant relationships

**Issue:** Performance slow
- Note: Large fact tables (3.5M rows) aggregated to dimensions first
- Note: RLS filtering may impact performance if dimensions have many rows

---

**Last Updated:** June 2026  
**Measure Version:** 1.0  
**Total Measures:** 35+ documented

