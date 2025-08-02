from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)

# After this, in terminal run:
# flask db init
# flask db migrate -m "initial schema"
# flask db upgrade