
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
    
    @property
    def users( self ):
        return [ r.user for r in self.reviews ]

    def to_dict( self ):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'reviews': [ r.to_dict() for r in self.reviews ],
            'users': [ u.to_dict() for u in self.users ]
        }



class Review( db.Model, SerializerMixin ):
    __tablename__ = 'reviews'
    serialize_rules = ( '-game.reviews', '-user.reviews', '-game_id', 
                        '-user_id' )

    id = db.Column( db.Integer, primary_key = True )
    content = db.Column( db.String )

    user_id = db.Column( db.Integer, db.ForeignKey( 'users.id' ) )
    game_id = db.Column( db.Integer, db.ForeignKey( 'games.id' ) )

    def to_dict( self ):
        return {
            'id': self.id,
            'content': self.content
        }



class User( db.Model, SerializerMixin ):
    __tablename__ = 'users'
    serialize_rules = ( '-reviews.user', )
    
    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String )
    
    reviews = db.relationship( 'Review', backref='user' )

   