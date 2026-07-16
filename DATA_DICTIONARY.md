# PrimeChoice Retail Group — Data Dictionary

**Database:** primechoice  
**Currency:** Nigerian Naira (NGN)  
**Data Period:** 2022-01-01 to 2024-12-31  
**Records Generated:** ~3.5 million transactions + supporting data

---

## DIMENSION TABLES

### **dim_date**
**Purpose:** Calendar dimension with fiscal year tracking and Nigerian holidays  
**Grain:** One row per day (1,096 rows)  
**Key:** date_key (YYYYMMDD integer)

| Column | Type | Description |
|--------|------|-------------|
| date_key | INT | Primary key (YYYYMMDD format, e.g., 20220115) |
| full_date | DATE | Full date in YYYY-MM-DD format |
| day_of_week | INT | 1=Monday, 7=Sunday |
| day_name | VARCHAR | Monday, Tuesday, etc. |
| day_of_month | INT | 1-31 |
| day_of_year | INT | 1-366 |
| week_of_year | INT | 1-53 (ISO week) |
| iso_week | INT | ISO 8601 week number |
| week_start_date | DATE | Start date of the week |
| month_number | INT | 1-12 |
| month_name | VARCHAR | January, February, etc. |
| month_short | VARCHAR | Jan, Feb, etc. |
| quarter | INT | 1-4 |
| quarter_name | VARCHAR | Q1, Q2, Q3, Q4 |
| calendar_year | INT | 2022, 2023, 2024 |
| fiscal_week | INT | 1-52 (PrimeChoice fiscal year starts Feb) |
| fiscal_month | INT | 1-12 (Feb=1, Jan=12) |
| fiscal_quarter | INT | 1-4 |
| fiscal_year | INT | Fiscal year (e.g., 2022 = FY2022/2023) |
| fiscal_year_label | VARCHAR | FY22/23, FY23/24, etc. |
| is_weekend | TINYINT | 1=Sat/Sun, 0=Weekday |
| is_public_holiday | TINYINT | 1=Nigerian public holiday |
| holiday_name | VARCHAR | Name of holiday (e.g., "Christmas Day") |
| is_trading_day | TINYINT | 1=Store open, 0=Store closed (Sundays) |
| is_last_day_of_month | TINYINT | 1=EOM, 0=Other |
| is_last_day_of_quarter | TINYINT | 1=EOQ, 0=Other |
| month_year_label | VARCHAR | Jan-2022, Feb-2022, etc. |
| quarter_year_label | VARCHAR | Q1-2022, Q2-2022, etc. |

**Usage:** All fact tables join on date_key for time-based analysis

---

### **dim_store**
**Purpose:** Store master with location, format, and region  
**Grain:** One row per store (40 rows)  
**Key:** store_key (surrogate), store_id (business key)  
**Type:** SCD Type 2 (tracks history)

| Column | Type | Description |
|--------|------|-------------|
| store_key | INT | Primary key (surrogate) |
| store_id | VARCHAR | Business key (e.g., "SW-LAG-001") |
| store_name | VARCHAR | e.g., "PrimeChoice Lagos Hypermarket 1" |
| store_format | VARCHAR | Hypermarket, Supermarket, Express, Convenience, Outlet |
| store_status | VARCHAR | Active, Closed, Dormant |
| open_date | DATE | Store opening date |
| close_date | DATE | Store closing date (NULL if still open) |
| sales_floor_sqm | DECIMAL | Sales floor area in square meters |
| num_checkouts | INT | Number of checkout tills |
| has_car_park | TINYINT | 1=Yes, 0=No |
| has_cafe | TINYINT | 1=Yes (Hypermarkets only), 0=No |
| has_pharmacy | TINYINT | 1=Yes (Hypermarkets/Supermarkets), 0=No |
| address_line1 | VARCHAR | Street address |
| city | VARCHAR | Lagos, Abuja, Port Harcourt, Enugu, Ibadan, etc. |
| state_province | VARCHAR | State/region in Nigeria |
| post_code | VARCHAR | Postal code (NULL for Nigeria) |
| country | VARCHAR | Nigeria |
| country_code | VARCHAR | NG |
| latitude | DECIMAL | GPS latitude |
| longitude | DECIMAL | GPS longitude |
| cluster_name | VARCHAR | e.g., "Lagos Metro" |
| region_name | VARCHAR | South West, South South, South East, North Central |
| region_code | VARCHAR | SW-NG, SS-NG, SE-NG, NC-NG |
| division_name | VARCHAR | Nigeria West, Nigeria South, Nigeria North |
| row_effective_date | DATE | SCD Type 2: when record became active |
| row_expiry_date | DATE | SCD Type 2: when record expired (9999-12-31 = current) |
| is_current | TINYINT | 1=Current record, 0=Historical |

