from app import create_app
from dotenv import load_dotenv
from models import db, Category, Product, User
from werkzeug.security import generate_password_hash
import os

def run_seed():
    load_dotenv(r'Ventro\ventro.env')

    app = create_app()
    app.app_context().push()

    # Create tables
    db.create_all()

    # Create admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)

    # Categories
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

    # Retrieve categories
    cat = {c.slug: Category.query.filter_by(slug=c.slug).first() for c in categories}

    # Products
    products = [
        {"title": "Ventro Classic Tee", "slug": "ventro-classic-tee", "price": 599, "description": "Comfortable cotton tee with bold Ventro branding.", "image": "images/products/product1.jpg", "category": cat['clothing']},
        {"title": "Ventro Slim Jeans", "slug": "ventro-slim-jeans", "price": 1299, "description": "Slim fit jeans with stretchable denim.", "image": "images/products/product2.jpg", "category": cat['clothing']},
        {"title": "Ventro Hoodie", "slug": "ventro-hoodie", "price": 1599, "description": "Soft fleece hoodie perfect for all seasons.", "image": "images/products/product3.jpg", "category": cat['clothing']},
        {"title": "Ventro Backpack", "slug": "ventro-backpack", "price": 999, "description": "Stylish and durable backpack for everyday use.", "image": "images/products/product4.jpg", "category": cat['accessories']},
        {"title": "Ventro Cap", "slug": "ventro-cap", "price": 399, "description": "Adjustable cotton cap with Ventro logo.", "image": "images/products/product5.jpg", "category": cat['accessories']},
        {"title": "Ventro Smartwatch", "slug": "ventro-smartwatch", "price": 2999, "description": "Track your health and fitness with style.", "image": "images/products/product6.jpg", "category": cat['electronics']},
        {"title": "Ventro Earbuds", "slug": "ventro-earbuds", "price": 1499, "description": "Wireless earbuds with long-lasting battery.", "image": "images/products/product7.jpg", "category": cat['electronics']},
        {"title": "Ventro Power Bank", "slug": "ventro-power-bank", "price": 999, "description": "10000mAh power bank with fast charging.", "image": "images/products/product8.jpg", "category": cat['electronics']},
        {"title": "Ventro LED Lamp", "slug": "ventro-led-lamp", "price": 699, "description": "Energy-efficient LED table lamp.", "image": "images/products/product9.jpg", "category": cat['home-kitchen']},
        {"title": "Ventro Mixer Grinder", "slug": "ventro-mixer-grinder", "price": 2499, "description": "Powerful mixer grinder for home chefs.", "image": "images/products/product10.jpg", "category": cat['home-kitchen']},
        {"title": "Ventro Coffee Mug", "slug": "ventro-coffee-mug", "price": 299, "description": "Ceramic coffee mug with Ventro logo.", "image": "images/products/product11.jpg", "category": cat['food-beverages']},
        {"title": "Ventro Chocolate Box", "slug": "ventro-chocolate-box", "price": 499, "description": "Premium assorted chocolate gift box.", "image": "images/products/product12.jpg", "category": cat['food-beverages']},
        {"title": "Ventro Face Wash", "slug": "ventro-face-wash", "price": 249, "description": "Gentle cleansing face wash for all skin types.", "image": "images/products/product13.jpg", "category": cat['beauty-care']},
        {"title": "Ventro Shampoo", "slug": "ventro-shampoo", "price": 349, "description": "Nourishing shampoo with natural ingredients.", "image": "images/products/product14.jpg", "category": cat['beauty-care']},
        {"title": "Ventro Dumbbells", "slug": "ventro-dumbbells", "price": 899, "description": "Pair of rubber-coated dumbbells for workout.", "image": "images/products/product15.jpg", "category": cat['fitness-sports']},
        {"title": "Ventro Yoga Mat", "slug": "ventro-yoga-mat", "price": 799, "description": "Non-slip yoga mat with extra cushioning.", "image": "images/products/product16.jpg", "category": cat['fitness-sports']},
        {"title": "Ventro Football", "slug": "ventro-football", "price": 699, "description": "Durable synthetic leather football.", "image": "images/products/product17.jpg", "category": cat['fitness-sports']},
        {"title": "Ventro Teddy Bear", "slug": "ventro-teddy-bear", "price": 599, "description": "Soft and cuddly teddy bear for kids.", "image": "images/products/product18.jpg", "category": cat['toys-games']},
        {"title": "Ventro Board Game", "slug": "ventro-board-game", "price": 899, "description": "Fun and engaging board game for families.", "image": "images/products/product19.jpg", "category": cat['toys-games']},
        {"title": "Ventro Office Chair", "slug": "ventro-office-chair", "price": 5499, "description": "Ergonomic office chair with lumbar support.", "image": "images/products/product20.jpg", "category": cat['furniture']},
        {"title": "Ventro Study Table", "slug": "ventro-study-table", "price": 3999, "description": "Compact wooden study table with storage.", "image": "images/products/product21.jpg", "category": cat['furniture']},
        {"title": "Ventro Guitar", "slug": "ventro-guitar", "price": 6999, "description": "Acoustic guitar for beginners and pros.", "image": "images/products/product22.jpg", "category": cat['instruments']},
        {"title": "Ventro Drum Set", "slug": "ventro-drum-set", "price": 12999, "description": "Compact drum kit for music enthusiasts.", "image": "images/products/product23.jpg", "category": cat['instruments']},
        {"title": "Ventro Notebook", "slug": "ventro-notebook", "price": 199, "description": "Set of 3 ruled notebooks with soft covers.", "image": "images/products/product24.jpg", "category": cat['books-stationery']},
        {"title": "Ventro Pen Set", "slug": "ventro-pen-set", "price": 299, "description": "Premium ball pen set with smooth ink flow.", "image": "images/products/product25.jpg", "category": cat['books-stationery']},
        {"title": "Ventro Car Vacuum", "slug": "ventro-car-vacuum", "price": 1899, "description": "Portable vacuum cleaner for car interiors.", "image": "images/products/product26.jpg", "category": cat['automotive']},
        {"title": "Ventro Car Perfume", "slug": "ventro-car-perfume", "price": 499, "description": "Long-lasting car air freshener with ocean scent.", "image": "images/products/product27.jpg", "category": cat['automotive']},
        {"title": "Ventro Wall Clock", "slug": "ventro-wall-clock", "price": 899, "description": "Modern wall clock with silent sweep movement.", "image": "images/products/product28.jpg", "category": cat['home-kitchen']},
        {"title": "Ventro Table Fan", "slug": "ventro-table-fan", "price": 1299, "description": "3-speed table fan for powerful air circulation.", "image": "images/products/product29.jpg", "category": cat['home-kitchen']},
        {"title": "Ventro Protein Shake", "slug": "ventro-protein-shake", "price": 999, "description": "Delicious protein supplement for fitness lovers.", "image": "images/products/product30.jpg", "category": cat['food-beverages']}
    ]

    # Add products if not already existing
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
    print("🎉 Database seeded with all categories and multiple products successfully!")
