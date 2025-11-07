from app import create_app
from models import db
import runpy
import os

app = create_app()

with app.app_context():
    print("🧹 Dropping and recreating tables...")
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated successfully!")

    # Now run seeding file
    print("🌱 Running seed_products.py...")
    runpy.run_path(os.path.join(os.path.dirname(__file__), "seed_products.py"))
    print("🎉 Database seeded successfully!")
