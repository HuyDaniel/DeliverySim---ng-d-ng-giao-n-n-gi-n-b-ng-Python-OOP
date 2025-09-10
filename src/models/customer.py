class Customer:
    def __init__(self, customer_id: str, name: str, email: str):
        self._id = customer_id
        self.name = name
        self.email = email

    @property
    def id(self) -> str:
        return self._id

    def __repr__(self) -> str:
        return f"Customer(id={self.id}, name='{self.name}')"
