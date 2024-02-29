#  This is the main file of the project.
#  You can find all documentation and test the API in http://127.0.0.1:8000
import json
import subprocess
import sys
import uuid

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.mananger import get_user_manager
from database import async_session_maker, create_db_and_tables
from dto.user import UserRead, UserCreate
from models.ticket import Ticket
from models.user import User
from routers import ticket as ticket_router
from routers import user as user_router
import uvicorn
from starlette.middleware.cors import CORSMiddleware


#  Install requirements from requirements.txt
def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


install_requirements()

#  Create FastAPI instance
app = FastAPI(
    title="WIX Ticket System"
)

origins = [
    "https://localhost:5173",
    "https://localhost:5173/",
    "https://localhost:5173/*"
    # другие домены, с которых разрешены запросы
]

#  CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # разрешить cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


#  Load data from json file to database if database is empty (for first run)
async def load_data_from_json(db_session: AsyncSession, json_file="data.json"):
    result = await db_session.execute(select(Ticket).limit(1))
    instance = result.scalars().first()
    if not instance:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            new_record = Ticket(**item)
            db_session.add(new_record)
        await db_session.commit()


@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()
    # Create database session
    db = async_session_maker()

    # Load data from json file to database if database is empty (for first run)
    await load_data_from_json(db)

    # Close database session
    await db.close()


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


#  Add routers
app.include_router(
    ticket_router.router,
    prefix="/tickets",
    tags=["ticket"])
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    user_router.router,
    prefix="/user",
    tags=["user"])
current_active_user = fastapi_users.current_user(active=True)

# Run server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, workers=2)
