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

@app.route('/player/post', methods=['POST'])
def post_player():
    data = request.get_json()
    player = Player(data['username'], data['password'])
    db.session.add(player)
    db.session.commit()
    return jsonify(player_schema.jsonify(player)), 201

@app.route('/player/get', methods=['GET'])
def get_players():
    players = Player.query.all()
    return jsonify(players_schema.jsonify(players))

@app.route('/player/<id>/delete', methods=['DELETE'])
def delete_player(id):
    player = Player.query.filter_by(id=id).first()
    db.session.delete(player)
    db.session.commit()
    return '', 204

@app.route('/player/<id>/update', methods=['PUT'])
def update_player(id):
    data = request.get_json()
    player = Player.query.filter_by(id=id).first()
    player.username = data['username']
    player.password = data['password']
    db.session.commit()
    return jsonify(player_schema.jsonify(player)), 200

if __name__ == '__main__':
    app.run(debug=True)