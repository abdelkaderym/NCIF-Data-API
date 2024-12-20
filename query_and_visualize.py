import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db_name = "ncif_data.db"
conn = sqlite3.connect(db_name)

query_density = """
SELECT
    sod_data.census_tract AS census_tract,
    COUNT(sod_data.NAMEBR) AS total_branches
FROM
    sod_data
WHERE
    sod_data.census_tract IS NOT NULL
GROUP BY
    sod_data.census_tract;
"""
density_df = pd.read_sql_query(query_density, conn)
print("Branch Density by Census Tract:")
print(density_df)

query_pm_density = """
SELECT
    epa_data.census_tract,
    epa_data.arithmetic_mean AS pm25,
    COUNT(sod_data.NAMEBR) AS total_branches
FROM
    epa_data
JOIN
    sod_data ON epa_data.census_tract = sod_data.census_tract
WHERE
    epa_data.census_tract IS NOT NULL
GROUP BY
    epa_data.census_tract
HAVING
    epa_data.arithmetic_mean > 5 AND total_branches > 3;
"""
pm_density_df = pd.read_sql_query(query_pm_density, conn)
print("Census Tracts with PM2.5 > 5 and > 3 Branches:")
print(pm_density_df)

plt.figure(figsize=(10, 6))
plt.scatter(pm_density_df['pm25'], pm_density_df['total_branches'], alpha=0.7)
plt.title("PM2.5 Levels vs Branch Density")
plt.xlabel("PM2.5 Levels")
plt.ylabel("Branch Density")
plt.grid(True)
plt.show()

conn.close()
