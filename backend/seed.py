from app.db import SessionLocal
from app.models import Item, User
from app.auth import get_password_hash

def run():
    db = SessionLocal()
    try:
        # seed a demo user
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(username="admin", hashed_password=get_password_hash("admin123")))

        # seed items
        seed_items = [
            ("SKU-0001", "4006381333931", 25),
            ("SKU-0002", "8412345678906", 10),
            ("SKU-0003", "5012345678900", 0),
        ]
        for sku, ean, qty in seed_items:
            if not db.query(Item).filter(Item.sku == sku).first():
                db.add(Item(sku=sku, ean13=ean, quantity=qty))
        db.commit()
        print("Seed complete")
    finally:
        db.close()

if __name__ == "__main__":
    run()
