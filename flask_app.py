from app import create_app
from app.models import db
from sqlalchemy import text

app = create_app('ProductionConfig')

with app.app_context():
    # Disable foreign key checks using a raw connection and commit right after
    # db.session.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    # db.session.commit()  # <--- make sure this commits before dropping

    # db.drop_all()

    # db.session.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
    # db.session.commit()

    # # Optional: recreate tables
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
