from __future__ import annotations

class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self._id = product_id
        self.name = name
        self.price = float(price)

    @property
    def id(self) -> str:
        return self._id

    def price_with_tax(self) -> float:
        """Mặc định thuế 10%."""
        return round(self.price * 1.10, 2)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"


class FoodProduct(Product):
    """Ví dụ kế thừa: thực phẩm thuế thấp hơn."""
    def price_with_tax(self) -> float:
        return round(self.price * 1.05, 2)
