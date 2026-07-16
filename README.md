# PrimeChoice Retail Group — Enterprise BI Dashboard

## 📊 Project Overview

A comprehensive 5-page Power BI dashboard for a Nigerian omnichannel retailer. The dataset is based on real retail transaction data that has been adapted and adjusted using AI to create a realistic analytical scenario while protecting proprietary information.



**Built for:** Portfolio demonstration | Data analytics role showcase

---

## 🎯 Key Features

### Dashboard Pages (5 Total)

| Page | Purpose | Key Metrics |
|------|---------|-------------|
| **Executive Scorecard** | Leadership overview | Revenue, Gross Profit, Margin %, OTIF |
| **Sales & Product Performance** | Category analysis | Product margins, ABC classification, trends |
| **Store Operations & Inventory** | Store management | Days of cover, shrinkage, out-of-stock alerts |
| **Supply Chain & Logistics** | Supplier performance | OTIF %, lead times, procurement costs |
| **Finance & P&L Bridge** | Financial analysis | Budget variance, YoY growth, profitability margins |

### Technical Capabilities

✅ **Data Integration:** MySQL database with 16 tables (9 dimensions, 6 facts)  
✅ **Advanced Analytics:** 50+ DAX measures including time intelligence & YoY growth  
✅ **Row-Level Security:** 6 user roles (CEO, Regional Directors, Store Managers, Finance, Supply Chain, Category Managers)  
✅ **Interactive Filtering:** Region, store, product category, supplier, date slicers  
✅ **Realistic Data:** 3 years (2022-2024) adapted from real retail patterns with AI adjustments

---

## 📁 Dataset

**Source:** Real Nigerian retail transaction data, adapted and anonymized using AI  
**Period:** January 2022 - December 2024  
**Volume:** 3.5M transaction records + supporting dimensions

### Data Adaptation Process

The dataset originates from actual retail operations but has been:
- **Anonymized:** Company names, customer identities, and sensitive details replaced
- **Adjusted with AI:** Data patterns and relationships preserved while values/names modified
- **Enriched:** Additional calculated fields and dimensions added for analytical completeness
- **Validated:** Ensured business logic and referential integrity throughout
  
### Key Tables

- **Fact Tables:** Sales, Inventory, Purchase Orders, Budget, Finance, Returns (6 tables)
- **Dimension Tables:** Date, Store, Product, Customer, Supplier, Employee, Promotion, Channel, Warehouse, Cost Centre (10 tables)
- **Features:** Seasonal patterns, regional income variation, promotional lift effects, supplier OTIF variance

---

## 🛠️ Tech Stack

- **BI Tool:** Power BI Desktop
- **Database:** MySQL
- **Languages:** DAX (measures), M (data transformations), SQL (schema)
- **Analytics:** Time intelligence, statistical measures, predictive indicators
- **Data Processing:** AI-assisted data transformation and adaptation

---

## 📈 Key Metrics & Insights

### Executive KPIs
- ### Executive KPIs
- **Total Revenue:** ₦29.42bn (3-year period)
- **Gross Profit:** ₦8.01bn
- **Gross Margin:** 27.23% (profitability efficiency)
- **EBITDA %:** 22.4% (operational earnings as % of revenue)

### Operational Insights
- **Inventory Turnover:** 1.07x annually (slow-moving stock)
- **Days of Cover:** 10 days (tight inventory levels)
- **Shrinkage Rate:** 0.94% (excellent control)
- **Product Mix:** 228 active SKUs with 520 total in catalog

### Supply Chain
- **Avg Lead Time:** 6.05 days
- **Fill Rate:** 93.67%
- **Top Supplier:** Flour Mills (highest OTIF)

---

## 📚 Documentation

- [**DASHBOARD_OVERVIEW.md**](./DASHBOARD_OVERVIEW.md) — Detailed guide to each dashboard page
- [**DATA_DICTIONARY.md**](./DATA_DICTIONARY.md) — Complete data model documentation
- [**DAX_Measures.md**](./documentation/DAX_Measures.md) — All 50+ measures explained
- [**RLS_Setup.md**](./documentation/RLS_Setup.md) — Row-level security configuration

---

## 🎨 Dashboard Screenshots

