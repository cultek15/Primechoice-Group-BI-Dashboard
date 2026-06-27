# Row-Level Security (RLS) Configuration Guide

Complete documentation of how row-level security (RLS) is implemented in the PrimeChoice dashboard.

---

## Overview

Row-Level Security ensures each user sees only the data relevant to their role. This document explains:
- How RLS roles are configured
- Which users have which access
- How data is filtered by role
- How to add new users or roles

---

## RLS Architecture

### Key Components

1. **rls_user_region_map Table**
   - Links users (by email/upn) to authorized regions
   - Maps users to specific store or category assignments

2. **DAX Role Definitions**
   - 6 roles with RLS filters on specific dimensions
   - Filters apply based on USERNAME() function

3. **Dimension Filtering**
   - dim_store: filtered by region_code
   - dim_product: filtered by category
   - dim_supplier: filtered by supplier_type
   - dim_cost_centre: filtered by cost_centre assignment

---

## The 6 RLS Roles

### Role 1: CEO

**Who:** Chief Executive Officer / Group Managing Director

**Access Level:** UNRESTRICTED (sees all data)

**DAX Filters:** None applied

**Dashboard Visibility:** All 5 pages, all regions, all stores, all products

**User Examples:**
- ceo@primechoice.com.ng

**Business Logic:** 
- CEO needs complete visibility for strategic decisions
- Can drill from executive overview to transaction detail
- Can compare regions and stores

**Typical Usage:**
- Board reporting
- Strategic planning
- Performance reviews

---

### Role 2: Regional Director - Southwest

**Who:** Regional Director for South West region (Lagos, Ibadan, Abeokuta)

**Access Level:** REGION-SPECIFIC

**DAX Filters Applied:**
```dax
[region_code] = "SW-NG"
```

**Data Visible:**
- ✅ All stores in SW-NG region (e.g., Lagos Hypermarket, Ibadan Store)
- ✅ All products sold in region
- ✅ All suppliers serving region
- ❌ Data from SS-NG, SE-NG, NC-NG regions hidden

**Dashboard Pages:**
- ✅ Executive Scorecard (shows only SW revenue, margin, etc.)
- ✅ Sales & Product (shows SW product mix)
- ✅ Store Operations (shows only SW stores)
- ✅ Supply Chain (shows suppliers to SW region)
- ✅ Finance (shows SW P&L)

**User Examples:**
- rd.southwest@primechoice.com.ng
- rd_southwest@primechoice.com.ng

**Business Logic:**
- Regional director is accountable for their region's performance
- Can see competitor regions only for benchmarking (if CEO grants)
- Focused P&L responsibility for SW region

**Typical Usage:**
- Monitor SW store performance
- Manage SW inventory
- Track SW supplier performance
- Report to CEO on regional KPIs

---

### Role 3: Regional Director - South South

**Access Level:** REGION-SPECIFIC

**DAX Filters Applied:**
```dax
[region_code] = "SS-NG"
```

**Geography:** Port Harcourt, Warri, Benin City

**Data Visible:** All SS-NG region data only

**User Examples:**
- rd.southsouth@primechoice.com.ng

---

### Role 4: Regional Director - South East

**Access Level:** REGION-SPECIFIC

**DAX Filters Applied:**
```dax
[region_code] = "SE-NG"
```

**Geography:** Enugu, Owerri, Onitsha

**Data Visible:** All SE-NG region data only

**User Examples:**
- rd.southeast@primechoice.com.ng

---

### Role 5: Regional Director - North Central

**Access Level:** REGION-SPECIFIC

**DAX Filters Applied:**
```dax
[region_code] = "NC-NG"
```

**Geography:** Abuja, Kaduna, Ilorin

**Data Visible:** All NC-NG region data only

**User Examples:**
- rd.northcentral@primechoice.com.ng

---

### Role 6: Store Manager

**Who:** Individual store manager

**Access Level:** STORE-SPECIFIC

**DAX Filters Applied:**
```dax
[store_key] = LOOKUPVALUE(dim_employee[store_key], dim_employee[email_upn], USERNAME())
```

**Data Visible:**
- ✅ Only their assigned store
- ✅ Products sold at that store
- ✅ Inventory levels at that store
- ❌ Other stores hidden
- ❌ Other regions hidden

