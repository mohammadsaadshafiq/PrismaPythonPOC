import asyncio
from fastapi import FastAPI
from prisma import Prisma
import uvicorn


app = FastAPI()
prisma = Prisma()


async def connect() -> None:
    await prisma.connect()


@app.on_event("startup")
async def startup_event():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()


@app.post("/users")
async def create_user(user: dict):
    created_user = await prisma.user.create(user)
    return created_user


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    return user


@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    updated_user = await prisma.user.update(where={"id": user_id}, data=user_data)
    return updated_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    deleted_user = await prisma.user.delete(where={"id": user_id})
    return deleted_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
