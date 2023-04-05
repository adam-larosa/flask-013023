from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Owner( db.Model ):
    __tablename__ = 'owners'

    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )

    