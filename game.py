import ai
import copy
import random

class Engine:
    """Game engine. Maintains board state and returns it for rendering"""
    def __init__(self, depth=2):
        self.depth = depth
        self.state = [[0 for i in range(4)] for j in range(4)]
        self.machine_turn = True

    def get_next(self):
        opens = openTiles(self.state)
      
        if self.machine_turn:
            if len(opens) == 0:
                pass
            square = random.choice(openTiles(self.state))
            value = 2 if random.random() < 0.9 else 4
            self.state = result(self.state, ("place", square, value))
        else:
            if gameover(self.state):
                return None
            # print("pre-action", self.state)
            action = nextAction(self.state, self.depth)
            # print("old", self.state)
            self.state = result(self.state, action)
            # print(action, "new", self.state)
        self.machine_turn = not self.machine_turn
        return self.state
        
    def get_state(self):
        return self.state

def gameover(state):
    return len(playerActions(state)) == 0

def score(state):
    return max(score_bottom_right(state), score_bottom_right(transpose(state))) 

def score_bottom_right(state):
    positional = positional_scoring(state)
    # neighbors = neighbor_scoring(state)
    # network = network_scoring(state)
    return positional


def positional_scoring(state):
    """Give position points to squares that follow a snake"""
    total = 0
    power = 1
    # row 0
    for i in range(3, -1, -1):
        total += 2 ** power * state[0][i]
        power += 1
    # row 1
    for i in range(4):
        total += 2 ** power * state[1][i]
        power += 1
    # row 2
    for i in range(3, -1, -1):
        total += 2 ** power * state[2][i]
        power += 1
    # row 3
    for i in range(4):
        total += 2 ** power * state[3][i]
        power += 1
    return total

def neighbor_scoring(state):
    """return some of tiles whose neighbor is equal to half their value"""
    count = 0
    for row in range(4):
        for col in range(4):
            score = state[row][col]
            nbr_found = False
            for row_offset in [-1, 1]:
                r_index = row + row_offset
                if r_index in range(4):
                    if state[r_index][col] == score / 2 and not nbr_found:
                        count += score ** 2
                        nbr_found = True

            for col_offset in [-1, 1]:
                c_index = col + col_offset
                if c_index in range(4):
                    if state[row][c_index] == score / 2 and not nbr_found:
                        count += score ** 2
                        nbr_found = True

    return count

def network_scoring(state):
    """Score based on manhattan distances between consecutive blocks"""
    weighted_distance = 0
    squares = []
    for row in range(4):
        for col in range(4):
            if state[row][col] != 0:
                squares.append((state[row][col], (row, col)))
    ordered = sorted(squares, key=lambda x: x[0])
    for i in range(len(ordered) - 1):
        first_coords = ordered[i][1]
        second_coords = ordered[i + 1][1]
        weighted_distance += ordered[i][0] * (
            abs(first_coords[0] - second_coords[0]) + 
            abs(first_coords[1] - second_coords[1]))
    return weighted_distance


def playerActions(state):
    actions = []
    for direction in ["up", "down", "left", "right"]:
        action = ("shift", direction)
        newstate = result(state, action)
        if newstate != state:
            actions.append(action)
    return actions

def openTiles(state):
    tiles = []
    for x in range(len(state)):
        for y in range(len(state[x])):
            if state[x][y] == 0:
                tiles.append((x,y))
    return tiles

def gameActions(state):
    actions = []
    for tile in openTiles(state):
        place2 = ("place", tile, 2)
        place4 = ("place", tile, 4)
        actions.append((place2, 0.9))
        actions.append((place4, 0.1))
    return actions

def result(state, action):
    if action[0] is "place":
        x, y = action[1]
        newstate = copy.deepcopy(state)
        newstate[x][y] = action[2]
        return newstate
    elif action[0] is "shift":
        return shift(state, action[1])
    else:
        raise Exception("Received illegal action: " + action)

def nextAction(state, depth):
    return ai.expectimax(state, gameover, score, playerActions, gameActions, result, depth)
    # return ("shift", "right")


def collapse_list(items):
    """given a list of 4 elements, collapses them towards the 0 index"""
    blocker = -1 #to prevent double collapses
    new_items = items[:]
    for index in range(1, 4):
        if new_items[index] == 0:
            continue
        cell = index
        for target in range(index - 1, blocker, -1):
            if new_items[target] == new_items[cell]:
                new_items[target] = 2 * new_items[target]
                blocker = target
                new_items[cell] = 0
                break
            elif new_items[target] == 0:
                new_items[target] = new_items[cell]
                new_items[cell] = 0
                cell = target
            else:
                break
    return new_items


def transpose(matrix):
    """Swap rows and cols"""
    new_mat = [[0]*4 for i in range(4)]
    for col in range(len(matrix)):
        for row in range(len(matrix)):
            new_mat[col][row] = matrix[row][col]
    return new_mat


def vertical_shift(state, shift_down):
    """Does a shift on the state object
    if shift_down, shifts down, else shifts up"""
    transposed = transpose(state)
    new_mat = horizontal_shift(transposed, shift_down)
    return transpose(new_mat)
    

def horizontal_shift(state, shift_right):
    """Shift the state object right or left, collapsing tiles"""
    new_mat = []
    for row in state:
        new = row[:]
        if shift_right:
            new.reverse()
        collapsed = collapse_list(new)
        if shift_right:
            collapsed.reverse()
        new_mat.append(collapsed)

    return new_mat



def shift(state, direction):
    if direction in ["up", "down"]:
        result = vertical_shift(state, direction == "down") 
    elif direction in ["left", "right"]:
        result = horizontal_shift(state, direction == "right")
    else:
        raise Exception("Recieved illegal direction")
    return result

    
