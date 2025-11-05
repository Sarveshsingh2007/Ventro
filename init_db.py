from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash
import seed_products  # 👈 imports your full product seeding script

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database tables created successfully!")

    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created (username: admin, password: admin123)")
    else:
        print("✅ Admin user already exists.")

    # Seed all categories and products
    try:
        seed_products.run_seed()  # 👈 this will call a function we'll define below
        print("🎉 All products & categories seeded successfully!")
    except Exception as e:
        print(f"⚠️ Seeding skipped or failed: {e}")
