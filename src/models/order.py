from __future__ import annotations
from typing import List
from .product import Product

class OrderItem:
    def __init__(self, product: Product, qty: int):
        assert qty > 0, "Số lượng phải > 0"
        self.product = product
        self.qty = qty

    def line_total(self) -> float:
        return round(self.product.price_with_tax() * self.qty, 2)

    def __repr__(self) -> str:
        return f"OrderItem(product={self.product.id}, qty={self.qty})"


class Order:
    def __init__(self, order_id: str, customer_id: str):
        self._id = order_id
        self.customer_id = customer_id
        self.items: List[OrderItem] = []

    @property
    def id(self) -> str:
        return self._id

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def total(self) -> float:
        return round(sum(i.line_total() for i in self.items), 2)

    def __repr__(self) -> str:
        return f"Order(id={self.id}, customer_id={self.customer_id}, items={len(self.items)})"
