# Dashboard Pages Overview

Detailed guide to each of the 5 dashboard pages, including purpose, metrics, visuals, and key insights.

---

## Page 1: Executive Scorecard

**Audience:** CEO, Group Managing Director, C-Suite Executives
**Refresh Frequency:** Daily
**Use Case:** Strategic performance review, board reporting

### Purpose
High-level overview of business health across key dimensions. Redesigned around a "less is more" principle — three focused, larger visuals instead of five smaller ones, each answering a distinct executive question.

### KPI Cards (Top Row)

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Revenue** | ₦29.42bn | Cumulative 3-year sales performance |
| **Gross Profit** | ₦8.01bn | Profit before operating expenses |
| **Gross Margin %** | 27.23% | Profitability per sale (industry benchmark: 25-30%) |
| **EBITDA %** | 22.04% | Operating efficiency |

### Chart 1: Monthly Revenue Performance
- **Title:** Monthly Revenue Performance
- **Subtitle (Question):** *How accurately did our forecasts predict actual revenue each month?*
- **Type:** Combo chart (columns + line)
- **Insight:** Budget line consistently sits above actual revenue; forecast model is systemically misaligned
- **Action:** Investigate budget realism; reconcile forecast methodology against actual sales drivers

### Chart 2: Revenue Growth Trajectory
- **Title:** Revenue Growth Trajectory
- **Subtitle (Question):** *How did revenue performance compare across years?*
- **Type:** Multi-line chart (2023 vs 2024)
- **Insight:** Both years follow a similar seasonal rhythm, with 2024 showing stronger peaks
- **Action:** Use the repeatable seasonal pattern to plan inventory and staffing

### Chart 3: Regional Revenue Distribution
- **Title:** Regional Revenue Distribution
- **Subtitle (Question):** *Which regions contribute most to our revenue?*
- **Type:** Geographic map (Nigeria) + ranked bar list
- **Top Regions:** Lagos (₦5.1bn), Oyo (₦4.4bn), FCT (₦3.6bn), Rivers (₦3.3bn), Ogun (₦3.2bn)
- **Insight:** Revenue is concentrated in the Southwest corridor
- **Action:** Evaluate expansion opportunity in underrepresented regions

### Chart 4: Gross Profit Trend
- **Title:** Gross Profit Trend
- **Subtitle (Question):** *Did profitability remain resilient despite operational challenges?*
- **Type:** Line chart (monthly gross profit)
- **Insight:** Profit climbs steadily through the year and accelerates sharply in December, confirming margin resilience even amid forecast and supply chain issues
- **Action:** Protect the cost discipline driving this resilience as the business scales

