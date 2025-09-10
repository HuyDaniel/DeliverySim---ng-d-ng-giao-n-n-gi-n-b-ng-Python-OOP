from src.services.order_service import OrderService
from src.models.product import FoodProduct  # demo kế thừa

def seed_data(svc: OrderService):
    # Tạo sẵn vài product/food (kế thừa)
    p1 = svc.create_product("Chuột gaming", 300000)
    p2 = svc.create_product("Bàn phím cơ", 800000)

    # Ghi đè một sản phẩm thành FoodProduct để demo polymorphism
    svc.products[p1.id] = FoodProduct(p1.id, p1.name, p1.price / 3)  # giả sử chuột… là đồ ăn 🤖

    c1 = svc.create_customer("Huy", "huy@example.com")
    return p1, p2, c1

def main():
    svc = OrderService()
    p1, p2, c1 = seed_data(svc)

    order = svc.create_order(c1.id)
    svc.add_item(order.id, p1.id, 2)
    svc.add_item(order.id, p2.id, 1)

    print(svc.order_summary(order.id))

if __name__ == "__main__":
    main()
