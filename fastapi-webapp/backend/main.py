from fastapi import FastAPI, HTTPException, status
from database.connection import engine
from database import models
from auth.register import router as auth_router
from auth.login import router as login_router
from auth.user_data import router as user_data_router
from auth.secret import router as secret_router
from middleware.conf import middleware_config
from config import HOST, PORT
import uvicorn

app = FastAPI()
middleware_config(app)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app.add_event_handler("startup", init_db)
app.include_router(auth_router, prefix="/auth")
app.include_router(login_router, prefix="/auth")
app.include_router(user_data_router, prefix="/data")
app.include_router(secret_router, prefix="/data")

@app.get("/")
def read_root():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not authorized to view this content"
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
