# =============================================================================
# PrimeChoice Retail Group — Synthetic Data Generator  v4
# =============================================================================
# PRE-REQUISITE: run primechoice_ddl_v3.sql in MySQL BEFORE this script.
#
# FIXES IN v4
#   - np.random.lognormal used instead of random.lognormal (AttributeError fix)
#   - SET FOREIGN_KEY_CHECKS=0/1 wraps every DELETE so re-runs never fail
#   - fact_purchase_orders: exp_d AND act_d both clamped to 2024-12-31 so
#     expected_delivery_date_key never references a date outside dim_date
#   - All other date-key references audited — only dates from date_keys list used
#
# HOW TO RUN
#   1. Edit DB_CONFIG (user / password) below.
#   2. Ensure primechoice_ddl_v3.sql has already been executed in MySQL.
#   3. pip install faker mysql-connector-python numpy
#   4. python generate_primechoice_data_v4.py
#   Estimated runtime: 5-12 minutes.
# =============================================================================

import random
import hashlib
import math
import warnings
from datetime import date, timedelta, datetime

import numpy as np
import mysql.connector
from faker import Faker

warnings.filterwarnings('ignore')
fake = Faker('en_GB')
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# =============================================================================
# !! EDIT YOUR MYSQL CREDENTIALS HERE !!
# =============================================================================
DB_CONFIG = {
    'host':       'localhost',
    'port':       3306,
    'user':       'root',           # your MySQL username
    'password':   '**********',  # your MySQL password
    'database':   'primechoice',
    'charset':    'utf8mb4',
    'autocommit': False,
}
# =============================================================================

DATE_MAX = date(2024, 12, 31)   # last date in dim_date — never reference beyond this


# ---------------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------------

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


def bulk_insert(cur, table, rows, batch=500):
    if not rows:
        return 0
    cols = list(rows[0].keys())
    sql  = (f"INSERT INTO `{table}` ({','.join(f'`{c}`' for c in cols)}) "
            f"VALUES ({','.join(['%s'] * len(cols))})")
    for i in range(0, len(rows), batch):
        cur.executemany(sql, [tuple(r[c] for c in cols) for r in rows[i:i+batch]])
    return len(rows)


def fk_delete(cur, table):
    """Delete all rows disabling FK checks so parent tables can be cleared safely."""
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute(f"DELETE FROM `{table}`")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")


def dk(d: date) -> int:
    """Convert date → YYYYMMDD integer key."""
    return int(d.strftime('%Y%m%d'))


def clamp_date(d: date) -> date:
    """Clamp a date to DATE_MAX so it always maps to a valid dim_date row."""
    return min(d, DATE_MAX)


def ngn(v) -> float:
    return round(float(v), 2)


def date_range(start: str, end: str):
    cur_d = date.fromisoformat(start)
    end_d = date.fromisoformat(end)
    while cur_d <= end_d:
        yield cur_d
        cur_d += timedelta(days=1)


# ---------------------------------------------------------------------------
# REFERENCE DATA
# ---------------------------------------------------------------------------

REGIONS = [
    {'code': 'SW-NG', 'name': 'South West',    'div': 'Nigeria West',  'income_mult': 1.20,
     'cities': ['Lagos', 'Ibadan', 'Abeokuta']},
    {'code': 'SS-NG', 'name': 'South South',   'div': 'Nigeria South', 'income_mult': 1.05,
     'cities': ['Port Harcourt', 'Warri', 'Benin City']},
    {'code': 'SE-NG', 'name': 'South East',    'div': 'Nigeria South', 'income_mult': 0.95,
     'cities': ['Enugu', 'Owerri', 'Onitsha']},
    {'code': 'NC-NG', 'name': 'North Central', 'div': 'Nigeria North', 'income_mult': 1.00,
     'cities': ['Abuja', 'Kaduna', 'Ilorin']},
]

# (sales_mult, margin_adj, stores_per_region[SW, SS, SE, NC])
FORMATS = {
    'Hypermarket': (4.5,  0.02, [3, 1, 1, 2]),
    'Supermarket': (2.2,  0.00, [5, 3, 2, 4]),
    'Express':     (1.0, -0.01, [4, 3, 2, 3]),
    'Convenience': (0.5, -0.02, [2, 1, 1, 1]),
    'Outlet':      (0.8,  0.03, [1, 1, 0, 0]),
}

# dept → {category: (avg_retail_ngn, avg_margin_pct, is_perishable)}
DEPT_CATS = {
    'Food': {
        'Fresh Produce':          (850,   0.38, True),
        'Bakery':                 (1200,  0.42, True),
        'Dairy & Eggs':           (1500,  0.30, True),
        'Meat & Fish':            (3500,  0.28, True),
        'Frozen Foods':           (2200,  0.32, False),
        'Beverages':              (1800,  0.35, False),
        'Snacks & Confectionery': (900,   0.40, False),
        'Dry Goods & Grains':     (1200,  0.25, False),
    },
    'Non-Food': {
        'Cleaning & Laundry': (2200, 0.32, False),
        'Personal Care':      (2800, 0.38, False),
        'Baby & Toddler':     (3500, 0.35, False),
        'Pet Care':           (2100, 0.30, False),
        'Stationery':         (800,  0.40, False),
    },
    'Household': {
        'Kitchen & Dining': (5500, 0.42, False),
        'Home Storage':     (3200, 0.44, False),
        'Lighting':         (4500, 0.38, False),
        'Bedding & Towels': (6500, 0.40, False),
    },
    'Electronics': {
        'Phones & Accessories': (35000, 0.18, False),
        'Small Appliances':     (22000, 0.22, False),
        'Audio & TV':           (55000, 0.16, False),
    },
    'Clothing': {
        'Mens Clothing':      (8500,  0.50, False),
        'Womens Clothing':    (9200,  0.52, False),
        'Childrens Clothing': (5500,  0.48, False),
        'Footwear':           (12000, 0.46, False),
    },
    'Health': {
        'Pharmacy OTC':           (2500, 0.35, False),
        'Vitamins & Supplements': (3200, 0.45, False),
        'First Aid':              (1800, 0.40, False),
    },
}

RETURN_RATES = {
    'Electronics': 0.045, 'Clothing': 0.035, 'Household': 0.020,
    'Non-Food': 0.012,    'Health': 0.010,   'Food': 0.004,
}

SEASONAL    = [0.72, 0.85, 0.95, 1.05, 0.92, 0.88, 0.90, 0.95, 0.98, 1.05, 1.15, 1.45]
DOW_WEIGHTS = [0.85, 0.88, 0.90, 0.92, 1.10, 1.35, 0.65]
YOY         = {2022: 1.00, 2023: 1.09, 2024: 1.18}

BRANDS = [
    'PrimeChoice', 'PrimeChoice', 'PrimeChoice',
    'Dangote', 'Unilever', 'Nestle', 'P&G', 'Chi Limited',
    'Dufil', 'Cadbury Nigeria', 'Coca-Cola', 'Pepsi',
    'Indomie', 'Peak Milk', 'Golden Penny', 'Honeywell',
    'Saro', 'Reckitt', 'Johnson and Johnson', 'Samsung', 'Tecno',
]