**Usage:** Slice by region, format, city; analyze store-level performance

---

### **dim_product**
**Purpose:** Product master with pricing, margins, and classification  
**Grain:** One row per SKU (520 rows)  
**Key:** product_key (surrogate), product_id (business key)  
**Type:** SCD Type 2

| Column | Type | Description |
|--------|------|-------------|
| product_key | INT | Primary key (surrogate) |
| product_id | VARCHAR | Business key (e.g., "SKU-000001") |
| product_name | VARCHAR | Full product name |
| product_name_short | VARCHAR | Truncated name for reports |
| brand_name | VARCHAR | Brand (PrimeChoice own label, Dangote, Unilever, etc.) |
| is_own_label | TINYINT | 1=PrimeChoice own brand, 0=Vendor brand |
| sub_category_name | VARCHAR | e.g., "Fresh Produce", "Bakery" |
| category_name | VARCHAR | Same as sub_category (for convenience) |
| department_name | VARCHAR | Food, Non-Food, Household, Electronics, Clothing, Health |
| division_name | VARCHAR | Same as department |
| unit_of_measure | VARCHAR | Each, Kg, Litre, Pack |
| pack_size | DECIMAL | Size of pack in UOM |
| is_perishable | TINYINT | 1=Perishable (fresh produce), 0=Non-perishable |
| is_age_restricted | TINYINT | 1=Age 18+ required (Pharmacy OTC), 0=None |
| min_age_required | INT | Minimum age (18 for Pharmacy) |
| is_online_only | TINYINT | 1=Available online only, 0=Available in stores |
| is_store_only | TINYINT | 1=Available in store only, 0=Available online |
| retail_price_ngn | DECIMAL | Recommended retail price in NGN |
| cost_price_ngn | DECIMAL | Product cost in NGN |
| target_margin_pct | DECIMAL | Target gross margin % |
| vat_rate_pct | DECIMAL | VAT rate (7.5% standard) |
| product_status | VARCHAR | Live, Discontinued, Coming Soon |
| launch_date | DATE | Product launch date |
| discontinued_date | DATE | Discontinuation date (NULL if still active) |
| row_effective_date | DATE | SCD Type 2: effective date |
| row_expiry_date | DATE | SCD Type 2: expiry date |
| is_current | TINYINT | 1=Current product, 0=Historical |

**Usage:** Product hierarchy (Department → Category), margin analysis, brand mix

---

### **dim_customer**
**Purpose:** Customer master with loyalty segmentation  
**Grain:** One row per loyalty member + ANON-0000 placeholder (5,001 rows)  
**Key:** customer_key (surrogate), customer_id (business key)

