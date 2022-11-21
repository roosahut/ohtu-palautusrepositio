from player import Player


class PlayerStats:
    def __init__(self, reader):
        self.response = reader.read_players()

    def top_scorers_by_nationality(self, nat):
        players = []

        for player_dict in self.response:
            if player_dict['nationality'] == nat:
                player = Player(
                    player_dict['name'],
                    player_dict['team'],
                    player_dict['goals'],
                    player_dict['assists']
                )
                players.append(player)
        players.sort(key=lambda a: a.points, reverse=True)
        return players
