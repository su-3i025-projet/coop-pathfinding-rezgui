class Map:
    def __init__(self, size, obstacles, posPlayers):
        self.rows, self.cols = size
        self.obstacles = obstacles
        self.posPlayers = posPlayers

    def isValid(self, state):
        state_row = state[0]    
        state_col = state[1]

        if (state_row, state_col) not in self.obstacles\
            and state_row >= 0 and state_row < self.rows\
            and state_col >= 0 and state_col < self.cols:
                return True

        return False

    def getPosPlayers(self):
        return self.posPlayers

    def setPosPlayer(self, j, pos):
        self.posPlayers[j] = pos
