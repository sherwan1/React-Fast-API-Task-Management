from fastapi import FastAPI
from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router
from databaseconfig import SessionLocal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user_router)
app.include_router(task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/db-test")
# def db_test(db: Session = Depends(get_db)):
#     return {"message": "Database dependency working"}