# (name, type, is_strategic, lead_days, otif_target)
SUPPLIER_DATA = [
    ('Dangote Industries Ltd',       'Manufacturer', True,  3,  0.96),
    ('Unilever Nigeria Plc',         'Manufacturer', True,  5,  0.95),
    ('Nestle Nigeria Plc',           'Manufacturer', True,  4,  0.94),
    ('Chi Limited',                  'Manufacturer', True,  3,  0.97),
    ('Dufil Prima Foods',            'Manufacturer', True,  4,  0.95),
    ('Flour Mills of Nigeria',       'Manufacturer', True,  5,  0.93),
    ('Honeywell Flour Mills',        'Manufacturer', True,  4,  0.94),
    ('Cadbury Nigeria',              'Manufacturer', True,  6,  0.92),
    ('Coca-Cola HBC Nigeria',        'Manufacturer', True,  3,  0.97),
    ('PZ Cussons Nigeria',           'Manufacturer', True,  5,  0.93),
    ('Seven-Up Bottling Co',         'Manufacturer', False, 4,  0.90),
    ('Nigerian Breweries',           'Manufacturer', False, 5,  0.88),
    ('Golden Penny Foods',           'Distributor',  False, 7,  0.85),
    ('Promasidor Nigeria',           'Distributor',  False, 6,  0.87),
    ('UAC Foods',                    'Distributor',  False, 5,  0.89),
    ('Friesland Campina Wamco',      'Manufacturer', False, 8,  0.86),
    ('Beloxxi Industries',           'Manufacturer', False, 6,  0.88),
    ('De-United Foods',              'Manufacturer', False, 5,  0.90),
    ('TGI Group',                    'Distributor',  False, 7,  0.84),
    ('Multipro Enterprise',          'Distributor',  False, 8,  0.82),
    ('Grand Cereals Ltd',            'Manufacturer', False, 9,  0.83),
    ('Tropical General Investments', 'Distributor',  False, 7,  0.85),
    ('Saro Agrosciences',            'Manufacturer', False, 10, 0.80),
    ('Reckitt Benckiser Nigeria',    'Manufacturer', False, 6,  0.88),
    ('GIG Logistics',                '3PL',          False, 2,  0.92),
    ('Kobo360 Logistics',            '3PL',          False, 3,  0.88),
    ('DHL Supply Chain Nigeria',     '3PL',          False, 2,  0.94),
    ('Jumia Express Fulfilment',     '3PL',          False, 2,  0.91),
    ('Olam Nigeria',                 'DirectFarm',   False, 5,  0.86),
    ('Lagos Fresh Farms',            'DirectFarm',   False, 2,  0.90),
    ('Ibadan Agro Co-op',            'DirectFarm',   False, 3,  0.85),
    ('Abuja Fresh Harvest',          'DirectFarm',   False, 4,  0.83),
    ('East Farms Nigeria',           'DirectFarm',   False, 5,  0.82),
    ('BUA Group',                    'Manufacturer', False, 6,  0.87),
    ('Coscharis Group',              'Distributor',  False, 8,  0.80),
    ('Eleganza Industries',          'Manufacturer', False, 9,  0.78),
    ('Tropical Springwater',         'Manufacturer', False, 4,  0.88),
    ('La Casera Company',            'Manufacturer', False, 5,  0.86),
    ('Tolaram Group',                'Manufacturer', False, 6,  0.85),
    ('Citiserve Ltd',                'Distributor',  False, 7,  0.82),
    ('EkoCorps Distribution',        'Distributor',  False, 5,  0.84),
    ('West Africa Trade Co',         'Distributor',  False, 10, 0.78),
    ('Pan African Supplies',         'Distributor',  False, 12, 0.75),
    ('Afrimart Wholesale',           'Distributor',  False, 8,  0.80),
    ('NovaCentury Nigeria',          'Distributor',  False, 9,  0.79),
    ('DirectSource Africa',          'Distributor',  False, 11, 0.76),
    ('Farmcrowdy Supplies',          'DirectFarm',   False, 3,  0.88),
    ('Agrorite Nigeria',             'DirectFarm',   False, 4,  0.85),
    ('Southern Cross Imports',       'Distributor',  False, 15, 0.72),
    ('Stallion Group',               'Distributor',  False, 10, 0.78),
    ('Jubaili Bros',                 'Distributor',  False, 8,  0.80),
    ('Mikano International',         'Distributor',  False, 9,  0.77),
    ('Ecobank Supply Chain',         '3PL',          False, 3,  0.87),
    ('Transnational Corp',           'Distributor',  False, 7,  0.82),
    ('Reiz Continental Supplies',    'Distributor',  False, 6,  0.84),
    ('Vitafoam Nigeria',             'Manufacturer', False, 7,  0.85),
    ('Coleman Cables',               'Manufacturer', False, 8,  0.82),
    ('Seplat Agro',                  'DirectFarm',   False, 5,  0.83),
    ('Veritasi Homes Supply',        'Distributor',  False, 6,  0.81),
    ('Konga Logistics',              '3PL',          False, 2,  0.89),
]

PROMO_CALENDAR = [
    # (name, type, mechanic, disc_value, start_month, start_day, duration_days, is_national)
    ('New Year Clearance',    'Clearance',      'PctOff',   25,  1,  2,  14, True),
    ('Valentine Special',     'Seasonal',       'PctOff',   15,  2,  7,  10, True),
    ('Ramadan Savings',       'PriceReduction', 'PctOff',   10,  3, 10,  30, True),
    ('Easter Weekend',        'Multibuy',       '3for2',    33,  4,  1,   5, True),
    ('Workers Day Promo',     'PriceReduction', 'FixedOff', 500, 5,  1,   7, True),
    ('Mid-Year Clearance',    'Clearance',      'PctOff',   20,  7,  1,  14, True),
    ('Back to School',        'Seasonal',       'Multibuy', 15,  8, 15,  21, True),
    ('Independence Day Sale', 'Seasonal',       'PctOff',   12,  9, 28,   5, True),
    ('October Mega Sale',     'PriceReduction', 'PctOff',   18, 10,  1,  14, True),
    ('Black Friday',          'PriceReduction', 'PctOff',   30, 11, 24,   4, True),
    ('Cyber Monday',          'PriceReduction', 'PctOff',   25, 11, 27,   2, True),
    ('Christmas Countdown',   'Seasonal',       '3for2',    33, 12,  1,  24, True),
    ('Christmas Day Special', 'Seasonal',       'PctOff',   40, 12, 24,   3, True),
    ('Loyalty Gold Bonus',    'LoyaltyPoints',  'PctOff',    5,  1, 15,  30, False),
    ('Own Label Push',        'PriceReduction', 'PctOff',   10,  3,  1,  21, False),
    ('Fresh Produce Week',    'Multibuy',       'BOGOF',    50,  5, 15,   7, False),
    ('Electronics Expo',      'PriceReduction', 'PctOff',   15,  6,  1,  14, False),
    ('Clothing Clearance',    'Clearance',      'PctOff',   35,  6, 20,  10, False),
]

RETURN_REASONS = [
    ('RR01', 'Faulty or Defective',  0.28),
    ('RR02', 'Wrong Item Delivered', 0.18),
    ('RR03', 'Changed Mind',         0.20),
    ('RR04', 'Not As Described',     0.12),
    ('RR05', 'Damaged Packaging',    0.10),
    ('RR06', 'Expired Product',      0.07),
    ('RR07', 'Other',                0.05),
]


