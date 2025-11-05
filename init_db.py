from app import create_app
from models import db
from werkzeug.security import generate_password_hash
from models import User

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")

    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        from models import User
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created (username: admin, password: admin123)")