### Removed From This Page
- Revenue by Product Category (moved deeper into Page 2's product-level analysis — redundant at executive level)

### Slicers
- **Region:** SW-NG, SS-NG, SE-NG, NC-NG (or All)
- **Year:** 2022, 2023, 2024 (or All)

### Key Questions This Page Answers
1. How accurately are we forecasting revenue?
2. Is revenue growth continuing year over year?
3. Which regions drive the business?
4. Is profitability holding up despite known operational problems?

---

## Page 2: Sales & Product Performance

**Audience:** Category Managers, Product Managers, Marketing Team
**Refresh Frequency:** Weekly
**Use Case:** Product strategy, pricing decisions, promotion planning

### Purpose
Product-level performance view, now built around profitability rather than raw sales volume. Focused catalog of 228 active SKUs with 100% utilization.

### KPI Cards (Top Row)

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Units Sold** | 5M units | Volume metric |
| **Avg Product Margin %** | 27.23% | Average profitability across all products |
| **Active SKUs** | 228 | Full catalog utilization — every SKU is selling |

### Chart 1: Product Profitability Analysis
- **Title:** Product Profitability Analysis
- **Subtitle (Question):** *Which products balanced volume and margin most effectively?*
- **Type:** Scatter chart (X: Total Revenue, Y: Margin %, Bubble: Units Sold)
- **Insight:** Product mix spans high-volume/low-margin commodities and low-volume/high-margin niche items, including one outlier bubble near ₦4bn revenue
- **Action:** Identify products in the top-right quadrant (high revenue + high margin) for expanded promotion

### Chart 2: Revenue Trend by Product Category
- **Title:** Revenue Trend by Product Category
- **Subtitle (Question):** *What seasonal patterns did each category follow?*
- **Type:** Multi-line chart (Audio & TV, Footwear, Phones & Accessories, Small Appliances, Womens Clothing)
- **Insight:** Audio & TV leads throughout the year with a pronounced December uplift shared across categories
- **Action:** Plan category-specific seasonal promotions around the observed December pattern

### Chart 3: Top Products by Profit Contribution *(New)*
- **Title:** Top Products by Profit Contribution
- **Subtitle (Question):** *Which products generated the most profit, and which ones should we prioritize?*
- **Type:** Ranked horizontal bar chart
- **Top Products:** PrimeChoice Footwear (₦154M), PrimeChoice Womens (₦141M), Chi Limited Footwear (₦139M), Golden Penny Womens (₦132M)
- **Insight:** The highest-*revenue* products (from Page 1's category view) are not always the highest-*profit* products — footwear and womenswear outperform on profit contribution despite Audio & TV leading on revenue
- **Action:** Prioritize inventory and promotional spend based on profit contribution, not revenue alone; investigate why top-revenue categories don't top the profit list

### Removed From This Page
- Sales by Department (Treemap) — redundant with Revenue Trend by Category
- Top 5 Products by Revenue — replaced by the more actionable Top Products by *Profit* view

### Slicers
- **Category:** All categories, Audio & TV, Phones, etc.
- **Region:** All regions
- **Year:** All years

### Key Questions This Page Answers
1. Which products balance volume and margin best?
2. How do categories move seasonally?
3. Which products should we actually prioritize — by profit, not just revenue?

---

## Page 3: Store Operations & Inventory

**Audience:** Store Managers, Regional Directors, Operations Team
**Refresh Frequency:** Weekly/Daily for alerts
**Use Case:** Inventory management, out-of-stock prevention, shrinkage control

### Purpose
Store-level operational health, restructured into a clean 2x2 grid for readability.

### KPI Cards (Top Row)

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Stores in Network** | 40 | Complete store count across all regions |
| **Avg Days of Cover** | 10.05 | Inventory lasts ~10 days on average — lean, low safety margin |
| **Shrinkage %** | 0.94% | Waste rate is excellent (world-class is <1%) |

### Chart 1: Out-of-Stock Trend
- **Title:** Out-of-Stock Trend
- **Subtitle (Question):** *How often did we experience inventory shortages during this period?*
- **Type:** Line chart (monthly incident count)
- **Insight:** Incidents dip mid-year and climb sharply from October into December
- **Action:** Investigate whether the December spike reflects supplier delays or a demand surge; pre-position stock ahead of the next seasonal peak

### Chart 2: Stock Turnover by Department *(New)*
- **Title:** Stock Turnover by Department
- **Subtitle (Question):** *How quickly did inventory turn in each department?*
- **Type:** Column chart
- **Values:** Food (0.69), Non-Food (0.14), Household (0.10), Clothing (0.09), Health (0.08), Electronics (0.07)
- **Insight:** Food turns over roughly 5-10x faster than every other department — consistent with its perishability and the higher shrinkage rate seen in Chart 3
- **Action:** Use Food's turnover model where applicable to reduce excess capital tied up in slower-moving departments (Non-Food, Household, Electronics)

### Chart 3: Shrinkage % by Department
- **Title:** Shrinkage % by Department
- **Subtitle (Question):** *Which departments experienced the highest inventory loss rates?*
- **Type:** Ranked horizontal bar chart
- **Values:** Food (1.28%), Health/Household/Electronics/Non-Food (0.80% each)
- **Insight:** Food is the only department above the network average, consistent with its perishable nature
- **Action:** Tighten cold-chain and expiry management for Food; maintain current controls elsewhere

### Chart 4: Inventory Value by Department
- **Title:** Inventory Value by Department
- **Subtitle (Question):** *Which departments held the most inventory capital?*
- **Type:** Pie chart
- **Values:** Electronics ₦44.9bn+ (63%+ of capital), Non-Food ₦9.56bn, Household, Food ₦5.3bn+, Clothing
- **Insight:** Electronics represents by far the largest share of working capital, despite the lowest turnover and shrinkage of any department
- **Action:** Prioritize Electronics for inventory optimization — largest capital base with the most room to improve turnover

### Removed From This Page
- Out-of-Stock Alert List (product/store detail table) — moved to operational drill-down; not strategic for this view
- Inventory Days of Cover by Store — showed a data inconsistency (uniform 25-day reading across all stores against a 10.05-day network average); removed pending reconciliation with source data

### Slicers
- **Region:** View regional store performance
- **Store:** Drill into individual store inventory
- **Year:** Track inventory health over time

### Key Questions This Page Answers
1. How often are we running out of stock, and is it worsening?
2. Which departments turn inventory fastest, and which are slow-moving?
3. Where are we losing product to shrinkage?
4. Where is our inventory capital actually tied up?

---

## Page 4: Supply Chain & Logistics

**Audience:** Supply Chain Lead, Procurement Manager, Logistics Team
**Refresh Frequency:** Daily
**Use Case:** Supplier performance, cost control, delivery reliability

### Purpose
Supplier and logistics performance tracking, now including a cost-vs-reliability matrix to guide supplier intervention priorities.

### KPI Cards (Top Row)

| Metric | Value | Insight |
|--------|-------|---------|
| **OTIF %** | 21% | On-Time-In-Full performance (target: >90%) 🔴 CRITICAL |
| **Avg Lead Time** | 6.05 days | Within acceptable range (5-10 days) ✅ |
| **Fill Rate %** | 93.67% | Close to target (>95%) ✅ |

🔴 **CRITICAL ALERT:** OTIF of 21% is severely below target. Top 5 suppliers all score 63-67% (vs 90% target), indicating a systemic, network-wide delivery failure rather than an isolated vendor issue.

### Chart 1: Supplier OTIF Scorecard
- **Title:** Supplier OTIF Scorecard
- **Subtitle (Question):** *Which suppliers consistently met delivery targets?*
- **Type:** Ranked horizontal bar chart with 90% reference line
- **Values:** Flour Mills of Nigeria (67.11%), Coca-Cola HBC (66.20%), Dufil Prima Foods (64.20%), Dangote Industries (64.17%), Unilever Nigeria (63.41%)
- **Insight:** Every top supplier falls 23-27 points short of target — there is no "reliable" supplier to lean on
- **Action:** 🔴 Escalate immediately; renegotiate SLAs across the board or begin qualifying alternative suppliers

### Chart 2: Supplier Performance Matrix *(New)*
- **Title:** Supplier Performance Matrix
- **Subtitle (Question):** *Which suppliers offer the best balance of cost efficiency and on-time delivery?*
- **Type:** Scatter/bubble chart (X: OTIF %, Y: Cost, Bubble: Spend), with reference line
- **Insight:** The bulk of suppliers cluster in the low-OTIF range, with a smaller cluster of higher-OTIF, higher-cost suppliers further right — visually confirming that reliability and cost are currently in tension across the supply base
- **Action:** Use this view to identify which suppliers to renegotiate (low OTIF, low cost) versus which to protect as reliable partners (higher OTIF), even at a cost premium

### Chart 3: Supplier Spend Distribution
- **Title:** Supplier Spend Distribution
- **Subtitle (Question):** *How concentrated is our supplier dependency?*
- **Type:** Pareto/combo chart (bars + cumulative % line)
- **Top Suppliers by Spend:** DHL Supply Chain (₦394M), Lagos Fresh Farms (₦353M), Nestle Nigeria (₦325M), Flour Mills of Nigeria (₦308M), De-United Foods (₦247M)
- **Insight:** Spend is concentrated among a handful of suppliers, creating dependency risk on top of the existing reliability problem
- **Action:** Develop qualified backup suppliers for the top spend categories to reduce single-source exposure

### Chart 4: Procurement Cost Movement
- **Title:** Procurement Cost Movement
- **Subtitle (Question):** *How did procurement costs trend throughout the period, and were there seasonal patterns?*
- **Type:** Stacked area chart (Regular vs Strategic suppliers)
- **Insight:** Costs rise steadily into year-end, peaking in December alongside the seasonal demand spike seen on Pages 1-3
- **Action:** Pre-negotiate Q4 pricing and lock in contracts ahead of the seasonal cost run-up

### Removed From This Page
- Lead Time Variance Analysis — superseded by the Supplier Performance Matrix, which combines reliability and cost in one view
- PO Delivery Performance (On-Time/Late pie) — redundant with OTIF Scorecard; the two metrics told conflicting stories since OTIF is the stricter (on-time AND in-full) measure

### Slicers
- **Supplier:** Filter to specific supplier performance
- **Region:** View supplier performance by region served
- **Year:** Track supplier reliability over time

### Key Questions This Page Answers
1. Which suppliers consistently met delivery targets?
2. Which suppliers offer the best balance of cost and reliability?
3. How dependent are we on a small number of suppliers?
4. How did procurement costs move over the period?

---

## Page 5: Finance & P&L Bridge

**Audience:** Finance Director, CFO, Finance Analysts, Board
**Refresh Frequency:** Monthly (after month-close)
**Use Case:** Budget variance analysis, profitability tracking, financial reporting

### Purpose
Monthly profit & loss analysis with budget comparison, now extended down to store-level profit performance.

### KPI Cards (Top Row)

| Metric | Value | Insight |
|--------|-------|---------|
| **Total Revenue** | ₦29.42bn | Cumulative 3-year revenue |
| **Gross Profit** | ₦8.01bn | Revenue minus COGS |
| **Revenue Variance** | -₦276.70bn | Actual vs Budget 🔴 CRITICAL MISS |

🔴 **ALERT:** A variance of this scale points to a forecasting model that is fundamentally misaligned with actual sales performance, not a minor shortfall.

### Chart 1: Profit & Loss Bridge
- **Title:** Profit & Loss Bridge
- **Subtitle (Question):** *How did revenue convert to profit through each stage of cost?*
- **Type:** Waterfall chart (Revenue → Gross Profit → EBITDA → Opex → COGS → Total)
- **Insight:** COGS is the single largest drain on profitability, followed by Opex
- **Action:** Prioritize COGS reduction through supplier renegotiation; pair with the Supplier Performance Matrix on Page 4 to target the right suppliers

### Chart 2: Revenue: Actual vs Forecast Accuracy
- **Title:** Revenue: Actual vs Forecast Accuracy
- **Subtitle (Question):** *How consistently did actual revenue align with our forecasts across the period?*
- **Type:** Combo chart (columns + variance line)
- **Insight:** Budget consistently overshoots actual revenue across nearly every month
- **Action:** Rebuild the forecasting model using observed seasonal patterns rather than top-down targets

### Chart 3: Revenue Growth: Annual Comparison
- **Title:** Revenue Growth: Annual Comparison
- **Subtitle (Question):** *How did revenue trajectory compare across 2022, 2023, and 2024?*
- **Type:** Clustered column chart
- **Insight:** Each year outpaces the last, with December consistently the strongest month across all three years
- **Action:** Use the three-year seasonal pattern as the foundation for next year's (more realistic) budget

### Chart 4: Top Stores by Profit Contribution *(New)*
- **Title:** Top Stores by Profit Contribution
- **Subtitle (Question):** *Which store locations generated the most profit, and which ones are underperforming?*
- **Type:** Ranked horizontal bar chart
- **Top Stores:** PrimeChoice Abeokuta (₦526M), PrimeChoice Ibadan (₦522M), PrimeChoice Lagos (₦516M), PrimeChoice Port Harcourt (₦452M), PrimeChoice Kaduna (₦434M)
- **Insight:** Abeokuta leads on profit despite Lagos and Oyo dominating overall regional revenue on Page 1 — a strong signal that store-level operating efficiency, not just regional market size, is driving profitability
- **Action:** Study Abeokuta's operating model (pricing, staffing, cost control) as a template for underperforming stores in higher-revenue regions

### Removed From This Page
- Monthly P&L Summary Table — too granular for the strategic view; retained as a drill-down/export rather than a dashboard visual
- Profitability Margins Trend — margins were confirmed stable (a positive validation rather than a problem to solve); removed to keep the page focused on the forecast-gap and store-profit story

### Slicers
- **Cost Centre:** Filter to specific business unit P&L
- **Region:** View regional profitability
- **Year:** Compare year-over-year P&L

### Key Questions This Page Answers
1. How did revenue convert to profit?
2. How consistently did we hit our forecasts?
3. Is revenue growth continuing year over year?
4. Which stores actually drive profit, regardless of regional revenue size?

---

## Cross-Page Navigation

**Navigation Buttons (Left Sidebar):**
- Dashboard icon → Executive Scorecard (Page 1)
- Boxes icon → Sales & Products (Page 2)
- Store icon → Store Operations (Page 3)
- Logistics icon → Supply Chain (Page 4)
- Finance icon → Finance & P&L Bridge (Page 5)

---

## Common Slicer Behavior

### Page 1 (Executive Scorecard)
- **Region:** SW-NG, SS-NG, SE-NG, NC-NG (or All)
- **Year:** 2022, 2023, 2024 (or All)

### Page 2 (Sales & Products)
- **Category:** All categories, Audio & TV, Phones & Accessories, Small Appliances, Clothing, etc.
- **Region:** All regions
- **Year:** All years

### Page 3 (Store Operations)
- **Region:** Filter stores by region first
- **Store:** Specific store selection
- **Year:** Time period filter

### Page 4 (Supply Chain)
- **Supplier:** Individual supplier focus (All, or specific suppliers)
- **Region:** Regional supplier performance
- **Year:** Historical supplier tracking

### Page 5 (Finance)
- **Cost Centre:** Business unit P&L
- **Region:** Regional profitability
- **Year:** Year-over-year comparison

**Slicer Strategy:** Start broad (All), then drill down to specific region/store/supplier for deep analysis.

---

## Performance Notes

- Dashboard refreshes **daily** from MySQL database
- Large datasets (3.5M transactions) use **aggregated views** for performance
- All visuals respond to slicer selections with cross-filtering
- Row-level security ensures users see only authorized data
- Chart counts were deliberately reduced across all pages (from 23 total visuals to 18) to prioritize clarity and executive scan-ability over exhaustive detail

---

## Critical Alerts Summary

| Alert | Page | Severity | Action Required |
|-------|------|----------|-----------------|
| OTIF 21% | Exec, Supply Chain | 🔴 CRITICAL | Immediate supplier intervention; SLA renegotiation |
| Revenue Variance -₦276.70bn | Finance | 🔴 CRITICAL | Reconcile budget assumptions; sales target review |
| Days of Cover 10.05 days | Store Ops | 🟠 WARNING | Increase safety stock; improve forecasting |
| Supplier Concentration (top suppliers) | Supply Chain | 🟠 WARNING | Develop backup suppliers; reduce dependency |
| Inventory Days of Cover by Store (data inconsistency) | Store Ops | ⚪ DATA ISSUE | Chart removed pending reconciliation with 10.05-day network average |

---

**Last Updated:** July 2026
**Dashboard Version:** 2.0 (Refined — "Less is More" redesign)
