from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate
from decouple import config

app = Flask(__name__)

db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_name = config('DB_NAME')
db_port = config('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@localhost:{db_port}/{db_name}'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'

    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    reader_pk = db.Column(db.Integer, db.ForeignKey("readers.pk"))
    reader = db.relationship("ReaderModel")

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = "readers"

    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    books = db.relationship("BookModel", backref="book", lazy="dynamic")


class Books(Resource):
    def get(self):
        books = BookModel.query.all()
        books_data = [b.as_dict() for b in books]
        return {"books": books_data}, 200

    def post(self):
        data = request.get_json()
        book = BookModel(**data)
        db.session.add(book)
        db.session.commit()
        return book.as_dict(), 201


api.add_resource(Books, "/books/")

if __name__ == "__main__":
    app.run(debug=True)