| Column | Type | Description |
|--------|------|-------------|
| customer_key | INT | Primary key (1=ANON-0000 placeholder) |
| customer_id | VARCHAR | Business key (e.g., "LC-0000001") |
| first_name | VARCHAR | Customer first name (mixed English/Nigerian) |
| last_name | VARCHAR | Customer last name (mixed English/Nigerian) |
| email_hash | VARCHAR | SHA-256 hash of firstname.lastname@email.com (PII protected) |
| age_group | VARCHAR | <25, 25-34, 35-44, 45-54, 55-64, 65+ |
| gender | VARCHAR | Male, Female, Others |
| post_code_district | VARCHAR | e.g., "Lagos-Isl", "Ikeja", "VI" |
| loyalty_tier | VARCHAR | Standard (60%), Silver (25%), Gold (12%), Platinum (3%) |
| loyalty_join_date | DATE | Date customer joined loyalty program |
| is_active | TINYINT | 1=Active member, 0=Inactive |
| preferred_channel | VARCHAR | InStore (55%), Online (20%), Both (25%) |

**Usage:** Customer segmentation, 80/20 analysis, loyalty analytics; ANON-0000 for anonymous shoppers

---

### **dim_supplier**
**Purpose:** Supplier master with performance targets  
**Grain:** One row per supplier (60 rows)  
**Key:** supplier_key (surrogate), supplier_id (business key)

| Column | Type | Description |
|--------|------|-------------|
| supplier_key | INT | Primary key (surrogate) |
| supplier_id | VARCHAR | Business key (e.g., "SUP-0001") |
| supplier_name | VARCHAR | e.g., "Dangote Industries Ltd" |
| supplier_type | VARCHAR | Manufacturer, Distributor, 3PL, DirectFarm |
| is_strategic | TINYINT | 1=Top 10 strategic supplier, 0=Other |
| country_of_origin | VARCHAR | Nigeria, Ghana, South Africa, etc. |
| country_code | VARCHAR | NG, GH, ZA, etc. |
| trade_region | VARCHAR | ECOWAS, Africa, EU, RoW |
| ethical_audit_status | VARCHAR | Compliant, Pending, Failed |
| last_audit_date | DATE | Latest ethical audit date |
| lead_time_days | INT | Contracted lead time (2-30 days) |
| min_order_qty | INT | Minimum order quantity |
| preferred_incoterm | VARCHAR | EXW, FOB, CIF, DDP |
| supplier_status | VARCHAR | Active, Inactive, Suspended |
| onboard_date | DATE | Date supplier was onboarded |

**Usage:** OTIF analysis, supplier performance, supply chain risk

---

### **dim_promotion**
**Purpose:** Promotion/campaign master  
**Grain:** One row per promotion (108 rows for 36 promos × 3 years)  
**Key:** promotion_key (surrogate), promotion_id (business key)

| Column | Type | Description |
|--------|------|-------------|
| promotion_key | INT | Primary key (1=PROMO-NONE placeholder) |
| promotion_id | VARCHAR | Business key (e.g., "PROMO-0001") |
| promotion_name | VARCHAR | e.g., "2022 New Year Clearance" |
| promotion_type | VARCHAR | Clearance, Seasonal, PriceReduction, Multibuy, LoyaltyPoints |
| discount_mechanic | VARCHAR | PctOff, FixedOff, 3for2, BOGOF |
| discount_value | DECIMAL | 10 (for 10% off), 500 (for ₦500 off), 33 (for 3for2) |
| promotion_start_date | DATE | Campaign start date |
| promotion_end_date | DATE | Campaign end date |
| is_national_promo | TINYINT | 1=National campaign, 0=Regional/pilot |
| funding_source | VARCHAR | Retailer, Supplier, Joint |
| budget_ngn | DECIMAL | Campaign budget in NGN |

**Usage:** Promotional lift analysis, campaign effectiveness, trade spend

---

### **dim_channel**
**Purpose:** Sales channel master  
**Grain:** One row per channel (6 rows)  
**Key:** channel_key (primary key)

| Column | Type | Description |
|--------|------|-------------|
| channel_key | INT | Primary key |
| channel_id | VARCHAR | POS, eComm, Marketplace, B2B, Wholesale, Other |
| channel_name | VARCHAR | Full channel name |
| channel_type | VARCHAR | Retail, Online, Wholesale |

**Usage:** Sales split analysis (In-store vs Online)

