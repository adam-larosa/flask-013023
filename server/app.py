from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Game


app = Flask( __name__ )

app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///meow.db' 
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )

db.init_app( app )





@app.route( '/' )
def index():
    return "<h1>hello meow!!</h1>"


@app.route( '/games' )
def games():
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



@app.route( '/games/<int:id>' )
def games_by_id( id ):
    
    game = Game.query.filter( Game.id == id ).first()

    response = make_response( game.to_dict(), 200  )
    
    return response





if __name__ == '__main__':
    app.run( port=8000, debug=True )