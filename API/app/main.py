from fastapi import FastAPI
from app.config import engine
from app import router

app = FastAPI()

# @app.on_event("startup")
# async def startup():
#     await engine.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await engine.disconnect()

@app.get("/")
async def Home():
    return "Welcome to the Lab Monitoring API of Uniandes"

app.include_router(router.router)