PRODUCTS = [
    {"id": 1, "name": "Teclado", "price": 25000},
    {"id": 2, "name": "Mouse", "price": 15000},
    {"id": 3, "name": "Monitor", "price": 120000},
]


def delete_product(product_id: int) -> bool:
    for index, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            PRODUCTS.pop(index)
            return True
    return False
