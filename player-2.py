from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<Player %r>' % self.username
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

        db.session.add(self)
        db.session.commit()

class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')
        model = Player
        load_instance = True
        dump_instance = True

player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)

@app.route('/player/post', methods=['POST'])
def post_player():
    data = request.get_json()
    username = data['username']
    password = data['password']
    player = Player(username, password)
    db.session.add(player)
    db.session.commit()
    return player_schema.jsonify(player)

@app.route('/player/get', methods=['GET'])
def get_players():
    players = Player.query.all()
    return players_schema.jsonify(players)

@app.route('/player/delete/<int:id player>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    db.session.delete(player)
    db.session.commit()
    return player_schema.jsonify(player)

@app.route('/player/update/<int:id player>', methods=['PUT'])
def update_player(id):
    data = request.get_json()
    player = Player.query.get(id)
    player.username = data['username']
    player.password = data['password']
    db.session.commit()
    return player_schema.jsonify(player)

if __name__ == '__main__':
    app.run(debug=True)