---

### **dim_employee**
**Purpose:** Employee master with job roles  
**Grain:** One row per employee (200 rows)  
**Key:** employee_key (surrogate), employee_id (business key)

| Column | Type | Description |
|--------|------|-------------|
| employee_key | INT | Primary key (surrogate) |
| employee_id | VARCHAR | Business key (e.g., "EMP-00001") |
| full_name | VARCHAR | Full name (mixed English/Nigerian) |
| job_title | VARCHAR | Store Manager, Regional Director, Finance Analyst, etc. |
| department | VARCHAR | Store Ops, Finance, Buying, Logistics, IT, HR |
| contract_type | VARCHAR | Full-Time (60%), Part-Time (30%), Casual (10%) |
| store_key | INT | FK to dim_store (NULL if Head Office) |
| region_code | VARCHAR | SW-NG, SS-NG, SE-NG, NC-NG (NULL if HO) |
| email_upn | VARCHAR | e.g., "emp00001@primechoice.com.ng" |
| is_active | TINYINT | 1=Currently employed, 0=Departed |
| hire_date | DATE | Employment start date |
| leave_date | DATE | Exit date (NULL if still employed) |

**Usage:** Staff efficiency, labor cost analysis, store management

---

### **dim_cost_centre**
**Purpose:** Cost centre (budget responsibility) master  
**Grain:** One row per cost centre (25 rows)  
**Key:** cost_centre_key (surrogate), cost_centre_code (business key)

| Column | Type | Description |
|--------|------|-------------|
| cost_centre_key | INT | Primary key (surrogate) |
| cost_centre_code | VARCHAR | e.g., "CC-SW-NG-OPS" |
| cost_centre_name | VARCHAR | e.g., "South West Store Operations" |
| cost_centre_type | VARCHAR | Direct, Corporate |
| owner_employee_key | INT | FK to dim_employee (manager) |
| region_code | VARCHAR | SW-NG, SS-NG, etc. (NULL if corporate) |
| gl_account_group | VARCHAR | Store Direct Costs, Supply Chain, Revenue Costs, Central Overheads |
| is_active | TINYINT | 1=Active, 0=Closed |

**Usage:** P&L reporting by centre, responsibility accounting

---

### **dim_warehouse**
**Purpose:** Warehouse/distribution centre master  
**Grain:** One row per facility (6 rows)  
**Key:** warehouse_key (surrogate), warehouse_id (business key)

| Column | Type | Description |
|--------|------|-------------|
| warehouse_key | INT | Primary key (surrogate) |
| warehouse_id | VARCHAR | e.g., "WH-001" |
| warehouse_name | VARCHAR | e.g., "Lagos NDC (National)" |
| warehouse_type | VARCHAR | NDC, RDC, Fulfilment, Dark Store |
| city | VARCHAR | Lagos, Abuja, Port Harcourt, Enugu |
| country | VARCHAR | Nigeria |
| country_code | VARCHAR | NG |
| capacity_pallets | INT | Pallet capacity |
| is_automated | TINYINT | 1=Automated, 0=Manual |
| is_third_party | TINYINT | 1=3PL operated, 0=PrimeChoice owned |
| operator_name | VARCHAR | PrimeChoice Logistics, GIG, Kobo360, etc. |

**Usage:** Inventory distribution, logistics cost allocation

---

## FACT TABLES