**Dashboard Pages Relevant:**
- ✅ Store Operations (their store only)
- ⚠️ Sales & Products (filtered to store)
- ⚠️ Executive Scorecard (their store performance only)

**User Examples:**
- storemanager1@primechoice.com.ng (Lagos store)
- storemanager2@primechoice.com.ng (Port Harcourt store)

**Business Logic:**
- Store manager is accountable for their store's performance
- Can manage store-level inventory
- Can see operational metrics for their store
- Cannot compare across stores

**Typical Usage:**
- Daily store performance monitoring
- Inventory management
- Stock-out alerts
- Local supplier interactions

---

### Role 7: Finance Analyst

**Who:** Finance team member

**Access Level:** UNRESTRICTED (all regions, all financial data)

**DAX Filters:** None on cost centre (sees all)

**Data Visible:** 
- ✅ All P&L data across all cost centres
- ✅ Budget variance at all levels
- ✅ Financial details by region/store
- ❌ Customer personal data (PII) not visible
- ❌ Supplier payment terms (confidential) not visible

**Dashboard Pages:**
- ✅ Finance & P&L Bridge (full access)
- ✅ Executive Scorecard (financial KPIs)
- ⚠️ Other pages available for context but focused on Finance

**User Examples:**
- finance@primechoice.com.ng
- analyst.finance@primechoice.com.ng

**Business Logic:**
- Finance needs cross-functional visibility
- Must see all regions/stores for consolidated reporting
- Group-level P&L responsibility

**Typical Usage:**
- Month-end close reporting
- Budget variance analysis
- Cost centre performance review
- Board financial reporting

---

### Role 8: Supply Chain Lead

**Who:** Head of supply chain / procurement

**Access Level:** SUPPLIER-SPECIFIC + UNRESTRICTED

**DAX Filters Applied:**
```dax
-- No filter on suppliers (can see all)
-- Can see all regions served by suppliers
```

**Data Visible:**
- ✅ All suppliers
- ✅ OTIF performance across all suppliers
- ✅ Lead time data for all suppliers
- ✅ Procurement costs
- ✅ Which regions each supplier serves
- ❌ Supplier payment terms (Finance only)
- ❌ Pricing negotiation details (confidential)

**Dashboard Pages:**
- ✅ Supply Chain & Logistics (full access)
- ✅ Executive Scorecard (OTIF % visible)
- ⚠️ Store Operations (inventory context)

**User Examples:**
- supplychain@primechoice.com.ng
- scm.lead@primechoice.com.ng

**Business Logic:**
- Supply chain needs system-wide visibility
- Accountable for supplier performance across all regions
- Strategic sourcing and supplier management

**Typical Usage:**
- Supplier scorecard management
- Lead time monitoring
- OTIF improvement initiatives
- Supplier negotiations

---

### Role 9: Category Manager

**Who:** Product category manager (e.g., Food category)

**Access Level:** CATEGORY-SPECIFIC

**DAX Filters Applied:**
```dax
[category_name] IN 
CALCULATE(
    VALUES(rls_user_region_map[assigned_category]),
    rls_user_region_map[upn] = USERNAME()
)
```

**Data Visible:**
- ✅ Only assigned category products
- ✅ Margin/performance of category products
- ✅ Category sales across all stores/regions
- ❌ Other categories hidden
- ❌ Full product catalog hidden

**Dashboard Pages:**
- ✅ Sales & Product Performance (category focus)
- ✅ Executive Scorecard (category contribution)
- ✅ Store Operations (category-specific inventory)

**User Examples:**
- catmgr.food@primechoice.com.ng (Food category)
- catmgr.electronics@primechoice.com.ng (Electronics category)

**Business Logic:**
- Category manager owns P&L for their category
- Accountable for margins, promotions, pricing
- Need to see performance across all regions/stores for their category

**Typical Usage:**
- Category performance analysis
- Promotional planning for category
- Pricing recommendations
- Vendor management

---

## rls_user_region_map Lookup Table

This table is the backbone of RLS. It links users to their authorized data access.

### Table Structure
upn | region_code | assigned_store_key | assigned_category | role_type | is_active

