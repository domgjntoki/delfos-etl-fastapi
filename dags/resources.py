# ./dags/resources.py
from dagster import resource
import psycopg2
import httpx

@resource
def source_api_resource():
    return httpx.Client(base_url="http://fastapi:8000")

@resource
def target_db_resource():
    return "postgresql://alvo_user:alvo_pass@alvo-db:5432/alvo"