# ===========================================================================
# STEP 1 — dim_date
# ===========================================================================
def gen_dim_date():
    print("\n[1/16] dim_date ...")
    nigerian_holidays = {
        date(2022,  1,  1): "New Year's Day",   date(2022,  4, 15): "Good Friday",
        date(2022,  4, 18): "Easter Monday",    date(2022,  5,  1): "Workers Day",
        date(2022,  6, 12): "Democracy Day",    date(2022, 10,  1): "Independence Day",
        date(2022, 12, 25): "Christmas Day",    date(2022, 12, 26): "Boxing Day",
        date(2023,  1,  1): "New Year's Day",   date(2023,  4,  7): "Good Friday",
        date(2023,  4, 10): "Easter Monday",    date(2023,  5,  1): "Workers Day",
        date(2023,  6, 12): "Democracy Day",    date(2023, 10,  1): "Independence Day",
        date(2023, 12, 25): "Christmas Day",    date(2023, 12, 26): "Boxing Day",
        date(2024,  1,  1): "New Year's Day",   date(2024,  3, 29): "Good Friday",
        date(2024,  4,  1): "Easter Monday",    date(2024,  5,  1): "Workers Day",
        date(2024,  6, 12): "Democracy Day",    date(2024, 10,  1): "Independence Day",
        date(2024, 12, 25): "Christmas Day",    date(2024, 12, 26): "Boxing Day",
    }
    rows = []
    for d in date_range('2022-01-01', '2024-12-31'):
        dow   = d.isoweekday()
        iso   = d.isocalendar()
        wk_st = d - timedelta(days=d.weekday())
        q     = math.ceil(d.month / 3)
        eom   = (d.replace(day=28) + timedelta(4)).replace(day=1) - timedelta(1)
        qem   = {1:3,2:3,3:3,4:6,5:6,6:6,7:9,8:9,9:9,10:12,11:12,12:12}[d.month]
        q_end = (date(d.year, qem, 28) + timedelta(4)).replace(day=1) - timedelta(1)
        fy    = d.year if d.month >= 2 else d.year - 1
        fm    = d.month - 1 if d.month >= 2 else d.month + 11
        fq    = math.ceil(fm / 3)
        fw    = min(((d - date(fy, 2, 1)).days // 7) + 1, 52)
        rows.append({
            'date_key':               dk(d),
            'full_date':              d.isoformat(),
            'day_of_week':            dow,
            'day_name':               d.strftime('%A'),
            'day_of_month':           d.day,
            'day_of_year':            d.timetuple().tm_yday,
            'week_of_year':           iso[1],
            'iso_week':               iso[1],
            'week_start_date':        wk_st.isoformat(),
            'month_number':           d.month,
            'month_name':             d.strftime('%B'),
            'month_short':            d.strftime('%b'),
            'quarter':                q,
            'quarter_name':           f'Q{q}',
            'calendar_year':          d.year,
            'fiscal_week':            fw,
            'fiscal_month':           fm,
            'fiscal_quarter':         fq,
            'fiscal_year':            fy,
            'fiscal_year_label':      f'FY{str(fy)[2:]}/{str(fy+1)[2:]}',
            'is_weekend':             1 if dow >= 6 else 0,
            'is_public_holiday':      1 if d in nigerian_holidays else 0,
            'holiday_name':           nigerian_holidays.get(d),
            'is_trading_day':         0 if dow == 7 else 1,
            'is_last_day_of_month':   1 if d == eom else 0,
            'is_last_day_of_quarter': 1 if d == q_end else 0,
            'month_year_label':       d.strftime('%b-%Y'),
            'quarter_year_label':     f'Q{q}-{d.year}',
        })
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_date')
    n = bulk_insert(cur, 'dim_date', rows)
    conn.commit(); cur.close(); conn.close()
    print(f"  ✓ {n:,} rows")
    return [r['date_key'] for r in rows]


# ===========================================================================
# STEP 2 — dim_store
# ===========================================================================
def gen_dim_stores():
    print("\n[2/16] dim_store ...")
    rows = []
    snum = 1
    for region in REGIONS:
        for fmt, (mult, madj, counts) in FORMATS.items():
            r_idx = REGIONS.index(region)
            for i in range(counts[r_idx]):
                city   = region['cities'][i % len(region['cities'])]
                lo_sqm = {'Hypermarket': 3000, 'Supermarket': 800, 'Express': 300}.get(fmt, 150)
                hi_sqm = {'Hypermarket': 6000, 'Supermarket': 2500, 'Express': 700}.get(fmt, 350)
                sfm    = round(random.uniform(lo_sqm, hi_sqm), 0)
                open_d = date(2019, 1, 1) + timedelta(days=random.randint(0, 500))
                rows.append({
                    'store_id':           f"{region['code'][:2]}-{city[:3].upper()}-{snum:03d}",
                    'store_name':         f"PrimeChoice {city} {fmt} {i+1}",
                    'store_format':       fmt,
                    'store_status':       'Active',
                    'open_date':          open_d.isoformat(),
                    'close_date':         None,
                    'sales_floor_sqm':    sfm,
                    'num_checkouts':      max(2, int(sfm / 250)),
                    'has_car_park':       1 if fmt in ['Hypermarket','Supermarket','Outlet'] else 0,
                    'has_cafe':           1 if fmt == 'Hypermarket' else 0,
                    'has_pharmacy':       1 if fmt in ['Hypermarket','Supermarket'] else 0,
                    'address_line1':      fake.street_address(),
                    'city':               city,
                    'state_province':     city,
                    'post_code':          None,
                    'country':            'Nigeria',
                    'country_code':       'NG',
                    'latitude':           round(random.uniform(4.5, 13.5), 6),
                    'longitude':          round(random.uniform(3.0, 15.0), 6),
                    'cluster_name':       f"{city} Metro",
                    'region_name':        region['name'],
                    'region_code':        region['code'],
                    'division_name':      region['div'],
                    'row_effective_date': '2022-01-01',
                    'row_expiry_date':    '9999-12-31',
                    'is_current':         1,
                })
                snum += 1
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_store')
    n = bulk_insert(cur, 'dim_store', rows)
    conn.commit()
    cur.execute("SELECT store_key, region_code, store_format FROM dim_store")
    stores = cur.fetchall()
    cur.close(); conn.close()
    print(f"  ✓ {n} stores")
    return stores


# ===========================================================================
# STEP 3 — dim_product
# ===========================================================================
def gen_dim_products():
    print("\n[3/16] dim_product ...")
    rows   = []
    n_skus = {'Food':12, 'Non-Food':8, 'Household':6, 'Electronics':6, 'Clothing':8, 'Health':6}
    for dept, cats in DEPT_CATS.items():
        for cat, (avg_retail, avg_margin, is_perish) in cats.items():
            for _ in range(n_skus.get(dept, 6)):
                brand  = random.choice(BRANDS)
                is_own = 1 if brand == 'PrimeChoice' else 0
                margin = round(avg_margin + (0.05 if is_own else 0) + random.uniform(-0.04, 0.04), 4)
                retail = round(avg_retail * random.uniform(0.7, 1.4), 2)
                cost   = round(retail * (1 - margin), 2)
                rows.append({
                    'product_id':         f"SKU-{len(rows)+1:06d}",
                    'product_name':       f"{brand} {cat} {fake.word().capitalize()}",
                    'product_name_short': f"{brand[:10]} {cat[:15]}",
                    'brand_name':         brand,
                    'is_own_label':       is_own,
                    'sub_category_name':  cat,
                    'category_name':      cat,
                    'department_name':    dept,
                    'division_name':      dept,
                    'unit_of_measure':    random.choice(['Each','Kg','Litre','Pack']),
                    'pack_size':          round(random.uniform(0.1, 5.0), 3),
                    'is_perishable':      1 if is_perish else 0,
                    'is_age_restricted':  1 if cat == 'Pharmacy OTC' else 0,
                    'min_age_required':   18 if cat == 'Pharmacy OTC' else None,
                    'is_online_only':     1 if random.random() < 0.03 else 0,
                    'is_store_only':      1 if cat in ['Fresh Produce','Bakery'] else 0,
                    'retail_price_ngn':   retail,
                    'cost_price_ngn':     cost,
                    'target_margin_pct':  round(margin * 100, 2),
                    'vat_rate_pct':       7.50,
                    'product_status':     'Live',
                    'launch_date':        date(2019, 1, 1).isoformat(),
                    'discontinued_date':  None,
                    'row_effective_date': '2022-01-01',
                    'row_expiry_date':    '9999-12-31',
                    'is_current':         1,
                })
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_product')
    n = bulk_insert(cur, 'dim_product', rows)
    conn.commit()
    cur.execute("SELECT product_key, category_name, department_name, "
                "retail_price_ngn, cost_price_ngn, is_perishable FROM dim_product")
    products = cur.fetchall()
    cur.close(); conn.close()
    print(f"  ✓ {n} products")
    return products


# ===========================================================================
# STEP 4 — dim_customer
# ===========================================================================
def gen_dim_customers():
    print("\n[4/16] dim_customer ...")
    tiers     = ['Standard','Silver','Gold','Platinum']
    tw        = [60, 25, 12, 3]
    tier_mult = {'Standard':1.0, 'Silver':1.8, 'Gold':2.8, 'Platinum':4.5}
    rows = []
    for i in range(5000):
        tier = random.choices(tiers, weights=tw)[0]
        rows.append({
            'customer_id':        f"LC-{i+1:07d}",
            'first_name':         fake.first_name(),
            'last_name':          fake.last_name(),
            'email_hash':         hashlib.sha256(fake.email().encode()).hexdigest(),
            'age_group':          random.choice(['<25','25-34','35-44','45-54','55-64','65+']),
            'gender':             random.choices(['Male','Female','Others'], weights=[48,48,4])[0],
            'post_code_district': random.choice(['Lagos-Isl','Ikeja','VI','Lekki','Surulere',
                                                  'Yaba','Ikorodu','Abuja-Ctrl','GRA-PH',
                                                  'Enugu-East','Ibadan-Nth']),
            'loyalty_tier':       tier,
            'loyalty_join_date':  (date(2019,1,1)+timedelta(days=random.randint(0,1460))).isoformat(),
            'is_active':          1,
            'preferred_channel':  random.choices(['InStore','Online','Both'], weights=[55,20,25])[0],
        })
    conn = get_conn(); cur = conn.cursor()
    # Only delete real customers — keep ANON-0000 (key=1)
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute("DELETE FROM dim_customer WHERE customer_id != 'ANON-0000'")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    n = bulk_insert(cur, 'dim_customer', rows)
    conn.commit()
    cur.execute("SELECT customer_key, loyalty_tier FROM dim_customer")
    customers = cur.fetchall()
    cur.close(); conn.close()
    print(f"  ✓ {n} customers")
    return customers, tier_mult


# ===========================================================================
# STEP 5 — dim_supplier
# ===========================================================================
def gen_dim_suppliers():
    print("\n[5/16] dim_supplier ...")
    rows = []
    for i, (name, stype, strategic, lead, otif) in enumerate(SUPPLIER_DATA):
        rows.append({
            'supplier_id':          f"SUP-{i+1:04d}",
            'supplier_name':        name,
            'supplier_type':        stype,
            'is_strategic':         1 if strategic else 0,
            'country_of_origin':    random.choice(['Nigeria','Nigeria','Nigeria',
                                                    'Ghana','South Africa','Netherlands','China']),
            'country_code':         random.choice(['NG','NG','NG','GH','ZA','NL','CN']),
            'trade_region':         ('ECOWAS' if stype in ['DirectFarm','3PL']
                                     else random.choice(['ECOWAS','Africa','EU','RoW'])),
            'ethical_audit_status': random.choices(['Compliant','Pending','Failed'],
                                                    weights=[75, 20, 5])[0],
            'last_audit_date':      (date(2023,1,1)+timedelta(days=random.randint(0,365))).isoformat(),
            'lead_time_days':       lead,
            'min_order_qty':        random.randint(50, 500),
            'preferred_incoterm':   random.choice(['EXW','FOB','CIF','DDP']),
            'supplier_status':      'Active',
            'onboard_date':         date(2018, 1, 1).isoformat(),
        })
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_supplier')
    n = bulk_insert(cur, 'dim_supplier', rows)
    conn.commit()
    cur.execute("SELECT supplier_key, lead_time_days FROM dim_supplier ORDER BY supplier_key")
    raw       = cur.fetchall()
    suppliers = [(raw[i][0], raw[i][1], SUPPLIER_DATA[i][4]) for i in range(len(raw))]
    cur.close(); conn.close()
    print(f"  ✓ {n} suppliers")
    return suppliers


# ===========================================================================
# STEP 6 — dim_promotion
# ===========================================================================
def gen_dim_promotions():
    print("\n[6/16] dim_promotion ...")
    rows = []
    pid  = 1
    for year in [2022, 2023, 2024]:
        for name, ptype, mech, disc, sm, sd, dur, national in PROMO_CALENDAR:
            try:
                start = date(year, sm, sd)
            except ValueError:
                start = date(year, sm, 28)
            end = start + timedelta(days=dur)
            rows.append({
                'promotion_id':         f"PROMO-{pid:04d}",
                'promotion_name':       f"{year} {name}",
                'promotion_type':       ptype,
                'discount_mechanic':    mech,
                'discount_value':       float(disc),
                'promotion_start_date': start.isoformat(),
                'promotion_end_date':   end.isoformat(),
                'is_national_promo':    1 if national else 0,
                'funding_source':       random.choice(['Retailer','Supplier','Joint']),
                'budget_ngn':           ngn(random.uniform(2_000_000, 25_000_000)),
            })
            pid += 1
    conn = get_conn(); cur = conn.cursor()
    # Keep PROMO-NONE (key=1)
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute("DELETE FROM dim_promotion WHERE promotion_id != 'PROMO-NONE'")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    n = bulk_insert(cur, 'dim_promotion', rows)
    conn.commit()
    cur.execute("SELECT promotion_key, discount_mechanic, discount_value, "
                "promotion_start_date, promotion_end_date FROM dim_promotion")
    promos = cur.fetchall()
    cur.close(); conn.close()
    print(f"  ✓ {n} promotions")
    return promos


# ===========================================================================
# STEP 7 — dim_warehouse
# ===========================================================================
def gen_dim_warehouses():
    print("\n[7/16] dim_warehouse ...")
    whs = [
        ('WH-001', 'Lagos NDC',              'NDC',        'Lagos',         5000, 1, 0, 'PrimeChoice Logistics'),
        ('WH-002', 'Abuja RDC',              'RDC',        'Abuja',         2500, 0, 0, 'PrimeChoice Logistics'),
        ('WH-003', 'Port Harcourt RDC',      'RDC',        'Port Harcourt', 2000, 0, 0, 'PrimeChoice Logistics'),
        ('WH-004', 'Enugu RDC',              'RDC',        'Enugu',         1500, 0, 0, 'PrimeChoice Logistics'),
        ('WH-005', 'Lagos eComm Fulfilment', 'Fulfilment', 'Lagos',         1200, 1, 1, 'GIG Logistics'),
        ('WH-006', 'Lagos North Dark Store', 'Dark Store', 'Lagos',          400, 0, 1, 'Kobo360 Logistics'),
    ]
    rows = [{
        'warehouse_id':    w[0], 'warehouse_name': w[1], 'warehouse_type': w[2],
        'city':            w[3], 'country': 'Nigeria',   'country_code': 'NG',
        'capacity_pallets':w[4], 'is_automated': w[5],   'is_third_party': w[6],
        'operator_name':   w[7],
    } for w in whs]
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_warehouse')
    bulk_insert(cur, 'dim_warehouse', rows)
    conn.commit()
    cur.execute("SELECT warehouse_key FROM dim_warehouse")
    keys = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    print(f"  ✓ {len(keys)} warehouses")
    return keys


# ===========================================================================
# STEP 8 — dim_employee
# ===========================================================================
def gen_dim_employees(stores):
    print("\n[8/16] dim_employee ...")
    titles = [
        'Store Manager','Deputy Manager','Department Manager','Team Leader',
        'Customer Assistant','Checkout Operator','Stock Controller',
        'Warehouse Operative','Finance Analyst','Category Manager',
        'Supply Chain Coordinator','Regional Director','HR Business Partner',
    ]
    rows = []
    for i in range(200):
        store = random.choice(stores)
        is_ho = random.random() < 0.10
        rows.append({
            'employee_id':   f"EMP-{i+1:05d}",
            'full_name':     fake.name(),
            'job_title':     random.choice(titles),
            'department':    random.choice(['Store Ops','Finance','Buying','Logistics','IT','HR']),
            'contract_type': random.choices(['Full-Time','Part-Time','Casual'], weights=[60,30,10])[0],
            'store_key':     None if is_ho else store[0],
            'region_code':   None if is_ho else store[1],
            'email_upn':     f"emp{i+1:05d}@primechoice.com.ng",
            'is_active':     1,
            'hire_date':     (date(2018,1,1)+timedelta(days=random.randint(0,1460))).isoformat(),
            'leave_date':    None,
        })
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_employee')
    bulk_insert(cur, 'dim_employee', rows)
    conn.commit()
    cur.execute("SELECT employee_key FROM dim_employee")
    keys = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    print(f"  ✓ {len(keys)} employees")
    return keys


# ===========================================================================
# STEP 9 — dim_cost_centre
# ===========================================================================
def gen_dim_cost_centres(emp_keys):
    print("\n[9/16] dim_cost_centre ...")
    rows = []
    for region in REGIONS:
        for ctype, gl in [('Store Operations', 'Store Direct Costs'),
                          ('Logistics',        'Supply Chain'),
                          ('Sales & Mktg',     'Revenue Costs')]:
            rows.append({
                'cost_centre_code':   f"CC-{region['code']}-{ctype[:3].upper()}",
                'cost_centre_name':   f"{region['name']} {ctype}",
                'cost_centre_type':   'Direct',
                'owner_employee_key': random.choice(emp_keys),
                'region_code':        region['code'],
                'gl_account_group':   gl,
                'is_active':          1,
            })
    for dept in ['Finance','IT','HR','Marketing','Property','Group CEO']:
        rows.append({
            'cost_centre_code':   f"CC-HO-{dept[:4].upper()}",
            'cost_centre_name':   f"Head Office {dept}",
            'cost_centre_type':   'Corporate',
            'owner_employee_key': random.choice(emp_keys),
            'region_code':        None,
            'gl_account_group':   'Central Overheads',
            'is_active':          1,
        })
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'dim_cost_centre')
    bulk_insert(cur, 'dim_cost_centre', rows)
    conn.commit()
    cur.execute("SELECT cost_centre_key FROM dim_cost_centre")
    keys = [r[0] for r in cur.fetchall()]
    cur.close(); conn.close()
    print(f"  ✓ {len(keys)} cost centres")
    return keys


# ===========================================================================
# STEP 10 — Bridge tables
# ===========================================================================
def gen_bridges(products, promos):
    print("\n[10/16] Bridge tables ...")
    prod_keys  = [p[0] for p in products]
    dept_prods = {}
    for p in products:
        dept_prods.setdefault(p[2], []).append(p[0])

    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'bridge_product_promotion')
    fk_delete(cur, 'bridge_store_promotion')
    cur.execute("SELECT store_key FROM dim_store")
    all_stores = [r[0] for r in cur.fetchall()]

    bpp, bsp = [], []
    seen_pp  = set()
    seen_sp  = set()

    for promo_key, mech, disc, start, end in promos:
        if promo_key == 1:          # skip PROMO-NONE placeholder
            continue
        pool        = (prod_keys if random.random() > 0.4
                       else random.choice(list(dept_prods.values())))
        sample_size = min(random.randint(15, 120), len(pool))
        for pk in random.sample(pool, sample_size):
            if (pk, promo_key) not in seen_pp:
                bpp.append({'product_key': pk, 'promotion_key': promo_key,
                            'weighting_factor': 1.0})
                seen_pp.add((pk, promo_key))
        store_pool = (all_stores if random.random() > 0.3
                      else random.sample(all_stores, max(5, len(all_stores) // 2)))
        for sk in store_pool:
            if (sk, promo_key) not in seen_sp:
                bsp.append({'store_key': sk, 'promotion_key': promo_key})
                seen_sp.add((sk, promo_key))

    n1 = bulk_insert(cur, 'bridge_product_promotion', bpp)
    n2 = bulk_insert(cur, 'bridge_store_promotion',   bsp)
    conn.commit(); cur.close(); conn.close()
    print(f"  ✓ {n1:,} product-promo links | {n2:,} store-promo links")


# ===========================================================================
# STEP 11 — fact_sales
# ===========================================================================
def gen_fact_sales(stores, products, customers, tier_mult, promos, date_keys, emp_keys):
    print("\n[11/16] fact_sales  (longest step — ~5-10 min) ...")

    region_income = {r['code']: r['income_mult'] for r in REGIONS}

    # Build promo date index  date_key → [(promo_key, disc_pct)]
    promo_days: dict = {}
    for promo_key, mech, disc, start, end in promos:
        if promo_key == 1:
            continue
        disc_pct = float(disc) / 100
        s = date.fromisoformat(str(start)[:10]) if not isinstance(start, date) else start
        e = date.fromisoformat(str(end)[:10])   if not isinstance(end,   date) else end
        cur_d = s
        while cur_d <= e:
            promo_days.setdefault(dk(cur_d), []).append((promo_key, disc_pct))
            cur_d += timedelta(days=1)

    # Customer pools by tier
    tier_pools: dict = {'Standard':[],'Silver':[],'Gold':[],'Platinum':[]}
    for ckey, ctier in customers:
        if ctier in tier_pools:
            tier_pools[ctier].append(ckey)

    # channel_key integers 1-6 match the DDL seed rows exactly
    channel_keys    = [1, 2, 3, 4, 5, 6]
    channel_weights = [60, 14, 10, 8, 4, 4]

    dept_prods: dict = {}
    for p in products:
        dept_prods.setdefault(p[2], []).append(p)
    dept_list    = list(dept_prods.keys())
    dept_weights = [8, 5, 3, 1, 3, 2][:len(dept_list)]

    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'fact_sales')
    conn.commit()

    rows = []; total = 0

    for date_key in date_keys:
        d   = date(int(str(date_key)[:4]),
                   int(str(date_key)[4:6]),
                   int(str(date_key)[6:8]))
        dow = d.isoweekday()
        if dow == 7:            # stores closed Sundays
            continue

        seasonal_m = SEASONAL[d.month - 1]
        dow_m      = DOW_WEIGHTS[dow - 1]
        yoy_m      = YOY[d.year]
        promo_m    = 1.30 if date_key in promo_days else 1.0
        if d.month == 12 and d.day in [23, 24]:
            promo_m = max(promo_m, 1.80)

        day_promos = promo_days.get(date_key, [])

        for store_key, region_code, store_fmt in stores:
            fmt_mult = FORMATS[store_fmt][0]
            reg_mult = region_income.get(region_code, 1.0)
            base     = 6 * seasonal_m * dow_m * yoy_m * promo_m * fmt_mult * reg_mult
            n_txns   = max(1, int(base + random.gauss(0, base * 0.15)))

            for _ in range(n_txns):
                txn_id  = f"T{date_key}{store_key:03d}{random.randint(1000,9999)}"
                chan_key = random.choices(channel_keys, weights=channel_weights)[0]

                r = random.random()
                if r < 0.55:
                    cust_key = 1
                elif r < 0.60 and tier_pools['Platinum']:
                    cust_key = random.choice(tier_pools['Platinum'])
                elif r < 0.72 and tier_pools['Gold']:
                    cust_key = random.choice(tier_pools['Gold'])
                elif r < 0.85 and tier_pools['Silver']:
                    cust_key = random.choice(tier_pools['Silver'])
                elif tier_pools['Standard']:
                    cust_key = random.choice(tier_pools['Standard'])
                else:
                    cust_key = 1

                # FIX: use np.random.lognormal — Python's random module has no lognormal
                n_lines       = max(1, min(12, int(np.random.lognormal(1.2, 0.6))))
                txn_promo_key = 1
                txn_disc_pct  = 0.0
                if day_promos and random.random() < 0.30:
                    txn_promo_key, txn_disc_pct = random.choice(day_promos)

                lead_dept = random.choices(dept_list, weights=dept_weights)[0]

                for line in range(1, n_lines + 1):
                    prod = (random.choice(dept_prods[lead_dept])
                            if random.random() < 0.70 else random.choice(products))
                    p_key, p_cat, p_dept, base_retail, base_cost, is_perish = prod

                    inflation = 1.0 + (d.year - 2022) * 0.065 + (d.month - 1) * 0.005
                    retail    = round(float(base_retail) * inflation, 2)
                    cost      = round(float(base_cost)   * inflation, 2)
                    qty       = round(random.uniform(1, 4), 2)
                    gross_rev = round(retail * qty, 4)
                    cogs      = round(cost   * qty, 4)

                    disc = (round(gross_rev * min(txn_disc_pct, 0.40), 4)
                            if txn_promo_key != 1 and random.random() < 0.70 else 0.0)

                    vat     = round((gross_rev - disc) * 0.075, 4)
                    is_ret  = 1 if random.random() < RETURN_RATES.get(p_dept, 0.008) else 0
                    ret_qty = qty if is_ret else 0.0
                    ret_val = round(gross_rev, 4) if is_ret else 0.0
                    pts     = (random.randint(0, 20) if cust_key == 1
                               else random.randint(5, 80))

                    # Do NOT insert generated columns:
                    # net_quantity, net_revenue_ngn, gross_profit_ngn
                    rows.append({
                        'transaction_id':          txn_id,
                        'line_number':             line,
                        'transaction_date_key':    date_key,
                        'transaction_time':        f"{random.randint(8,21):02d}:{random.randint(0,59):02d}:00",
                        'store_key':               store_key,
                        'product_key':             p_key,
                        'customer_key':            cust_key,
                        'channel_key':             chan_key,
                        'promotion_key':           txn_promo_key,
                        'employee_key':            (random.choice(emp_keys)
                                                    if random.random() > 0.4 else None),
                        'quantity_sold':           qty,
                        'return_quantity':         ret_qty,
                        'gross_revenue_ngn':       gross_rev,
                        'discount_ngn':            disc,
                        'return_value_ngn':        ret_val,
                        'cost_of_goods_sold_ngn':  cogs,
                        'vat_collected_ngn':       vat,
                        'loyalty_points_earned':   pts,
                        'loyalty_points_redeemed': random.randint(0, 5),
                        'is_return':               is_ret,
                        'is_voided':               1 if random.random() < 0.002 else 0,
                        'load_date_key':           date_key,
                        'source_system':           'POS' if chan_key == 1 else 'eComm',
                    })

                    if len(rows) >= 2000:
                        bulk_insert(cur, 'fact_sales', rows)
                        conn.commit()
                        total += len(rows)
                        rows   = []

    if rows:
        bulk_insert(cur, 'fact_sales', rows)
        conn.commit()
        total += len(rows)

    cur.close(); conn.close()
    print(f"  ✓ {total:,} sales lines")


# ===========================================================================
# STEP 12 — fact_inventory
# ===========================================================================
def gen_fact_inventory(stores, products, warehouse_keys, date_keys):
    print("\n[12/16] fact_inventory ...")
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT date_key FROM dim_date WHERE is_last_day_of_month = 1")
    eom_keys = [r[0] for r in cur.fetchall()]
    fk_delete(cur, 'fact_inventory')
    conn.commit()

    prod_sample = random.sample(products, min(120, len(products)))
    rows = []; total = 0

    for eom_dk in eom_keys:
        year = int(str(eom_dk)[:4])
        for store_key, region_code, store_fmt in stores:
            fmt_v = FORMATS[store_fmt][0]
            for prod in prod_sample:
                p_key, p_cat, p_dept, base_retail, base_cost, is_perish = prod
                max_close = 30 if is_perish else 200
                closing   = round(random.uniform(0, max_close), 2)
                avg_daily = round(fmt_v * random.uniform(2, 15), 2)
                doc       = round(closing / max(avg_daily, 0.1), 1)
                inflation = 1.0 + (year - 2022) * 0.065
                shrink    = 0.04 if is_perish else 0.008
                rows.append({
                    'snapshot_date_key':       eom_dk,
                    'store_key':               store_key,
                    'product_key':             p_key,
                    'warehouse_key':           None,   # NULL = store-held stock
                    'opening_stock_units':     round(closing + avg_daily * random.uniform(20, 35), 2),
                    'closing_stock_units':     closing,
                    'received_units':          round(avg_daily * random.uniform(25, 35), 2),
                    'sold_units':              round(avg_daily * 30, 2),
                    'wasted_units':            round(avg_daily * 30 * (0.06 if is_perish else 0.005), 2),
                    'shrinkage_units':         round(closing * shrink, 2),
                    'transfer_in_units':       round(random.uniform(0, 10), 2),
                    'transfer_out_units':      round(random.uniform(0, 5),  2),
                    'closing_stock_value_ngn': ngn(closing * float(base_cost) * inflation),
                    'is_out_of_stock':         1 if closing < 1 else 0,
                    'oos_hours':               round(random.uniform(2, 12), 1) if closing < 1 else 0.0,
                    'days_of_cover_remaining': doc,
                    'replenishment_ordered':   1 if doc < 7 else 0,
                    'replenishment_qty':       round(avg_daily * 14, 2) if doc < 7 else None,
                    'load_date_key':           eom_dk,
                })
                if len(rows) >= 1000:
                    bulk_insert(cur, 'fact_inventory', rows); conn.commit()
                    total += len(rows); rows = []

    if rows:
        bulk_insert(cur, 'fact_inventory', rows); conn.commit(); total += len(rows)
    cur.close(); conn.close()
    print(f"  ✓ {total:,} inventory snapshots")


# ===========================================================================
# STEP 13 — fact_purchase_orders
# FIX: exp_d clamped to DATE_MAX so expected_delivery_date_key always exists
#      in dim_date.  act_d also clamped.  Orders whose clamped exp_d == order_d
#      are skipped to avoid zero-day lead times inserting bad FK values.
# ===========================================================================
def gen_fact_purchase_orders(products, suppliers, warehouse_keys, date_keys):
    print("\n[13/16] fact_purchase_orders ...")
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'fact_purchase_orders')
    conn.commit()
    rows = []; total = 0; po_num = 1

    # Only use Mondays that are early enough for even the longest lead time
    # (15 days) to still land on or before DATE_MAX after clamping.
    monday_keys = [
        k for k in date_keys
        if date(int(str(k)[:4]), int(str(k)[4:6]), int(str(k)[6:8])).isoweekday() == 1
    ]

    for order_dk in monday_keys:
        order_d = date(int(str(order_dk)[:4]),
                       int(str(order_dk)[4:6]),
                       int(str(order_dk)[6:8]))

        for _ in range(random.randint(4, 12)):
            sup_key, contracted_lead, otif_target = random.choice(suppliers)
            wh_key = random.choice(warehouse_keys)

            # Clamp expected delivery date so the FK always resolves in dim_date
            exp_d = clamp_date(order_d + timedelta(days=contracted_lead))

            # If clamping made exp_d == order_d, shift it back one day to keep
            # lead time positive; if still equal (order on DATE_MAX) skip.
            if exp_d <= order_d:
                continue

            dec_pen = 0.15 if order_d.month == 12 else 0
            if random.random() > (otif_target - dec_pen):
                raw_act    = exp_d + timedelta(days=random.randint(1, 7))
                is_on_time = 0
            else:
                raw_act    = exp_d + timedelta(days=random.randint(-1, 0))
                is_on_time = 1

            # Clamp actual delivery date too
            act_d = clamp_date(raw_act)
            if act_d < order_d:         # edge case: clamp pushed before order
                act_d = None

            act_dk   = dk(act_d) if act_d else None
            act_lead = (act_d - order_d).days if act_d else None
            lead_var = (act_d - exp_d).days   if act_d else None

            for line in range(1, random.randint(1, 8) + 1):
                prod = random.choice(products)
                p_key, p_cat, p_dept, base_retail, base_cost, is_perish = prod
                inflation   = 1.0 + (order_d.year - 2022) * 0.065
                agreed_cost = round(float(base_cost) * inflation, 4)
                ord_qty     = round(random.uniform(100, 800), 2)
                fill_rate   = (random.uniform(0.97, 1.0) if otif_target > 0.92
                               else random.uniform(0.85, 1.0))
                rec_qty  = round(ord_qty * fill_rate, 2) if act_d else 0.0
                is_full  = 1 if rec_qty >= ord_qty * 0.98 else 0
                is_otif  = 1 if (is_on_time and is_full) else 0

                rows.append({
                    'po_number':                  f"PO-{order_dk}-{po_num:05d}",
                    'po_line_number':             line,
                    'order_date_key':             order_dk,
                    'expected_delivery_date_key': dk(exp_d),   # always within dim_date
                    'actual_delivery_date_key':   act_dk,      # NULL or within dim_date
                    'supplier_key':               sup_key,
                    'product_key':                p_key,
                    'warehouse_key':              wh_key,
                    'ordered_qty':                ord_qty,
                    'received_qty':               rec_qty,
                    'accepted_qty':               round(rec_qty * random.uniform(0.97, 1.0), 2),
                    'rejected_qty':               round(rec_qty * random.uniform(0.00, 0.03), 2),
                    'agreed_unit_cost_ngn':       agreed_cost,
                    'invoiced_unit_cost_ngn':     round(agreed_cost * random.uniform(0.98, 1.02), 4),
                    'freight_cost_ngn':           ngn(random.uniform(8_000, 60_000)),
                    'duty_and_tariff_ngn':        ngn(random.uniform(0, 15_000)),
                    'is_on_time':                 is_on_time if act_d else None,
                    'is_in_full':                 is_full    if act_d else None,
                    'is_otif':                    is_otif    if act_d else None,
                    'delivery_lead_time_days':    act_lead,
                    'lead_time_variance_days':    lead_var,
                    'po_status':                  'Received' if act_d else 'Shipped',
                    'load_date_key':              order_dk,
                })
            po_num += 1
            if len(rows) >= 500:
                bulk_insert(cur, 'fact_purchase_orders', rows); conn.commit()
                total += len(rows); rows = []

    if rows:
        bulk_insert(cur, 'fact_purchase_orders', rows); conn.commit(); total += len(rows)
    cur.close(); conn.close()
    print(f"  ✓ {total:,} PO lines")


# ===========================================================================
# STEP 14 — fact_budget_target
# ===========================================================================
def gen_fact_budget(stores, date_keys):
    print("\n[14/16] fact_budget_target ...")
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT MIN(date_key), fiscal_year, fiscal_month
        FROM   dim_date
        GROUP  BY fiscal_year, fiscal_month
        ORDER  BY fiscal_year, fiscal_month
    """)
    fiscal_months = cur.fetchall()
    fk_delete(cur, 'fact_budget_target')
    conn.commit()
    rows = []; total = 0

    for fm_dk, fy, fm in fiscal_months:
        yr_m   = {22: 1.00, 23: 1.08, 24: 1.17}.get(fy % 100, 1.0)
        seas_m = SEASONAL[(fm - 1) % 12]
        for store_key, region_code, store_fmt in stores:
            fmt_m = FORMATS[store_fmt][0]
            reg_m = {'SW-NG':1.20,'SS-NG':1.05,'SE-NG':0.95,'NC-NG':1.00}.get(region_code, 1.0)
            for dept, cats in DEPT_CATS.items():
                for cat, (avg_retail, avg_margin, _) in cats.items():
                    base = 3_500_000 * fmt_m * reg_m * seas_m * yr_m * random.uniform(0.85, 1.15)
                    rows.append({
                        'fiscal_month_date_key':    fm_dk,
                        'fiscal_year':              fy,
                        'fiscal_month':             fm,
                        'store_key':                store_key,
                        'category_name':            cat,
                        'department_name':          dept,
                        'budget_revenue_ngn':       ngn(base),
                        'budget_gross_profit_ngn':  ngn(base * avg_margin),
                        'budget_gross_margin_pct':  round(avg_margin * 100, 2),
                        'budget_transaction_count': random.randint(800, 6000),
                        'budget_units_sold':        round(random.uniform(300, 4000), 1),
                        'budget_lfl_growth_pct':    round(random.uniform(3, 12), 2),
                        'budget_version':           'Original',
                        'load_date_key':            fm_dk,
                    })
            if len(rows) >= 1000:
                bulk_insert(cur, 'fact_budget_target', rows); conn.commit()
                total += len(rows); rows = []

    if rows:
        bulk_insert(cur, 'fact_budget_target', rows); conn.commit(); total += len(rows)
    cur.close(); conn.close()
    print(f"  ✓ {total:,} budget rows")


# ===========================================================================
# STEP 15 — fact_finance_pl
# ===========================================================================
def gen_fact_finance_pl(cc_keys, date_keys):
    print("\n[15/16] fact_finance_pl ...")
    conn = get_conn(); cur = conn.cursor()
    cur.execute("""
        SELECT MIN(date_key), fiscal_year, fiscal_month
        FROM   dim_date
        GROUP  BY fiscal_year, fiscal_month
        ORDER  BY fiscal_year, fiscal_month
    """)
    fiscal_months = cur.fetchall()
    fk_delete(cur, 'fact_finance_pl')
    conn.commit()

    pl_lines = [
        ('Revenue',     '4000', 'Gross Revenue',         'above-the-line',  12_000_000),
        ('COGS',        '5000', 'Cost of Goods Sold',    'above-the-line',  -7_200_000),
        ('GrossProfit', '5100', 'Gross Profit',          'above-the-line',   4_800_000),
        ('StoreOpex',   '6000', 'Store Operating Costs', 'above-the-line',  -2_200_000),
        ('CentralOpex', '7000', 'Central Overheads',     'below-the-line',    -800_000),
        ('EBITDA',      '8000', 'EBITDA',                'below-the-line',   1_800_000),
    ]
    rows = []; total = 0

    for fm_dk, fy, fm in fiscal_months:
        yr_g   = {22: 1.00, 23: 1.09, 24: 1.18}.get(fy % 100, 1.0)
        seas_m = SEASONAL[(fm - 1) % 12]
        for cc_key in cc_keys:
            for pl_line, gl_code, gl_name, section, base in pl_lines:
                actual = round(base * yr_g * seas_m * random.uniform(0.88, 1.12), 2)
                budget = round(base * yr_g * seas_m * random.uniform(0.95, 1.05), 2)
                py_div = 1.09 if fy % 100 == 23 else (1.18 if fy % 100 == 24 else 1.0)
                py     = round(actual / py_div * random.uniform(0.92, 1.08), 2)

                # Do NOT insert generated columns:
                # variance_vs_budget_ngn, variance_vs_py_ngn
                rows.append({
                    'fiscal_month_date_key': fm_dk,
                    'fiscal_year':           fy,
                    'fiscal_month':          fm,
                    'cost_centre_key':       cc_key,
                    'store_key':             None,
                    'gl_account_code':       gl_code,
                    'gl_account_name':       gl_name,
                    'pl_line':               pl_line,
                    'pl_section':            section,
                    'actual_amount_ngn':     actual,
                    'budget_amount_ngn':     budget,
                    'prior_year_amount_ngn': py,
                    'journal_source':        'SAP-ERP',
                    'is_adjustment':         0,
                    'load_date_key':         fm_dk,
                })
            if len(rows) >= 1000:
                bulk_insert(cur, 'fact_finance_pl', rows); conn.commit()
                total += len(rows); rows = []

    if rows:
        bulk_insert(cur, 'fact_finance_pl', rows); conn.commit(); total += len(rows)
    cur.close(); conn.close()
    print(f"  ✓ {total:,} P&L rows")


# ===========================================================================
# STEP 16 — fact_customer_returns  +  rls_user_region_map
# ===========================================================================
def gen_fact_returns(stores, products, customers, date_keys):
    print("\n[16/16] fact_customer_returns ...")
    conn = get_conn(); cur = conn.cursor()
    fk_delete(cur, 'fact_customer_returns')
    conn.commit()

    # Only use trading date_keys (not Sundays) so return_date_key always
    # references a valid dim_date row that was actually inserted
    trading_keys = [
        k for k in date_keys
        if date(int(str(k)[:4]), int(str(k)[4:6]), int(str(k)[6:8])).isoweekday() != 7
    ]

    cust_keys = [c[0] for c in customers]
    rr_codes  = [r[0] for r in RETURN_REASONS]
    rr_descs  = [r[1] for r in RETURN_REASONS]
    rr_wts    = [r[2] for r in RETURN_REASONS]
    rows = []; total = 0

    for i in range(9000):
        d_key = random.choice(trading_keys)     # always a valid dim_date row
        store = random.choice(stores)
        prod  = random.choice(products)
        p_key, p_cat, p_dept, base_retail, base_cost, is_perish = prod
        year      = int(str(d_key)[:4])
        inflation = 1.0 + (year - 2022) * 0.065
        retail    = round(float(base_retail) * inflation, 2)
        qty       = round(random.uniform(1, 3), 1)
        reason_i  = random.choices(range(len(RETURN_REASONS)), weights=rr_wts)[0]

        rows.append({
            'return_transaction_id':   f"RTN-{d_key}-{i:06d}",
            'original_transaction_id': f"T{d_key}{store[0]:03d}{random.randint(1000,9999)}",
            'return_date_key':         d_key,
            'original_sale_date_key':  d_key,
            'store_key':               store[0],
            'product_key':             p_key,
            'customer_key':            random.choices(
                                           [1] + cust_keys[:500],
                                           weights=[40] + [1] * 500)[0],
            'channel_key':             random.randint(1, 4),
            'return_quantity':         qty,
            'refund_amount_ngn':       ngn(retail * qty),
            'restocking_cost_ngn':     ngn(retail * qty * random.uniform(0.03, 0.08)),
            'return_reason_code':      rr_codes[reason_i],
            'return_reason_desc':      rr_descs[reason_i],
            'return_outcome':          random.choices(
                                           ['Refund','Exchange','StoreCredit'],
                                           weights=[65, 25, 10])[0],
            'load_date_key':           d_key,
        })
        if len(rows) >= 500:
            bulk_insert(cur, 'fact_customer_returns', rows); conn.commit()
            total += len(rows); rows = []

    if rows:
        bulk_insert(cur, 'fact_customer_returns', rows); conn.commit(); total += len(rows)
    print(f"  ✓ {total:,} return rows")

    # ── rls_user_region_map ─────────────────────────────────────────────────
    print("\n[EXTRA] rls_user_region_map ...")
    rls = []
    for region in REGIONS:
        rls.append({
            'upn':                'ceo@primechoice.com.ng',
            'region_code':        region['code'],
            'role_type':          'CEO',
            'assigned_store_key': None,
            'assigned_category':  None,
            'is_active':          1,
        })
    rls += [
        {'upn':'rd.southwest@primechoice.com.ng',    'region_code':'SW-NG','role_type':'RegionalDirector','assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'rd.southsouth@primechoice.com.ng',   'region_code':'SS-NG','role_type':'RegionalDirector','assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'rd.southeast@primechoice.com.ng',    'region_code':'SE-NG','role_type':'RegionalDirector','assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'rd.northcentral@primechoice.com.ng', 'region_code':'NC-NG','role_type':'RegionalDirector','assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'finance@primechoice.com.ng',          'region_code':'SW-NG','role_type':'Finance',         'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'finance@primechoice.com.ng',          'region_code':'SS-NG','role_type':'Finance',         'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'finance@primechoice.com.ng',          'region_code':'SE-NG','role_type':'Finance',         'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'finance@primechoice.com.ng',          'region_code':'NC-NG','role_type':'Finance',         'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'supplychain@primechoice.com.ng',      'region_code':'SW-NG','role_type':'SupplyChain',     'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'supplychain@primechoice.com.ng',      'region_code':'SS-NG','role_type':'SupplyChain',     'assigned_store_key':None,'assigned_category':None,'is_active':1},
        {'upn':'catmgr.food@primechoice.com.ng',      'region_code':'SW-NG','role_type':'CategoryManager', 'assigned_store_key':None,'assigned_category':'Fresh Produce','is_active':1},
        {'upn':'storemanager1@primechoice.com.ng',    'region_code':'SW-NG','role_type':'StoreManager',    'assigned_store_key':1,   'assigned_category':None,'is_active':1},
    ]
    cur.execute("DELETE FROM rls_user_region_map")
    n = bulk_insert(cur, 'rls_user_region_map', rls)
    conn.commit(); cur.close(); conn.close()
    print(f"  ✓ {n} RLS user mappings")


# ===========================================================================
# MAIN
# ===========================================================================
if __name__ == '__main__':
    print("=" * 62)
    print("  PrimeChoice Retail Group — Synthetic Data Generator v4")
    print("  PRE-REQUISITE: primechoice_ddl_v3.sql must already be run")
    print("=" * 62)

    t0 = datetime.now()

    date_keys       = gen_dim_date()
    stores          = gen_dim_stores()
    products        = gen_dim_products()
    customers, tier = gen_dim_customers()
    suppliers       = gen_dim_suppliers()
    promos          = gen_dim_promotions()
    wh_keys         = gen_dim_warehouses()
    emp_keys        = gen_dim_employees(stores)
    cc_keys         = gen_dim_cost_centres(emp_keys)

    gen_bridges(products, promos)
    gen_fact_sales(stores, products, customers, tier, promos, date_keys, emp_keys)
    gen_fact_inventory(stores, products, wh_keys, date_keys)
    gen_fact_purchase_orders(products, suppliers, wh_keys, date_keys)
    gen_fact_budget(stores, date_keys)
    gen_fact_finance_pl(cc_keys, date_keys)
    gen_fact_returns(stores, products, customers, date_keys)

    elapsed = datetime.now() - t0
    print(f"\n{'=' * 62}")
    print(f"  ALL DONE  —  {str(elapsed).split('.')[0]} elapsed")
    print(f"  primechoice database is fully populated.")
    print(f"  Next: open Power BI Desktop → connect to localhost/primechoice")
    print(f"{'=' * 62}")
