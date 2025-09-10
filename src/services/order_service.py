from __future__ import annotations
from typing import Dict
from ..models.product import Product
from ..models.customer import Customer
from ..models.order import Order, OrderItem
from ..utils.id_generator import IdGenerator

class OrderService:
    """Đóng vai trò 'use-case layer' (dịch vụ nghiệp vụ)."""
    def __init__(self):
        self._prod_ids = IdGenerator("PROD")
        self._cust_ids = IdGenerator("CUST")
        self._order_ids = IdGenerator("ORD")

        self.products: Dict[str, Product] = {}
        self.customers: Dict[str, Customer] = {}
        self.orders: Dict[str, Order] = {}

    # --- Catalog ---
    def create_product(self, name: str, price: float) -> Product:
        p = Product(self._prod_ids.next(), name, price)
        self.products[p.id] = p
        return p

    def list_products(self):
        return list(self.products.values())

    # --- Customers ---
    def create_customer(self, name: str, email: str) -> Customer:
        c = Customer(self._cust_ids.next(), name, email)
        self.customers[c.id] = c
        return c

    # --- Orders ---
    def create_order(self, customer_id: str) -> Order:
        assert customer_id in self.customers, "Khách hàng không tồn tại"
        o = Order(self._order_ids.next(), customer_id)
        self.orders[o.id] = o
        return o

    def add_item(self, order_id: str, product_id: str, qty: int):
        assert order_id in self.orders, "Đơn hàng không tồn tại"
        assert product_id in self.products, "Sản phẩm không tồn tại"
        order = self.orders[order_id]
        product = self.products[product_id]
        order.add_item(OrderItem(product, qty))
        return order

    def order_summary(self, order_id: str) -> str:
        order = self.orders[order_id]
        lines = [f"Order {order.id} của Customer {order.customer_id}:"]
        for it in order.items:
            lines.append(f"- {it.product.name} x{it.qty} = {it.line_total()} VND (đã thuế)")
        lines.append(f"Tổng cộng: {order.total()} VND")
        return "\n".join(lines)
