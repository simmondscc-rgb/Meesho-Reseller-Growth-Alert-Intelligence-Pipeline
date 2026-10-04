import sqlite3
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "..", "data", "meesho_reseller.db")
OUTDIR = os.path.join(BASE, "output")
os.makedirs(OUTDIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


def run(sql):
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    return cols, cur.fetchall()


def save_csv(name, cols, rows):
    path = os.path.join(OUTDIR, name)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")


# Query 1
cols, rows = run("""
SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category
""")
save_csv("monthly_category_revenue.csv", cols, rows)
print("\n--- Query 1: Monthly category revenue ---")
for r in rows:
    print(r)
print("Grand total revenue:", round(sum(r[2] for r in rows), 2))

# Query 2
cols, rows = run("""
SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue, COUNT(*) AS n_orders
FROM orders o JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region ORDER BY total_revenue DESC
""")
save_csv("region_revenue.csv", cols, rows)
print("\n--- Query 2: Region revenue ---")
for r in rows:
    print(r)

# Query 3
cols, rows = run("""
SELECT r.reseller_id, r.reseller_name, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders o JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id, r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC LIMIT 5
""")
save_csv("top_resellers.csv", cols, rows)
print("\n--- Query 3: Top resellers (>50000) ---")
for r in rows:
    print(r)

# Query 4a
cols, rows = run("""
SELECT r.reseller_id, r.reseller_name, r.region
FROM resellers r LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL
""")
save_csv("resellers_no_orders.csv", cols, rows)
print("\n--- Query 4a: Resellers with no orders ---")
for r in rows:
    print(r)

# Query 4b
cols, rows = run("""
SELECT r.reseller_id, COUNT(*) AS count_star, COUNT(o.order_id) AS count_order_id
FROM resellers r LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id
""")
save_csv("resellers_no_orders_count_check.csv", cols, rows)
print("\n--- Query 4b: COUNT(*) vs COUNT(order_id) for RS024 ---")
for r in rows:
    print(r)

# Query 5
cols, rows = run("""
SELECT ROUND(SUM(quantity * unit_price) * 1.0 / COUNT(*), 2) AS aov_june_delivered
FROM orders WHERE month = 'June' AND status = 'Delivered'
""")
save_csv("aov_june_delivered.csv", cols, rows)
print("\n--- Query 5: AOV June Delivered ---")
for r in rows:
    print(r)

conn.close()