### **fact_sales**
**Purpose:** Point of sale transaction line items  
**Grain:** One row per line item on receipt (~900,000 rows)  
**Key:** transaction_id (business key, non-unique), line_number (uniqueness with transaction_id)  
**Fact Type:** Transactional

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | VARCHAR | Receipt/transaction ID (e.g., "T202201011001234") |
| line_number | INT | Line item number within transaction (1, 2, 3...) |
| transaction_date_key | INT | FK to dim_date |
| transaction_time | TIME | Time of transaction (HH:MM:SS) |
| store_key | INT | FK to dim_store |
| product_key | INT | FK to dim_product |
| customer_key | INT | FK to dim_customer (1=ANON-0000 for anonymous shoppers) |
| channel_key | INT | FK to dim_channel (POS, eComm, etc.) |
| promotion_key | INT | FK to dim_promotion (1=PROMO-NONE if no promotion) |
| employee_key | INT | FK to dim_employee (NULL if not recorded) |
| quantity_sold | DECIMAL | Quantity purchased (units/kg/litres) |
| return_quantity | DECIMAL | Quantity returned on same transaction |
| gross_revenue_ngn | DECIMAL | Revenue before discount (qty × retail_price) |
| discount_ngn | DECIMAL | Discount amount in NGN |
| return_value_ngn | DECIMAL | Refund value if item returned |
| cost_of_goods_sold_ngn | DECIMAL | COGS (qty × cost_price) |
| vat_collected_ngn | DECIMAL | VAT charged (7.5%) |
| loyalty_points_earned | INT | Loyalty points awarded |
| loyalty_points_redeemed | INT | Points redeemed on this transaction |
| is_return | TINYINT | 1=Returned item, 0=Regular sale |
| is_voided | TINYINT | 1=Transaction voided, 0=Valid |
| load_date_key | INT | Date record was loaded |
| source_system | VARCHAR | POS (in-store) or eComm (online) |

**Computed Columns (auto-calculated in DB):**
- net_quantity = quantity_sold - return_quantity
- net_revenue_ngn = gross_revenue_ngn - discount_ngn - return_value_ngn
- gross_profit_ngn = net_revenue_ngn - cost_of_goods_sold_ngn

**Key Metrics:**
- Gross Margin % = gross_profit_ngn / net_revenue_ngn
- Units per Transaction = SUM(quantity_sold) / COUNT(distinct transaction_id)

**Usage:** Revenue analysis, product mix, customer behavior, promotional effectiveness

---

### **fact_inventory**
**Purpose:** End-of-month inventory snapshots  
**Grain:** One row per product per store per month-end (~12,000 rows)  
**Key:** snapshot_date_key + store_key + product_key (composite)  
**Fact Type:** Periodic snapshot

| Column | Type | Description |
|--------|------|-------------|
| snapshot_date_key | INT | FK to dim_date (only EOM dates) |
| store_key | INT | FK to dim_store |
| product_key | INT | FK to dim_product |
| warehouse_key | INT | FK to dim_warehouse (NULL = store-held) |
| opening_stock_units | DECIMAL | Opening inventory |
| closing_stock_units | DECIMAL | Closing inventory (snapshot point) |
| received_units | DECIMAL | Units received during month |
| sold_units | DECIMAL | Units sold |
| wasted_units | DECIMAL | Waste/shrinkage (higher for perishables) |
| shrinkage_units | DECIMAL | Inventory shrinkage % |
| transfer_in_units | DECIMAL | Transfer in from other stores |
| transfer_out_units | DECIMAL | Transfer out to other stores |
| closing_stock_value_ngn | DECIMAL | Closing stock value at cost |
| is_out_of_stock | TINYINT | 1=OOS at snapshot, 0=In stock |
| oos_hours | DECIMAL | Hours out of stock during month |
| days_of_cover_remaining | DECIMAL | Days inventory will last (closing_stock / avg_daily_sales) |
| replenishment_ordered | TINYINT | 1=Replenishment PO raised, 0=No |
| replenishment_qty | DECIMAL | Qty ordered for replenishment |
| load_date_key | INT | Date record loaded |

**Key Metrics:**
- Inventory Turn = sold_units / avg(closing_stock_units)
- Stock Out Rate = COUNT(is_out_of_stock=1) / total_stores
- Days of Cover = Average across stores

**Usage:** Inventory management, stockout analysis, carrying cost

---

### **fact_purchase_orders**
**Purpose:** Purchase order lines from suppliers  
**Grain:** One row per PO line item (~18,000 rows)  
**Key:** po_number + po_line_number (composite)  
**Fact Type:** Transactional

