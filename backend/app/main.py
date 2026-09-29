from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.core.config import settings
from app.routers import health, auth, admin, citizen, volunteer, planner, ai_ops, projects, account, governance

app = FastAPI(title="JanVastu API", version="1.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS.split(","),
                   allow_credentials=False, allow_methods=["GET", "POST", "PATCH", "DELETE"],
                   allow_headers=["Authorization", "Content-Type", "Idempotency-Key"])
@app.exception_handler(RequestValidationError)
async def validation(request: Request, exc):
    return JSONResponse(status_code=422, content={"detail": "validation_error", "fields": [
        {"field": ".".join(str(x) for x in e["loc"][1:]), "type": e["type"]} for e in exc.errors()]})
@app.exception_handler(IntegrityError)
async def integrity(request: Request, exc):
    return JSONResponse(status_code=409, content={"detail": "conflict"})
app.include_router(health.router, prefix="/api/v1")
app.include_router(governance.router, prefix="/api/v1/admin")
for name, module in [("auth", auth), ("admin", admin), ("citizen", citizen), ("volunteer", volunteer), ("planner", planner), ("ai-ops", ai_ops), ("projects", projects), ("account", account)]:
    app.include_router(module.router, prefix="/api/v1/"+name)
