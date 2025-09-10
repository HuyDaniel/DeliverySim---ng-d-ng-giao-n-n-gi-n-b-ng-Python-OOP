# 🛒 OOP Shop (Python + FastAPI)

Demo dự án **OOP cơ bản với Python**:  
- Quản lý **Sản phẩm – Khách hàng – Đơn hàng** bằng OOP (class, kế thừa, đa hình).  
- Có thể chạy **CLI app** (`app.py`) hoặc chạy **REST API với FastAPI** (`src/api.py`).  

---

## 📂 Cấu trúc thư mục

OOP_shop/
├─ app.py # Demo chạy console (in kết quả ra terminal)
├─ requirements.txt # Danh sách thư viện cần cài
├─ src/
│ ├─ api.py # FastAPI app
│ ├─ init.py
│ ├─ models/ # Các class mô hình (Product, Customer, Order)
│ │ ├─ product.py
│ │ ├─ customer.py
│ │ ├─ order.py
│ │ └─ init.py
│ ├─ services/ # Lớp xử lý nghiệp vụ
│ │ ├─ order_service.py
│ │ └─ init.py
│ └─ utils/ # Tiện ích (id generator)
│ ├─ id_generator.py
│ └─ init.py


---

## ⚙️ Cài đặt môi trường

```bash
# 1. Tạo và kích hoạt venv
python -m venv Myvenv
Myvenv\Scripts\activate   # Windows
# source Myvenv/bin/activate  # Linux/macOS

# 2. Cài dependencies
pip install -r requirements.txt
fastapi
uvicorn
pydantic[email]
Chạy console app
python app.py
Ví dụ output
Order ORD-1 của Customer CUST-1:
- Chuột gaming x2 = 210000.0 VND (đã thuế)
- Bàn phím cơ x1 = 880000.0 VND (đã thuế)
Tổng cộng: 1090000.0 VND
Chạy web API
python -m uvicorn src.api:app --reload