| Column | Type | Description |
|--------|------|-------------|
| po_number | VARCHAR | Purchase order number (e.g., "PO-20220105-00001") |
| po_line_number | INT | Line item within PO |
| order_date_key | INT | FK to dim_date (PO creation date) |
| expected_delivery_date_key | INT | FK to dim_date (contracted delivery) |
| actual_delivery_date_key | INT | FK to dim_date (actual receipt, NULL=in transit) |
| supplier_key | INT | FK to dim_supplier |
| product_key | INT | FK to dim_product |
| warehouse_key | INT | FK to dim_warehouse |
| ordered_qty | DECIMAL | Quantity ordered |
| received_qty | DECIMAL | Quantity actually received |
| accepted_qty | DECIMAL | Quantity accepted (after QC) |
| rejected_qty | DECIMAL | Quantity rejected (damaged, defects) |
| agreed_unit_cost_ngn | DECIMAL | Negotiated cost per unit |
| invoiced_unit_cost_ngn | DECIMAL | Actual invoice unit cost |
| freight_cost_ngn | DECIMAL | Freight/transport cost |
| duty_and_tariff_ngn | DECIMAL | Import duty/tariff (if applicable) |
| is_on_time | TINYINT | 1=Delivered by expected date, 0=Late |
| is_in_full | TINYINT | 1=Received full qty, 0=Short-shipped |
| is_otif | TINYINT | 1=On-Time-In-Full, 0=Missed target |
| delivery_lead_time_days | INT | (actual_date - order_date) days |
| lead_time_variance_days | INT | (actual_date - expected_date) days (negative=early) |
| po_status | VARCHAR | Received, Shipped, Cancelled, In Transit |
| load_date_key | INT | Date record loaded |

**Trigger-Calculated Fields:**
- is_otif = is_on_time AND is_in_full
- delivery_lead_time_days = calculated on INSERT
- lead_time_variance_days = calculated on INSERT

**Key Metrics:**
- OTIF % = COUNT(is_otif=1) / total_pos
- Average Lead Time = AVG(delivery_lead_time_days)
- Supplier Fill Rate % = SUM(received_qty) / SUM(ordered_qty)
- Total Procurement Cost = SUM(received_qty × invoiced_unit_cost + freight + duty)

**Usage:** Supplier OTIF scorecard, supply chain efficiency, cost analysis

---

### **fact_budget_target**
**Purpose:** Monthly budget targets by store and category  
**Grain:** One row per store × category × fiscal month (~9,000 rows)  
**Key:** fiscal_month_date_key + store_key + category_name (composite)  
**Fact Type:** Planning

| Column | Type | Description |
|--------|------|-------------|
| fiscal_month_date_key | INT | FK to dim_date (1st day of fiscal month) |
| fiscal_year | INT | Fiscal year (e.g., 2022) |
| fiscal_month | INT | 1-12 (Feb=1, Jan=12) |
| store_key | INT | FK to dim_store |
| category_name | VARCHAR | Product category |
| department_name | VARCHAR | Department |
| budget_revenue_ngn | DECIMAL | Budgeted revenue |
| budget_gross_profit_ngn | DECIMAL | Budgeted gross profit |
| budget_gross_margin_pct | DECIMAL | Budgeted margin % |
| budget_transaction_count | INT | Expected transactions |
| budget_units_sold | DECIMAL | Expected units sold |
| budget_lfl_growth_pct | DECIMAL | Like-for-like growth assumption |
| budget_version | VARCHAR | Original, Revised, Forecast |
| load_date_key | INT | Load date |

**Usage:** Budget vs actual variance analysis, forecast accuracy, sales planning

---

### **fact_finance_pl**
**Purpose:** Monthly P&L by cost centre  
**Grain:** One row per GL line × cost centre × fiscal month (~5,000 rows)  
**Key:** fiscal_month_date_key + cost_centre_key + gl_account_code (composite)  
**Fact Type:** Planning/Reporting

