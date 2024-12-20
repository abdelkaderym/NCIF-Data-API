from fastapi import FastAPI, Query
import sqlite3
import pandas as pd

app = FastAPI()

DB_NAME = "ncif_data.db"

def query_database(sql_query: str):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

@app.get("/")
def home():
    return {"message": "Welcome to the NCIF API. Use /tracts to get data or /predict for predictions."}

@app.get("/tracts")
def get_tracts(pm25_min: float = Query(5, description="Minimum PM2.5 level"),
               branches_min: int = Query(3, description="Minimum branch count")):
    """
    Fetch census tracts filtered by PM2.5 levels and branch density.
    """
    query = f"""
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
        pm25 > {pm25_min} AND total_branches > {branches_min};
    """
    df = query_database(query)
    return df.to_dict(orient="records")

@app.get("/predict")
def predict_pm25(branch_density: int = Query(..., description="Branch density (number of branches)")):
    """
    Predict PM2.5 levels based on branch density using a simple linear model.
    """
    # Dummy model: PM2.5 increases slightly with branch density
    predicted_pm25 = 5 + 0.2 * branch_density
    return {"branch_density": branch_density, "predicted_pm25": predicted_pm25}
