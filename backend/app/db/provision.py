"""Run after migrations as the database owner. API uses janvastu_api."""
import os
from sqlalchemy import text
from psycopg2 import sql
from app.db.base import engine
def provision():
    password=os.environ.get("RUNTIME_DB_PASSWORD")
    if not password or len(password)<16:raise SystemExit("Set RUNTIME_DB_PASSWORD to at least 16 characters.")
    with engine.begin() as connection:
        raw=connection.connection.driver_connection
        with raw.cursor() as cursor:
            if not connection.scalar(text("SELECT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='janvastu_api')")):
                cursor.execute("CREATE ROLE janvastu_api LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT")
            cursor.execute(sql.SQL("ALTER ROLE janvastu_api PASSWORD {}").format(sql.Literal(password)))
        connection.execute(text("GRANT USAGE ON SCHEMA public TO janvastu_api"))
        connection.execute(text("GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO janvastu_api"))
        connection.execute(text("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO janvastu_api"))
        connection.execute(text("REVOKE ALL ON audit_logs FROM janvastu_api"))
        connection.execute(text("GRANT SELECT, INSERT ON audit_logs TO janvastu_api"))
        connection.execute(text("REVOKE ALL ON alembic_version FROM janvastu_api"))
    print("Runtime role ready; audit writes are limited to inserts.")
if __name__=="__main__":provision()
