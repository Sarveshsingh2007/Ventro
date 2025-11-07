import os
import uuid
from flask import Flask, render_template, redirect, url_for, request, session, flash
from config import Config
from models import db, User, Category, Product, Order
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import stripe
from dotenv import load_dotenv
from werkzeug.utils import secure_filename


# ✅ Load environment variables
load_dotenv()  # automatically loads from Ventro/.env

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # ✅ Load Stripe keys from environment
    app.config['STRIPE_PUBLISHABLE_KEY'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
    app.config['STRIPE_SECRET_KEY'] = os.getenv('STRIPE_SECRET_KEY')

    # ✅ Debug print to verify they loaded (optional)
    print("Stripe Publishable Key Loaded:", bool(app.config['STRIPE_PUBLISHABLE_KEY']))
    print("Stripe Secret Key Loaded:", bool(app.config['STRIPE_SECRET_KEY']))

    db.init_app(app)

    # ✅ Auto-create tables if they don't exist
    with app.app_context():
        db.create_all()

    # ✅ Stripe setup
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

    # ✅ Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---------- Helper: Cart ----------
    def _get_cart():
        return session.setdefault('cart', {})

    def _cart_total_and_items():
        cart = _get_cart()
        items = []
        total = 0
        for pid, qty in cart.items():
            p = Product.query.get(int(pid))
            if not p:
                continue
            subtotal = p.price * qty
            items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
        return total, items

    # ---------- Routes ----------
    @app.route('/')
    def home():
        products = Product.query.all()
        categories = Category.query.all()
        print(f"✅ Home route loaded: {len(products)} products found.")
        return render_template('home.html', products=products, categories=categories)

    @app.route('/search')
    def search():
        query = request.args.get('q', '').strip()
        categories = Category.query.all()
        results = []
        if query:
            results = Product.query.filter(Product.title.ilike(f"%{query}%")).all()
        return render_template('search_results.html', query=query, results=results, categories=categories)

    @app.route('/category/<slug>')
    def category_view(slug):
        cat = Category.query.filter_by(slug=slug).first_or_404()
        products = Product.query.filter_by(category=cat).all()
        categories = Category.query.all()
        return render_template('category.html', category=cat, products=products, categories=categories)

    @app.route('/product/<slug>')
    def product_view(slug):
        product = Product.query.filter_by(slug=slug).first_or_404()
        return render_template('product.html', product=product)

    @app.route('/add-to-cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        qty = int(request.form.get('qty', 1))
        cart = _get_cart()
        cart[str(product_id)] = cart.get(str(product_id), 0) + qty
        session['cart'] = cart
        flash('Added to cart', 'success')
        return redirect(request.referrer or url_for('home'))

    @app.route('/cart')
    def cart():
        total, items = _cart_total_and_items()
        return render_template('cart.html', total=total, items=items)

    @app.route('/cart/update', methods=['POST'])
    def cart_update():
        cart = _get_cart()
        for pid, qty in request.form.items():
            if pid.startswith('qty_'):
                product_id = pid.split('_', 1)[1]
                try:
                    q = int(qty)
                except ValueError:
                    q = 1
                if q <= 0:
                    cart.pop(product_id, None)
                else:
                    cart[product_id] = q
        session['cart'] = cart
        flash('Cart updated', 'success')
        return redirect(url_for('cart'))

    @app.route('/checkout', methods=['GET', 'POST'])
    def checkout():
        total, items = _cart_total_and_items()
        if not items:
            flash("Your cart is empty.", "warning")
            return redirect(url_for('home'))
        if request.method == 'POST':
            line_items = []
            for it in items:
                price_in_paise = int(it['product'].price * 100)
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': it['product'].title,
                            'description': it['product'].description or "",
                        },
                        'unit_amount': price_in_paise
                    },
                    'quantity': it['qty']
                })
            session_data = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=url_for('order_success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_for('payment_redirect', _external=True),
            )
            order = Order(stripe_session_id=session_data.id, amount=total)
            db.session.add(order)
            db.session.commit()
            return redirect(session_data.url, code=303)
        return render_template('checkout.html', total=total, items=items, stripe_pk=app.config['STRIPE_PUBLISHABLE_KEY'])

    @app.route('/payment_redirect')
    def payment_redirect():
        return render_template('payment_redirect.html')

    @app.route('/order_success')
    def order_success():
        session_id = request.args.get('session_id')
        try:
            stripe_session = stripe.checkout.Session.retrieve(session_id) if session_id else None
        except Exception:
            stripe_session = None
        session.pop('cart', None)
        return render_template('order_success.html', stripe_session=stripe_session)

    # ---------- Auth ----------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash("User already exists", "danger")
                return redirect(url_for('register'))
            user = User(username=username, email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        return render_template('auth/register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter((User.username == username) | (User.email == username)).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash("Logged in successfully", "success")
                return redirect(url_for('home'))
            flash("Invalid username or password", "danger")
        return render_template('auth/login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash("Logged out successfully", "info")
        return redirect(url_for('home'))

    # ---------- Admin ----------
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, is_admin=True).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            flash("Invalid admin credentials", "danger")
        return render_template('admin/admin_login.html')

    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for('home'))
        products = Product.query.all()
        orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('admin/dashboard.html', products=products, orders=orders)

    @app.route('/admin/products')
    @login_required
    def admin_product_list():
        if not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for('home'))
        products = Product.query.all()
        return render_template('admin/product_list.html', products=products)

    @app.route('/admin/product/new', methods=['GET', 'POST'])
    @login_required
    def admin_product_form():
        if not current_user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for('home'))
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug') or title.lower().replace(' ', '-')
            price = int(request.form.get('price', 0))
            description = request.form.get('description')
            image = request.form.get('image')
            cat_slug = request.form.get('category')
            category = Category.query.filter_by(slug=cat_slug).first()
            if not category:
                category = Category(name=cat_slug.capitalize(), slug=cat_slug)
                db.session.add(category)
                db.session.commit()
            product = Product(title=title, slug=slug, price=price, description=description, image=image, category=category)
            db.session.add(product)
            db.session.commit()
            flash("Product created successfully", "success")
            return redirect(url_for('admin_product_list'))
        categories = Category.query.all()
        return render_template('admin/product_form.html', categories=categories)

    # --- ADMIN: Edit Product ---
    @app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_product(product_id):
        product = Product.query.get_or_404(product_id)
        categories = Category.query.all()

        if request.method == 'POST':
            product.title = request.form['title']
            product.slug = request.form['slug']
            product.price = request.form['price']
            product.description = request.form['description']
            product.category_id = request.form['category_id']

            new_image_path = request.form.get('image', '').strip()
            uploaded_image = request.files.get('image')

            if uploaded_image and uploaded_image.filename != '':
                filename = secure_filename(uploaded_image.filename)
                image_folder = os.path.join('static', 'images', 'products')
                os.makedirs(image_folder, exist_ok=True)
                image_path = os.path.join(image_folder, filename)
                uploaded_image.save(image_path)
                product.image = f'images/products/{filename}'

            elif new_image_path:
                new_image_path = new_image_path.replace('\\', '/').strip()
                if new_image_path.startswith('static/'):
                    new_image_path = new_image_path[len('static/'):]
                if not new_image_path.startswith('images/products/'):
                    filename = os.path.basename(new_image_path)
                    new_image_path = f'images/products/{filename}'
                product.image = new_image_path

            product.is_available = 'is_available' in request.form
            db.session.commit()
            flash('✅ Product updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))

        return render_template('admin/edit_product.html', product=product, categories=categories)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
