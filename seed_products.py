from app import create_app
from dotenv import load_dotenv
from models import db, Category, Product, User
from werkzeug.security import generate_password_hash
import os

# Load environment variables
load_dotenv(r'Ventro\ventro.env')

# Create app instance
app = create_app()

# ✅ Everything below stays inside the app context
with app.app_context():
    # Drop and recreate tables
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated successfully!")

    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("👑 Admin user created.")
    else:
        print("👑 Admin already exists.")

    # Add categories
    categories = [
        Category(name='Clothing', slug='clothing'),
        Category(name='Accessories', slug='accessories'),
        Category(name='Electronics', slug='electronics'),
        Category(name='Home & Kitchen', slug='home-kitchen'),
        Category(name='Food & Beverages', slug='food-beverages'),
        Category(name='Beauty & Personal Care', slug='beauty-care'),
        Category(name='Fitness & Sports', slug='fitness-sports'),
        Category(name='Toys & Games', slug='toys-games'),
        Category(name='Furniture', slug='furniture'),
        Category(name='Musical Instruments', slug='instruments'),
        Category(name='Books & Stationery', slug='books-stationery'),
        Category(name='Automotive', slug='automotive')
    ]

    for c in categories:
        if not Category.query.filter_by(slug=c.slug).first():
            db.session.add(c)
    db.session.commit()
    print("📂 Categories added successfully!")

    # Retrieve category references
    cat = {c.slug: Category.query.filter_by(slug=c.slug).first() for c in categories}

    # ✅ Products are also added *inside* app context
    products = [
        # Clothing
        {"title": "Ventro Classic Tee", "slug": "ventro-classic-tee", "price": 599, "description": "Comfortable cotton tee with bold Ventro branding.", "image": "images/products/product1.jpg", "category": cat['clothing']},
        {"title": "Ventro Slim Jeans", "slug": "ventro-slim-jeans", "price": 1299, "description": "Slim fit jeans with stretchable denim.", "image": "images/products/product2.jpg", "category": cat['clothing']},
        {"title": "Ventro Hoodie", "slug": "ventro-hoodie", "price": 1599, "description": "Soft fleece hoodie perfect for all seasons.", "image": "images/products/product3.jpg", "category": cat['clothing']},
        {"title": "Ventro Formal Shirt", "slug": "ventro-formal-shirt", "price": 899, "description": "Crisp white formal shirt for office and events.", "image": "images/products/product4.jpg", "category": cat['clothing']},

        # Accessories
        {"title": "Minimalist Watch", "slug": "minimalist-watch", "price": 2499, "description": "Sleek and water-resistant watch.", "image": "images/products/product5.jpg", "category": cat['accessories']},
        {"title": "Stylish Sunglasses", "slug": "stylish-sunglasses", "price": 799, "description": "UV protected sunglasses for men & women.", "image": "images/products/product6.jpg", "category": cat['accessories']},
        {"title": "Leather Wallet", "slug": "leather-wallet", "price": 699, "description": "Premium leather wallet with multiple compartments.", "image": "images/products/product7.jpg", "category": cat['accessories']},

        # Electronics
        {"title": "Noise Cancelling Headset", "slug": "noise-headset", "price": 3999, "description": "Premium sound and active noise cancellation.", "image": "images/products/product8.jpg", "category": cat['electronics']},
        {"title": "Ventro Smartwatch", "slug": "ventro-smartwatch", "price": 2599, "description": "Track your health and notifications in style.", "image": "images/products/product9.jpg", "category": cat['electronics']},
        {"title": "Bluetooth Speaker", "slug": "bluetooth-speaker", "price": 1599, "description": "Compact speaker with deep bass.", "image": "images/products/product10.jpg", "category": cat['electronics']},
        {"title": "Ventro Powerbank 20000mAh", "slug": "ventro-powerbank", "price": 1999, "description": "Fast charging powerbank for all devices.", "image": "images/products/product11.jpg", "category": cat['electronics']},

        # Home & Kitchen
        {"title": "Non-Stick Cookware Set", "slug": "cookware-set", "price": 2299, "description": "Durable and stylish cookware for modern kitchens.", "image": "images/products/product12.jpg", "category": cat['home-kitchen']},
        {"title": "Electric Kettle", "slug": "electric-kettle", "price": 899, "description": "1.8L stainless steel kettle with auto shutoff.", "image": "images/products/product13.jpg", "category": cat['home-kitchen']},
        {"title": "Mixer Grinder", "slug": "mixer-grinder", "price": 3299, "description": "750W motor with 3 stainless steel jars.", "image": "images/products/product14.jpg", "category": cat['home-kitchen']},

        # Food & Beverages
        {"title": "Organic Honey 500g", "slug": "organic-honey", "price": 399, "description": "Pure Himalayan organic honey.", "image": "images/products/product15.jpg", "category": cat['food-beverages']},
        {"title": "Dark Roast Coffee 250g", "slug": "dark-roast-coffee", "price": 299, "description": "Strong aromatic dark roast beans.", "image": "images/products/product16.jpg", "category": cat['food-beverages']},
        {"title": "Green Tea Pack", "slug": "green-tea", "price": 249, "description": "Refreshing detox green tea.", "image": "images/products/product17.jpg", "category": cat['food-beverages']},

        # Beauty & Personal Care
        {"title": "Herbal Face Wash", "slug": "herbal-face-wash", "price": 199, "description": "Gentle natural cleanser with neem and aloe.", "image": "images/products/product18.jpg", "category": cat['beauty-care']},
        {"title": "Aloe Vera Moisturizer", "slug": "aloe-vera-moisturizer", "price": 249, "description": "Hydrating moisturizer with vitamin E.", "image": "images/products/product19.jpg", "category": cat['beauty-care']},
        {"title": "Hair Serum", "slug": "hair-serum", "price": 349, "description": "Protects and strengthens damaged hair.", "image": "images/products/product20.jpg", "category": cat['beauty-care']},

        # Fitness & Sports
        {"title": "Ventro Yoga Mat", "slug": "ventro-yoga-mat", "price": 799, "description": "Anti-slip yoga mat for comfort.", "image": "images/products/product21.jpg", "category": cat['fitness-sports']},
        {"title": "Dumbbell Set", "slug": "dumbbell-set", "price": 2499, "description": "Adjustable dumbbell set for home workouts.", "image": "images/products/product22.jpg", "category": cat['fitness-sports']},
        {"title": "Resistance Bands", "slug": "resistance-bands", "price": 699, "description": "Set of 5 stretchable resistance bands.", "image": "images/products/product23.jpg", "category": cat['fitness-sports']},

        # Toys & Games
        {"title": "LEGO Building Set", "slug": "lego-building-set", "price": 1599, "description": "Creative 500-piece LEGO set.", "image": "images/products/product24.jpg", "category": cat['toys-games']},
        {"title": "Remote Control Car", "slug": "remote-car", "price": 999, "description": "High-speed rechargeable RC car.", "image": "images/products/product25.jpg", "category": cat['toys-games']},
        {"title": "Puzzle Game", "slug": "puzzle-game", "price": 499, "description": "1000-piece puzzle for all ages.", "image": "images/products/product26.jpg", "category": cat['toys-games']},

        # Furniture
        {"title": "Ergonomic Office Chair", "slug": "office-chair", "price": 4999, "description": "Mesh chair with lumbar support.", "image": "images/products/product27.jpg", "category": cat['furniture']},
        {"title": "Wooden Coffee Table", "slug": "wooden-coffee-table", "price": 2999, "description": "Stylish table with oak finish.", "image": "images/products/product28.jpg", "category": cat['furniture']},
        {"title": "Bookshelf", "slug": "bookshelf", "price": 3499, "description": "5-tier wooden bookshelf.", "image": "images/products/product29.jpg", "category": cat['furniture']},

        # Instruments
        {"title": "Acoustic Guitar", "slug": "acoustic-guitar", "price": 6999, "description": "6-string guitar with rich tone.", "image": "images/products/product30.jpg", "category": cat['instruments']},
        {"title": "Digital Keyboard", "slug": "digital-keyboard", "price": 8499, "description": "61-key electronic keyboard.", "image": "images/products/product31.jpg", "category": cat['instruments']},

        # Books
        {"title": "The Power of Habit", "slug": "power-of-habit", "price": 499, "description": "Bestselling book by Charles Duhigg.", "image": "images/products/product32.jpg", "category": cat['books-stationery']},
        {"title": "Ventro Notebook Set", "slug": "ventro-notebook-set", "price": 299, "description": "Pack of 3 stylish notebooks.", "image": "images/products/product33.jpg", "category": cat['books-stationery']},

        # Automotive
        {"title": "Car Vacuum Cleaner", "slug": "car-vacuum", "price": 1299, "description": "Portable cleaner for easy car care.", "image": "images/products/product34.jpg", "category": cat['automotive']},
        {"title": "Car Phone Mount", "slug": "car-phone-mount", "price": 499, "description": "Magnetic dashboard phone holder.", "image": "images/products/product35.jpg", "category": cat['automotive']}
    ]

    for p in products:
        if not Product.query.filter_by(slug=p['slug']).first():
            product = Product(
                title=p['title'],
                slug=p['slug'],
                price=p['price'],
                description=p['description'],
                image=p['image'],
                category=p['category']
            )
            db.session.add(product)

    db.session.commit()
    print("🎉 Database seeded with all categories and products successfully!")
