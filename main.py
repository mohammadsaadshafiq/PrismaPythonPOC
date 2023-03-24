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


@app.post("/collection")
async def create_user(collection: dict):
    created_user = await prisma.collection.create(collection)
    return created_user


@app.get("/collection/{id}")
async def get_user(id):
    user = await prisma.collection.find_unique(where={"id": id})
    return user


@app.put("/collection/{id}")
async def update_user(id: str, collection_data: dict):
    updated_user = await prisma.collection.update(
        where={"id": id}, data=collection_data
    )
    return updated_user


@app.delete("/collection/{id}")
async def delete_user(id):
    deleted_user = await prisma.collection.delete(where={"id": id})
    return deleted_user


@app.get("/collection/path/{language}")
async def get_local_paths(language: str):
    records = await prisma.collection.find_many(where={"Language": language})
    return records


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
