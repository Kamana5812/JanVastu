"""Initialize a dedicated hosted database, then run the API as its restricted role."""
import hashlib
import hmac
import os
import subprocess
import sys

# Ensure /app (the project root inside the container) is always on sys.path,
# regardless of the working directory Render chooses to use.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
os.environ.setdefault("PYTHONPATH", _project_root)

from sqlalchemy.engine import make_url


def main():
    env=os.environ.copy()
    owner=env.pop("JANVASTU_OWNER_DATABASE_URL","")
    if owner:
        secret=env.get("SECRET_KEY","")
        if len(secret)<32 or secret.startswith("development-"):
            raise SystemExit("Hosted initialization requires a generated SECRET_KEY.")
        if owner.startswith("postgres://"):
            owner=owner.replace("postgres://","postgresql+psycopg2://",1)
        url=make_url(owner)
        password=hmac.new(secret.encode(),b"janvastu-runtime-database-role-v1",hashlib.sha256).hexdigest()
        setup={**env,"DATABASE_URL":owner,"RUNTIME_DB_PASSWORD":password}
        for command in ([sys.executable,"-m","alembic","upgrade","head"],
                        [sys.executable,"-m","app.db.provision"],
                        [sys.executable,"-m","app.db.seed"]):
            result=subprocess.run(command,env=setup,capture_output=True,text=True)
            output=result.stdout+result.stderr
            for value in (owner,url.password,password):
                if value:output=output.replace(value,"[redacted]")
            print(output,flush=True)
            if result.returncode:raise SystemExit("Hosted database initialization failed.")
        env["DATABASE_URL"]=url.set(username="janvastu_api",password=password).render_as_string(hide_password=False)
    env.pop("RUNTIME_DB_PASSWORD",None)
    # Owner credentials are absent from the serving process environment.
    os.execvpe(sys.executable,[sys.executable,"-m","uvicorn","app.main:app","--host","0.0.0.0","--port",env.get("PORT","8000")],env)


if __name__=="__main__":main()
