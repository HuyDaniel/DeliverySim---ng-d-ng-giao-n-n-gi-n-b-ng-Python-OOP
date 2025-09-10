# src/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List

from src.services.order_service import OrderService
from src.models.product import Product, FoodProduct
from src.models.order import Order, OrderItem

app = FastAPI(title="OOP Shop API", version="0.1.0")

# CORS cho dev frontend thử nhanh
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ----- Pydantic Schemas -----
class ProductIn(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    price_with_tax: float

class CustomerIn(BaseModel):
    name: str
    email: EmailStr

class CustomerOut(BaseModel):
    id: str
    name: str
    email: EmailStr

class OrderCreate(BaseModel):
    customer_id: str

class AddItemIn(BaseModel):
    product_id: str
    qty: int = Field(..., gt=0)

class OrderItemOut(BaseModel):
    product_id: str
    product_name: str
    qty: int
    line_total: float

class OrderOut(BaseModel):
    id: str
    customer_id: str
    items: List[OrderItemOut]
    total: float

# ----- Helpers chuyển model -> schema -----
def to_product_out(p: Product) -> ProductOut:
    return ProductOut(
        id=p.id, name=p.name, price=p.price, price_with_tax=p.price_with_tax()
    )

def to_order_out(o: Order) -> OrderOut:
    items = [
        OrderItemOut(
            product_id=i.product.id,
            product_name=i.product.name,
            qty=i.qty,
            line_total=i.line_total(),
        )
        for i in o.items
    ]
    return OrderOut(id=o.id, customer_id=o.customer_id, items=items, total=o.total())

# ----- Lifespan: khởi tạo service + seed demo -----
@app.on_event("startup")
def startup():
    svc = OrderService()
    # seed nhẹ cho dễ test
    p1 = svc.create_product("Chuột gaming", 300000)
    p2 = svc.create_product("Bàn phím cơ", 800000)
    # ví dụ kế thừa / polymorphism
    svc.products[p1.id] = FoodProduct(p1.id, p1.name, p1.price / 3)
    c1 = svc.create_customer("Huy", "huy@example.com")
    # lưu vào app state
    app.state.svc = svc

def get_svc() -> OrderService:
    return app.state.svc  # kiểu singleton in-memory

# ----- Endpoints -----
@app.get("/health")
def health():
    return {"status": "ok"}

# Products
@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(body: ProductIn):
    svc = get_svc()
    p = svc.create_product(body.name, body.price)
    return to_product_out(p)

@app.get("/products", response_model=List[ProductOut])
def list_products():
    svc = get_svc()
    return [to_product_out(p) for p in svc.list_products()]

# Customers
@app.post("/customers", response_model=CustomerOut, status_code=201)
def create_customer(body: CustomerIn):
    svc = get_svc()
    c = svc.create_customer(body.name, body.email)
    return CustomerOut(id=c.id, name=c.name, email=c.email)

# Orders
@app.post("/orders", response_model=OrderOut, status_code=201)
def create_order(body: OrderCreate):
    svc = get_svc()
    if body.customer_id not in svc.customers:
        raise HTTPException(404, "Khách hàng không tồn tại")
    o = svc.create_order(body.customer_id)
    return to_order_out(o)

@app.post("/orders/{order_id}/items", response_model=OrderOut)
def add_item(order_id: str, body: AddItemIn):
    svc = get_svc()
    if order_id not in svc.orders:
        raise HTTPException(404, "Đơn hàng không tồn tại")
    if body.product_id not in svc.products:
        raise HTTPException(404, "Sản phẩm không tồn tại")
    svc.add_item(order_id, body.product_id, body.qty)
    return to_order_out(svc.orders[order_id])

@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str):
    svc = get_svc()
    if order_id not in svc.orders:
        raise HTTPException(404, "Đơn hàng không tồn tại")
    return to_order_out(svc.orders[order_id])

@app.get("/orders/{order_id}/summary")
def order_summary(order_id: str):
    svc = get_svc()
    if order_id not in svc.orders:
        raise HTTPException(404, "Đơn hàng không tồn tại")
    return {"summary": svc.order_summary(order_id)}
