import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List

# Pydantic models
class ItemIn(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    in_stock: bool = True


class ItemOut(ItemIn):
    item_id: int


# Create FastAPI app
app = FastAPI()

# Database connection
DB_PATH = "items.db"


def get_db_connection():
    """Get a database connection with check_same_thread=False"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database: create items table if not exists"""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            in_stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Mount StaticFiles at /static
app.mount("/static", StaticFiles(directory="static"), name="static")


# GET "/" should return static/index.html
@app.get("/")
async def get_index():
    return FileResponse("static/index.html")


# Startup event: initialize database
@app.on_event("startup")
async def startup_event():
    init_db()


# API endpoints under /api prefix

# POST /api/items/{item_id}
@app.post("/api/items/{item_id}", response_model=ItemOut)
async def create_item(item_id: int, item: ItemIn):
    conn = get_db_connection()
    # Convert boolean to integer for in_stock
    in_stock_int = 1 if item.in_stock else 0
    conn.execute(
        "INSERT OR REPLACE INTO items (item_id, name, price, in_stock) VALUES (?, ?, ?, ?)",
        (item_id, item.name, item.price, in_stock_int)
    )
    conn.commit()
    conn.close()
    return ItemOut(item_id=item_id, name=item.name, price=item.price, in_stock=item.in_stock)


# GET /api/items/{item_id}
@app.get("/api/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.execute("SELECT item_id, name, price, in_stock FROM items WHERE item_id = ?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Convert integer to boolean for in_stock
    return ItemOut(item_id=row["item_id"], name=row["name"], price=row["price"], in_stock=bool(row["in_stock"]))


# GET /api/items
@app.get("/api/items", response_model=List[ItemOut])
async def get_items(
    in_stock: Optional[bool] = None,
    min_price: Optional[float] = None,
    sort: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.execute("SELECT item_id, name, price, in_stock FROM items")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to list of dicts
    items = []
    for row in rows:
        items.append({
            "item_id": row["item_id"],
            "name": row["name"],
            "price": row["price"],
            "in_stock": bool(row["in_stock"])
        })
    
    # Filter by in_stock
    if in_stock is not None:
        items = [item for item in items if item["in_stock"] == in_stock]
    
    # Filter by min_price
    if min_price is not None:
        items = [item for item in items if item["price"] >= min_price]
    
    # Sort by price
    if sort is not None:
        if sort == "price_asc":
            items.sort(key=lambda x: x["price"])
        elif sort == "price_desc":
            items.sort(key=lambda x: x["price"], reverse=True)
        else:
            raise HTTPException(status_code=400, detail="Invalid sort parameter")
    
    return [ItemOut(**item) for item in items]


# DELETE /api/items/{item_id}
@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int):
    conn = get_db_connection()
    # Check if item exists
    cursor = conn.execute("SELECT item_id, name, price, in_stock FROM items WHERE item_id = ?", (item_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Delete the item
    conn.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()
    
    item = {
        "item_id": row["item_id"],
        "name": row["name"],
        "price": row["price"],
        "in_stock": bool(row["in_stock"])
    }
    return {"deleted": {"item_id": item["item_id"], "item": item}}