### Page 1: Executive Scorecard
![Executive Scorecard](./dashboard/screenshots/01exec.png)

### Page 2: Sales & Product Performance
![Sales Products](./dashboard/screenshots/02sales&products.png)

### Page 3: Store Operations & Inventory
![Store Ops](./dashboard/screenshots/03stores&inventory.png)

### Page 4: Supply Chain & Logistics
![Supply Chain](./dashboard/screenshots/04supply.png)

### Page 5: Finance & P&L Bridge
![Finance](./dashboard/screenshots/05finance.png)

---

## 🚀 How to Use

### View the Dashboard

1. Download `PCL.BI.Dash.pbix` from `## (https://github.com/cultek15/Primechoice-Group-BI-Dashboard/releases/download/v1.0.0/PCL.BI.Dash.pbix)
2. Open in **Power BI Desktop**
3. Connect to your MySQL database (or use sample data if provided)
4. Interact with all slicers and charts

### Explore the Data

1. Review `primechoice_star_schema.sql` for database structure
2. Use `generate_data.py` to populate sample data
3. Check `DATA_DICTIONARY.md` for field descriptions

### Understand the Analytics

1. Read `DAX_Measures.md` for how each metric is calculated
2. Review `RLS_Setup.md` to understand security model
3. See `DASHBOARD_OVERVIEW.md` for business context

---

## 💡 Key Design Decisions

### Star Schema Architecture
- **Fact tables:** Designed for transaction-level analysis
- **Dimensions:** Conformed dimensions across facts for consistency
- **Bridges:** Product-Promotion and Store-Promotion many-to-many relationships

### Data Adaptation Approach
- **Real-world patterns:** Preserved actual business seasonality and trends
- **AI adjustments:** Used AI to adapt sensitive details while maintaining analytical integrity
- **Quality assurance:** Validated all relationships and business logic post-adaptation

### RLS Implementation
- **Dynamic filtering:** User-region mappings in lookup table
- **Role-based access:** 6 distinct user personas with appropriate data visibility
- **Scalable:** Easy to add new users or regions without dashboard changes

---

## 📊 Metrics Showcase

### Most Complex Measures

1. **YoY Growth %** — Compares current period to same period prior year
2. **OTIF (On-Time-In-Full)** — Combines on-time AND in-full delivery metrics
3. **ABC Classification** — Dynamic product ranking by cumulative revenue (80/20 rule)
4. **Cumulative Supplier Spend %** — Pareto analysis for concentration risk
5. **Days of Cover** — Remaining inventory duration based on sales velocity

---

## 🎓 Skills Demonstrated

✅ **BI & Analytics:** Dashboard design, KPI selection, drill-through analysis  
✅ **Data Modeling:** Star schema, slowly changing dimensions, many-to-many relationships  
✅ **DAX Programming:** 50+ measures, time intelligence, calculated columns, RLS expressions  
✅ **Database Design:** Normalized schema, constraints, views, triggers  
✅ **Data Engineering:** Synthetic data generation, quality validation, ETL logic  
✅ **Business Acumen:** Retail metrics, supply chain KPIs, financial P&L structure

---

## 📝 Project Stats

- **Dashboard Pages:** 5
- **Total Visuals:** 35+
- **DAX Measures:** 50+
- **Database Tables:** 16
- **Fact Records:** ~3.5M transactions
- **RLS Roles:** 6
- **Data Period:** 3 years (2022-2024)
- **Build Time:** 170+ hours

---

## 🔗 Links

- **Data Dictionary:** [See complete field documentation](./DATA_DICTIONARY.md)
- **Dashboard Guide:** [Detailed page-by-page walkthrough](./DASHBOARD_OVERVIEW.md)
- **Database Schema:** [SQL DDL and structure](./database/primechoice_star_schema.sql)

---

## 📧 Contact & Feedback

Built as a portfolio project to demonstrate enterprise BI capabilities using adapted real-world retail data.

**Skills showcased:** Power BI, DAX, SQL, Data Modeling, Analytics, Business Intelligence, AI-assisted Data Transformation


---

## 📄 License

This project uses adapted real retail data for educational/portfolio purposes. Original data has been anonymized and adjusted using AI technology to protect proprietary information.

---

**Last Updated:** June 2026  
**Version:** 1.0