### Example Rows
ceo@primechoice.com.ng | NULL | NULL | NULL | CEO | 1

rd.southwest@primechoice.com.ng | SW-NG | NULL | NULL | RegionalDirector | 1
rd.southsouth@primechoice.com.ng | SS-NG | NULL | NULL | RegionalDirector | 1
rd.southeast@primechoice.com.ng | SE-NG | NULL | NULL | RegionalDirector | 1
rd.northcentral@primechoice.com.ng | NC-NG | NULL | NULL | RegionalDirector | 1

storemanager1@primechoice.com.ng | SW-NG | 1 | NULL | StoreManager | 1
storemanager2@primechoice.com.ng | SS-NG | 5 | NULL | StoreManager | 1

finance@primechoice.com.ng | NULL | NULL | NULL | Finance | 1

supplychain@primechoice.com.ng | NULL | NULL | NULL | SupplyChain | 1

catmgr.food@primechoice.com.ng | NULL | NULL | Food | CategoryManager | 1
catmgr.electronics@primechoice.com.ng | NULL | NULL | Electronics | CategoryManager | 1

### Columns Explained

- **upn:** User Principal Name (email address) - must match USERNAME() in Power BI
- **region_code:** SW-NG, SS-NG, SE-NG, NC-NG (NULL = all regions)
- **assigned_store_key:** Specific store ID (NULL = all stores)
- **assigned_category:** Product category (NULL = all categories)
- **role_type:** CEO, RegionalDirector, StoreManager, Finance, SupplyChain, CategoryManager
- **is_active:** 1 = active, 0 = deactivated (prevents login)

---

## How RLS Works in Power BI

### Step 1: User Logs In

User opens Power BI dashboard and signs in:

Username: rd.southwest@primechoice.com.ng

Password: ••••••••

Power BI captures USERNAME() = "rd.southwest@primechoice.com.ng"

### Step 2: Role is Evaluated

Power BI Service looks up which role applies based on USERNAME()

From rls_user_region_map:
- UPN = "rd.southwest@primechoice.com.ng"
- role_type = "RegionalDirector"
- region_code = "SW-NG"

### Step 3: DAX Filters Are Applied

The Regional Director role has this filter:
```dax
[region_code] = "SW-NG"
```

### Step 4: All Visuals Are Filtered

Every chart, table, card shows only SW-NG data:

- Executive Scorecard → Shows only SW revenue, SW stores
- Sales & Products → Shows only products sold in SW
- Store Ops → Shows only SW stores
- Supply Chain → Shows only suppliers serving SW
- Finance → Shows only SW cost centres

### Step 5: User Sees Filtered Dashboard

Regional Director sees complete dashboard BUT filtered to their region only.

They cannot:
- Click slicer to select other regions
- Drill-through to other regions
- Export data from other regions

---

## Adding New Users to RLS

### Scenario: Hire New Regional Director for South West

**Step 1: Add User to Azure AD**
- Your IT team adds: new.director@primechoice.com.ng
- Assign Power BI Pro license

**Step 2: Add Row to rls_user_region_map**

Insert into rls_user_region_map:
```sql
INSERT INTO rls_user_region_map 
VALUES ('new.director@primechoice.com.ng', 'SW-NG', NULL, NULL, 'RegionalDirector', 1);
```

**Step 3: Add User to Power BI Role in Service**

In Power BI Service Admin portal:
- Go to your workspace
- Dataset → Manage Roles
- Select "Regional Director - Southwest" role
- Add email: new.director@primechoice.com.ng

**Step 4: Test Access**

New user signs into Power BI:
- Sees only SW-NG data ✅
- Cannot access other regions ✅
- All dashboards work with filtered data ✅

---

## Scenario: Deactivate a User

**Reason:** Store manager transferred to different store

**Action 1: Update rls_user_region_map**
```sql
UPDATE rls_user_region_map 
SET is_active = 0, assigned_store_key = 2
WHERE upn = 'storemanager1@primechoice.com.ng';
```

**Action 2: Re-publish Dashboard**
- User can still log in but sees blank dashboards (no data matches new filter)

---

## Troubleshooting RLS

### Problem: User sees all data (RLS not working)

**Checks:**
1. Is user assigned to a role in Power BI Service?
   - Go to: Workspace → Dataset → Manage Roles
   - Check user email is in role assignment
