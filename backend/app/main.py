import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import get_settings
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(name)s %(message)s')
settings=get_settings(); app=FastAPI(title="India Semiconductor Project Tracker API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',')],allow_methods=["GET","POST","PATCH"],allow_headers=["Content-Type","X-Admin-Key"])
app.include_router(router)
@app.get("/health")
def health(): return {"status":"ok"}
