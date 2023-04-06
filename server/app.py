from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

import ipdb

from models import db, Game, User


app = Flask( __name__ )

app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///meow.db' 
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )

db.init_app( app )

api = Api( app )

@app.errorhandler( NotFound )
def handle_not_found( e ):
    return make_response( { 'error': 'BUY A NEW MAP, YOU ARE LOST!!!' } )



class Users( Resource ):

    def get( self ):
        users = [ user.to_dict() for user in User.query.all() ]
        return make_response( users, 200 )

    def post( self ):
        data = request.get_json()
        new_user = User( name = data[ 'name' ] )
        db.session.add( new_user )
        db.session.commit()
        return make_response( new_user.to_dict(), 201 )        

api.add_resource( Users, '/users' )


class UsersById( Resource ):

    def get( self, id ):
        user = User.query.filter_by( id = id ).first()
        if user == None:
            return make_response( {'error': 'User not found' }, 404 )
        return make_response( user.to_dict(), 200 )

    def patch( self, id ):
        user = User.query.filter_by( id = id ).first()
        if user == None:
            return make_response( {'error': 'User not found' }, 404 )
        data = request.get_json()
        for key in data.keys():
            setattr( user, key, data[key] )
        db.session.add( user )
        db.session.commit()
        return make_response( user.to_dict(), 200 )

    def delete( self, id ):
        user = User.query.filter_by( id = id ).first()
        if user == None:
            return make_response( {'error': 'User not found' }, 404 )
        db.session.delete( user )
        db.session.commit()
        return make_response( user.to_dict(), 200 )


api.add_resource( UsersById, '/users/<int:id>' )




@app.route( '/games', methods = [ 'GET', 'POST' ] )
def games():
    
    if request.method == 'GET':
        game_list = []
        for game in Game.query.all():
            game_dict = {
                "id": game.id,
                "title": game.title,
                "price": game.price   
            }
            game_list.append( game_dict )
        
        response = make_response( game_list, 200 )
        return response

    elif request.method == 'POST':

        data = request.get_json()

        new_game = Game( 
            title = data.get( 'title' ), price = data.get( 'price' ) 
        )
        db.session.add( new_game )
        db.session.commit()
        return make_response( new_game.to_dict(), 201 )




@app.route( '/games/<int:id>', methods = [ 'GET', 'PATCH', 'DELETE'] )
def games_by_id( id ):
    
    game = Game.query.filter( Game.id == id ).first()

    if game == None:
        return make_response( { "error": 'game not found' }, 404 )

    if request.method == 'GET':
        response = make_response( game.to_dict(), 200 )
        return response
    
    


@app.route( '/' )
def index():
    return "<h1>hello meow!!</h1>"


if __name__ == '__main__':
    app.run( port=8000, debug=True )