| Column | Type | Description |
|--------|------|-------------|
| fiscal_month_date_key | INT | FK to dim_date (fiscal month) |
| fiscal_year | INT | Fiscal year |
| fiscal_month | INT | 1-12 |
| cost_centre_key | INT | FK to dim_cost_centre |
| store_key | INT | FK to dim_store (NULL if corporate) |
| gl_account_code | VARCHAR | GL code (e.g., "4000") |
| gl_account_name | VARCHAR | Revenue, COGS, Opex, etc. |
| pl_line | VARCHAR | Revenue, COGS, Gross Profit, Opex, EBITDA |
| pl_section | VARCHAR | above-the-line, below-the-line |
| actual_amount_ngn | DECIMAL | Actual amount |
| budget_amount_ngn | DECIMAL | Budgeted amount |
| prior_year_amount_ngn | DECIMAL | Prior year comparison |
| journal_source | VARCHAR | SAP-ERP, Manual, Adjustment |
| is_adjustment | TINYINT | 1=Manual adjustment entry, 0=System feed |
| load_date_key | INT | Load date |

**Computed Columns (in DB):**
- variance_vs_budget_ngn = actual_amount_ngn - budget_amount_ngn
- variance_vs_py_ngn = actual_amount_ngn - prior_year_amount_ngn

**Usage:** Monthly P&L reporting, variance analysis, profitability tracking

---

### **fact_customer_returns**
**Purpose:** Product returns/refunds  
**Grain:** One row per return line item (~9,000 rows)  
**Key:** return_transaction_id (business key, composite with return reason)  
**Fact Type:** Transactional

| Column | Type | Description |
|--------|------|-------------|
| return_transaction_id | VARCHAR | Return transaction ID |
| original_transaction_id | VARCHAR | FK to original fact_sales transaction |
| return_date_key | INT | FK to dim_date (return date) |
| original_sale_date_key | INT | FK to dim_date (original sale date) |
| store_key | INT | FK to dim_store |
| product_key | INT | FK to dim_product |
| customer_key | INT | FK to dim_customer |
| channel_key | INT | FK to dim_channel |
| return_quantity | DECIMAL | Qty returned |
| refund_amount_ngn | DECIMAL | Refund value |
| restocking_cost_ngn | DECIMAL | Cost to restock item |
| return_reason_code | VARCHAR | RR01-RR07 (faulty, wrong item, etc.) |
| return_reason_desc | VARCHAR | Reason description |
| return_outcome | VARCHAR | Refund, Exchange, StoreCredit |
| load_date_key | INT | Load date |

**Return Rate by Department:**
- Electronics: 4.5%
- Clothing: 3.5%
- Household: 2.0%
- Non-Food: 1.2%
- Health: 1.0%
- Food: 0.4%

**Usage:** Return analysis, quality issues, customer satisfaction, category health

---

## BRIDGE TABLES

### **bridge_product_promotion**
**Purpose:** Many-to-many link between products and promotions  
**Grain:** One row per product × promotion combination  

| Column | Type | Description |
|--------|------|-------------|
| product_key | INT | FK to dim_product |
| promotion_key | INT | FK to dim_promotion |
| weighting_factor | DECIMAL | Importance weight (1.0 = equal) |

**Usage:** Determine which products are eligible for each promotion

---

### **bridge_store_promotion**
**Purpose:** Many-to-many link between stores and promotions  
**Grain:** One row per store × promotion combination  

| Column | Type | Description |
|--------|------|-------------|
| store_key | INT | FK to dim_store |
| promotion_key | INT | FK to dim_promotion |

**Usage:** Determine which stores run which promotions

---

## RLS (ROW-LEVEL SECURITY) TABLE

### **rls_user_region_map**
**Purpose:** Maps Power BI users to regions for row-level security  
**Grain:** One row per user × region assignment  

