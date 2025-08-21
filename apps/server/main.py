from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.orchestrate import router as orchestrate_router
from routers.diagnostics import router as diagnostics_router
from routers.transactions import router as transactions_router
from routers.onboarding import router as onboarding_router

app = FastAPI(title='Agent Orchestrator', version='0.1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.include_router(orchestrate_router)
app.include_router(diagnostics_router)
app.include_router(transactions_router)
app.include_router(onboarding_router)

@app.get('/health')
def health(): return {'ok': True}
