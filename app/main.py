from fastapi import FastAPI, HTTPException
from typing import List
from app.models import Item
from app.database import get_db, create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

@app.get("/items/", response_model=List[Item])
async def read_items():
    db = get_db()
    items = db.query(Item).all()
    return items

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    db = get_db()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    db = get_db()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    db = get_db()
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.price = item.price
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    db = get_db()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item