2. Does user email in Azure AD match rls_user_region_map?
   - Case-sensitive: john@test.com ≠ John@test.com
   - Check for spaces or typos
3. Is is_active = 1 in lookup table?

**Fix:**
```sql
SELECT * FROM rls_user_region_map WHERE upn = 'user.email@company.com';
-- Verify exists and is_active = 1
```

### Problem: User sees no data

**Checks:**
1. Is region_code correctly spelled? (SW-NG not SW)
2. Does dim_store actually have SW-NG region?
3. Is there any data for that region in fact tables?

**Fix:**
```sql
SELECT DISTINCT region_code FROM dim_store;
-- Verify your filter value matches exactly
```

### Problem: User can see region A even though assigned region B

**Cause:** RLS filter not correctly applied to all visuals

**Fix:**
1. Re-publish dashboard
2. Verify DAX filters on all visuals include dimension filter
3. Check for measures that don't respect RLS context

---

## RLS Best Practices

### 1. Naming Convention
[role_type] [specific_filter]

Examples:
- "Regional Director - Southwest"
- "Store Manager"
- "Category Manager - Electronics"

### 2. Test Every Role
- Log in as each user type
- Verify correct data is visible
- Verify other data is hidden

### 3. Keep Lookup Table Accurate
- Update rls_user_region_map whenever user transfers
- Deactivate (don't delete) when user leaves
- Monthly audit of active users

### 4. Document Mappings
- Keep spreadsheet of user → role → region assignments
- Update when roles change
- Use for audit trails

### 5. Test Before Publishing
- Test RLS in Power BI Desktop using "View as Role"
- Select each role and verify filtering works
- Then publish to Service

---

## RLS Limitations

⚠️ **Limitations to be aware of:**

1. **RLS applies only in Power BI Service**
   - Does NOT restrict database access
   - Users with SQL credentials can still access MySQL directly
   - Use database-level permissions for additional security

2. **Row-level (not column-level)**
   - Can hide rows (e.g., "don't show other regions")
   - Cannot hide columns (e.g., "don't show salary column")
   - For sensitive columns, exclude from data import

3. **No RLS in Power BI Desktop**
   - Desktop shows all data
   - Use "View as Role" feature to test only
   - Real RLS enforcement happens in Service

4. **Performance impact**
   - Complex RLS filters can slow queries
   - Test performance after implementing RLS

---

## Implementation Checklist

- [ ] Create rls_user_region_map lookup table with all users
- [ ] Define 6+ roles in Power BI Desktop
- [ ] Apply DAX filters to each role (dim_store, dim_product, etc.)
- [ ] Test each role using "View as Role" in Desktop
- [ ] Publish dashboard to Power BI Service
- [ ] Create role assignments in Service
- [ ] Assign users to roles in Service
- [ ] Test access as each user type
- [ ] Document all roles and assignments
- [ ] Set up monthly audit process

---

## Reference: DAX Filter Syntax

### Region Filter (Regional Directors)
```dax
[region_code] = "SW-NG"
```

### Store Filter (Store Managers)
```dax
[store_key] = LOOKUPVALUE(dim_employee[store_key], dim_employee[email_upn], USERNAME())
```

### Category Filter (Category Managers)
```dax
[category_name] IN 
CALCULATE(VALUES(rls_user_region_map[assigned_category]), 
rls_user_region_map[upn] = USERNAME())
```

### Multiple Suppliers (Supply Chain)
```dax
-- No filter applied (sees all suppliers)
```

---

## Critical Supply Chain Context

**Important Note for Supply Chain Lead Role:**

The current dashboard reveals critical OTIF issues:
- Network OTIF: 21% (target: 90%)
- All top 5 suppliers: 63-67% OTIF (all below target)

The Supply Chain Lead role has unrestricted access to identify and address these systemic issues across all suppliers and regions. This is the highest priority operational challenge for the organization.

---

**Last Updated:** June 2026  
**RLS Version:** 1.0 (Final)  
**Roles Configured:** 6+ (CEO, 4× Regional Directors, Store Manager, Finance, Supply Chain, Category Manager)  
**Total Users Supported:** Unlimited (scalable via rls_user_region_map)
