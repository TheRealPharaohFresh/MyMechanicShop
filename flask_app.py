from app import create_app
from app.models import db
from seed import seed_database

app = create_app('ProductionConfig', testing=False)

with app.app_context():
    db.create_all()
    seed_database()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
