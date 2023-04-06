from flask import Flask, make_response, request
from flask_migrate import Migrate
import ipdb

from models import db, Game


app = Flask( __name__ )

app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///meow.db' 
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )

db.init_app( app )





@app.route( '/' )
def index():
    return "<h1>hello meow!!</h1>"


@app.route( '/games', methods = [ 'GET', 'POST' ] )
def games():

    if request.method == 'GET':
        games_list = []
        for game in Game.query.all():
            game_dict = {
                "id": game.id,
                "title": game.title,
                "price": game.price
            }
            games_list.append( game_dict )
        
        response = make_response( games_list, 200  )
        
        return response

    elif request.method == 'POST':
        game_info = request.get_json()
        game = Game( 
            title = game_info['title'], price = game_info[ 'price' ] 
        )
        db.session.add( game )
        db.session.commit()
        return make_response( game.to_dict(), 201 )



@app.route( '/games/<int:id>', methods = [ 'GET', 'PATCH', 'DELETE' ] )
def games_by_id( id ):
    
    game = Game.query.filter( Game.id == id ).first()

    if game == None:
        return make_response( { "error": "Game not found" }, 404 )

    if request.method == 'GET':
        response = make_response( game.to_dict(), 200  )
        return response




if __name__ == '__main__':
    app.run( port=8000, debug=True )
