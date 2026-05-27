"""Puntos de entrada de FASTAPI y eventos startup/shutdown"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos los routers
from src.rutas.auth_rutas import router as auth_router
# A futuro acá importarás: caballo_routes, carrera_routes, etc.

app = FastAPI(
    title="EquiData API - Grupo 10",
    description="API políglota para el análisis y gestión del ecosistema ecuestre.",
    version="1.0.0"
)

# --- MIDDLEWARES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers['X-Custom-Header'] = 'EquiData-Grupo10'
    return response 

# --- INCLUSIÓN DE RUTAS ---
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
# app.include_router(caballos_router, prefix="/caballos", tags=["Registro Maestro"])

# --- EVENTOS DE CICLO DE VIDA ---
@app.on_event("startup")
async def startup_event():
    print("EquiData API Iniciando...")
    # TODO: Acá inicializaremos las conexiones a MongoDB y Redis

@app.on_event("shutdown")
async def shutdown_event():
    print("EquiData API Cerrando...")
    # TODO: Acá cerraremos las conexiones a las bases de datos de forma segura

# --- ENDPOINT BASE (Health Check) ---
@app.get('/', tags=["General"])
async def root():
    return {
        "mensaje": "Bienvenido a EquiData API",
        "grupo": 10
    }