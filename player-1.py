from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Example data
players = [
    {'id': 1, 'name': 'Player 1', 'score': 100},
    {'id': 2, 'name': 'Player 2', 'score': 150},
    {'id': 3, 'name': 'Player 3', 'score': 200}
]

# Request parser
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='Name of the player')
parser.add_argument('score', type=int, help='Score of the player')

# Player resource
class PlayerResource(Resource):
    def get(self, player_id):
        for player in players:
            if player['id'] == player_id:
                return player
        return {'message': 'Player not found'}, 404

    def put(self, player_id):
        args = parser.parse_args()
        for player in players:
            if player['id'] == player_id:
                player['name'] = args['name'] if args['name'] else player['name']
                player['score'] = args['score'] if args['score'] else player['score']
                return player
        return {'message': 'Player not found'}, 404

    def delete(self, player_id):
        for index, player in enumerate(players):
            if player['id'] == player_id:
                deleted_player = players.pop(index)
                return deleted_player
        return {'message': 'Player not found'}, 404

# Players resource
class PlayersResource(Resource):
    def get(self):
        return players

    def post(self):
        args = parser.parse_args()
        player_id = max(player['id'] for player in players) + 1
        new_player = {'id': player_id, 'name': args['name'], 'score': args['score']}
        players.append(new_player)
        return new_player, 201

# API routes
api.add_resource(PlayerResource, '/players/<int:player_id>')
api.add_resource(PlayersResource, '/players')

if __name__ == '__main__':
    app.run(debug=True)
