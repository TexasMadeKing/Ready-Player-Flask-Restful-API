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

    def __init__(self, username, password):
        self.username = username
        self.password = password


class PlayerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


@app.route('/player', methods=['POST'])
def post_player():
    player_data = request.get_json()
    player = Player(username=player_data['username'], password=player_data['password'])
    db.session.add(player)
    db.session.commit()
    return player_schema.jsonify(player), 201


@app.route('/player', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify(players_schema.dump(players))


@app.route('/player/<int:id>', methods=['DELETE'])
def delete_player(id):
    player = Player.query.get(id)
    if player:
        db.session.delete(player)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Player not found'}), 404


@app.route('/player/<int:id>', methods=['PUT'])
def update_player(id):
    player = Player.query.get(id)
    if player:
        data = request.get_json()
        player.username = data.get('username', player.username)
        player.password = data.get('password', player.password)
        db.session.commit()
        return player_schema.jsonify(player), 200
    else:
        return jsonify({'error': 'Player not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
