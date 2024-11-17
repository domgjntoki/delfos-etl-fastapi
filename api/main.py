from fastapi import FastAPI, Query
import psycopg2
from typing import List

app = FastAPI()

DATABASE_URL = "dbname=fonte user=fonte_user password=fonte_pass host=fonte-db"

@app.get("/data")
def get_data(start: str, end: str, variables: List[str] = Query(...)):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    variable_columns = ", ".join(variables)
    query = f"""
        SELECT timestamp, {variable_columns}
        FROM data
        WHERE timestamp BETWEEN %s AND %s
    """
    cursor.execute(query, (start, end))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"data": result}

