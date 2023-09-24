from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from database import database, users, products, orders
from models import User, UserCreate, Product, ProductCreate, Order, OrderCreate
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# CRUD операции для пользователей
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    try:
        query = users.insert().values(**user.dict(), password=user.password)
        user_id = await database.execute(query)
        return {**user.dict(), "id": user_id}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = select([users]).where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CRUD операции для товаров
@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate):
    query = products.insert().values(**product.dict())
    product_id = await database.execute(query)
    return {**product.dict(), "id": product_id}

@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = select([products]).where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductCreate):
    query = (
        products
        .update()
        .where(products.c.id == product_id)
        .values(**product.dict())
        .returning(products)
    )
    updated_product = await database.execute(query)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    deleted_product = await database.execute(query)
    if deleted_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return deleted_product

# CRUD операции для заказов
@app.post("/orders/", response_model=Order)
async def create_order(order: OrderCreate):
    query = orders.insert().values(**order.dict(), order_date=datetime.now())
    order_id = await database.execute(query)
    return {**order.dict(), "id": order_id, "order_date": datetime.now()}

@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = select([orders]).where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderCreate):
    query = (
        orders
        .update()
        .where(orders.c.id == order_id)
        .values(**order.dict())
        .returning(orders)
    )
    updated_order = await database.execute(query)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    deleted_order = await database.execute(query)
    if deleted_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)