| Column | Type | Description |
|--------|------|-------------|
| upn | VARCHAR | User Principal Name (e.g., "rd.southwest@primechoice.com.ng") |
| region_code | VARCHAR | SW-NG, SS-NG, SE-NG, NC-NG |
| role_type | VARCHAR | CEO, RegionalDirector, CategoryManager, StoreManager, Finance, SupplyChain |
| assigned_store_key | INT | Specific store (NULL if all stores in region) |
| assigned_category | VARCHAR | Specific category (NULL if all categories) |
| is_active | TINYINT | 1=Active user, 0=Deactivated |

**Usage:** Power BI RLS DAX expressions filter data by region/role

---

## KEY METRICS & FORMULAS

| Metric | Formula | Used For |
|--------|---------|----------|
| **Total Revenue** | SUM(gross_revenue_ngn) | Top-line sales |
| **Gross Profit** | SUM(gross_profit_ngn) | Profitability |
| **Gross Margin %** | Gross Profit / Total Revenue | Efficiency |
| **COGS** | SUM(cost_of_goods_sold_ngn) | Cost tracking |
| **Units Sold** | SUM(quantity_sold) | Volume |
| **Avg Basket Value** | Total Revenue / Transaction Count | Customer spending |
| **Inventory Turnover** | SUM(sold_units) / AVG(closing_stock_units) | Stock efficiency |
| **Days of Cover** | closing_stock_units / avg_daily_sales | Inventory health |
| **OTIF %** | COUNT(is_otif=1) / COUNT(*) | Supplier performance |
| **Return Rate %** | SUM(return_quantity) / SUM(quantity_sold) | Quality |
| **YoY Growth %** | (Current Year - Prior Year) / Prior Year | Trend |

---

## DATA QUALITY NOTES

✅ **Completeness**
- All fact tables have no NULL foreign keys (enforced by DB)
- dim_date covers full 3-year period with no gaps

⚠️ **Nulls (Intentional)**
- employee_key in fact_sales = transaction not linked to employee
- close_date in dim_store = store still open
- actual_delivery_date_key in fact_purchase_orders = PO in transit
- warehouse_key in fact_inventory = store-held stock

✅ **Referential Integrity**
- All foreign keys enforced at database level
- Placeholder records (ANON-0000, PROMO-NONE) included for robustness

✅ **Business Logic**
- Seasonal patterns baked into fact_sales (Dec spike, Jan dip)
- Store format multipliers applied (Hypermarket 4.5×, Convenience 0.5×)
- Regional income variation (Lagos 1.2×, SE 0.95×)
- YoY growth trend (2022 baseline, 2023 +9%, 2024 +18%)

---

## USEFUL QUERIES

**Top 10 Products by Revenue:**
```sql
SELECT p.product_name, SUM(f.gross_revenue_ngn) as revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_key, p.product_name
ORDER BY revenue DESC
LIMIT 10;
```

**Supplier OTIF Scorecard:**
```sql
SELECT s.supplier_name, 
  COUNT(CASE WHEN f.is_otif=1 THEN 1 END)*100.0/COUNT(*) as otif_pct
FROM fact_purchase_orders f
JOIN dim_supplier s ON f.supplier_key = s.supplier_key
GROUP BY s.supplier_key, s.supplier_name
ORDER BY otif_pct DESC;
```

**Regional Revenue Comparison:**
```sql
SELECT d.region_code, DATE_FORMAT(d.full_date,'%Y-%m') as month,
  SUM(f.gross_revenue_ngn) as revenue
FROM fact_sales f
JOIN dim_store d ON f.store_key = d.store_key
JOIN dim_date dd ON f.transaction_date_key = dd.date_key
GROUP BY d.region_code, DATE_FORMAT(d.full_date,'%Y-%m')
ORDER BY month DESC, revenue DESC;
```

---

**Data Dictionary Version:** 1.0  
**Last Updated:** 2024-12-31  
**Contact:** BI Team

