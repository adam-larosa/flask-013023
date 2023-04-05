
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()



class Game( db.Model, SerializerMixin ):
    __tablename__ = 'games'
    serialize_rules = ( '-reviews.game', )

    id = db.Column( db.Integer, primary_key = True )
    title = db.Column( db.String )
    price = db.Column( db.Float )

    reviews = db.relationship( 'Review', backref='game' )



class Review( db.Model, SerializerMixin ):
    __tablename__ = 'reviews'
    serialize_rules = ( '-game.reviews', '-user.reviews', '-game_id', 
                        '-user_id' )

    id = db.Column( db.Integer, primary_key = True )
    content = db.Column( db.String )

    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    game_id = db.Column( db.Integer, db.ForeignKey( 'games.id' ) )



class User( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    serialize_rules = ( '-reviews.user', )
    
    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    
    reviews = db.relationship( 'Review', backref='user' )

   