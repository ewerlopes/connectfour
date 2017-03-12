from enum import Enum
import requests


class GameStatus(Enum):
    WAITING = 'WAITING'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'


class MasterServer:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def _call(self, method, resource, params=None, json=None):
        url = self.endpoint + resource

        response = requests.request(method, url, params=params, json=json)

        response.raise_for_status()

        return response.json()

    def get_games(self, version):
        params = {
            'version': version
        }

        return self._call('GET', 'games', params=params)

    def create_game(self, name, version):
        json = {
            'name': name,
            'version': version
        }

        return self._call('POST', 'games', json=json)

    def get_game(self, id):
        return self._call('GET', 'games/{}'.format(id))

    def update_game(self, id, token, status=None, name=None, version=None, winner=None):
        json = {
            'token': token
        }

        if status:
            json['status'] = status

        if name:
            json['name'] = name

        if version:
            json['version'] = version

        if winner:
            json['winner'] = winner

        return self._call('PUT', 'games/{}'.format(id), json=json)

    def delete_game(self, id, token):
        json = {
            'token': token
        }

        return self._call('DELETE', 'games/{}'.format(id), json=json)
