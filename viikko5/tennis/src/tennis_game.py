class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        if self.max_points() >= 4:
            return self.high()
        else:
            return self.low()

    def low(self):
        scores = {
            0: "Love",
            1: "Fifteen",
            2: "Thirty",
            3: "Forty",
        }
        if not self.deuce():
            return f'{scores[self.m_score1]}-{scores[self.m_score2]}'
        else:
            return f"{scores[self.m_score1]}-All"

    def high(self):
        if self.deuce():
            return 'Deuce'
        elif self.difference() == 1:
            return f'Advantage {self.current_winner()}'
        else:
            return f'Win for {self.current_winner()}'

    def difference(self):
        return abs(self.m_score1 - self.m_score2)

    def current_winner(self):
        if self.max_points() == self.m_score1:
            return 'player1'
        elif self.max_points() == self.m_score2:
            return 'player2'

    def max_points(self):
        return max(self.m_score1, self.m_score2)

    def deuce(self):
        return self.m_score1 == self.m_score2
