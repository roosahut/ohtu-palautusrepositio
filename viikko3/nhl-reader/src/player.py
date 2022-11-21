class Player:
    def __init__(self, name, team, goals, assists):
        self.name = name
        self.team = team
        self.goals = goals,
        self.assists = assists
        self.points = goals + assists

    def __str__(self):
        return f'{self.name:20} {self.team} {self.goals[0]} + {self.assists} = {self.points}'
