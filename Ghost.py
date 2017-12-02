import copy as copy
from random import randint

class Ghost(object):

    # Constructor
    def __init__(self, state, respawn):
        self.location = respawn
        self.respawn = respawn

    # Calculates and returns the 2D indices of the ghost spawn location
    def caclulateLocation(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 'G':
                    return i, j
        # If it didn't find the location
        print("Could not find ghost spawn point in calculateLocation")
        return None

    # Returns a tuple of the x and y sizes of the state
    def getStateSize(self, state):
        return len(state), len(state[0])

    # Returns variable actions the Ghost has
    def actions(self, state):
        actions = []
        ghostX = self.location[0]
        ghostY = self.location[1]
        stateX = self.getStateSize(state)[0]
        stateY = self.getStateSize(state)[1]
        print(state)
        print("In actions, ghostX: ", ghostX, "; ghostY: ", ghostY)

        # Check up
        if (state[ghostX - 1][ghostY] != '=') and (state[ghostX - 1][ghostY] != '|'):
            print("first: ", state[ghostX - 1][ghostY], "; second: ", state[ghostX - 1][ghostY])
            actions.append("up")
        # Check down
        if (state[ghostX + 1][ghostY] != '=') and (state[ghostX + 1][ghostY] != '|'):
            actions.append("down")
        # Check left
        if (state[ghostX][ghostY - 1] != '|') and (state[ghostX][ghostY - 1] != '='):
            actions.append("left")
        # Check right
        if (state[ghostX][ghostY + 1] != '|') and (state[ghostX][ghostY + 1] != '='):
            actions.append("right")

        return actions

    # Returns the state if an action is taken
    def takeAction(self, state, action):
        newState = copy.deepcopy(state)
        newLoc = None

        # Get location of new position after action is taken
        if action == 'up':
            # check for teloportation
            if state[self.location[0] - 1][self.location[1]] == 't':
                newLoc = (len(state) - 2, self.location[1])
            else:
                newLoc = (self.location[0] - 1, self.location[1])
        elif action == 'down':
            # check for teleportation
            if state[self.location[0] + 1][self.location[1]] == 't':
                newLoc = (1, self.location[1])
            else:
                newLoc = (self.location[0] + 1, self.location[1])
        elif action == 'left':
            # check for telelporation
            if state[self.location[0]][self.location[1] - 1] == 't':
                newLoc = (self.location[0], len(state[0]) - 2)
            else:
                newLoc = (self.location[0], self.location[1] - 1)
        elif action == 'right':
            # check for teleporation
            if state[self.location[0]][self.location[1] + 1] == 't':
                newLoc = (self.location[0], 1)
            else:
                newLoc = (self.location[0], self.location[1] + 1)

        # Update state and location
        #if newState[newLoc[0]][newLoc[1]] != 'G':
        newState[newLoc[0]][newLoc[1]] = 'g'
        #if newState[self.location[0]][self.location[1]] != 'G':
        newState[self.location[0]][self.location[1]] = ' '
        self.location = newLoc
        return newState

    # Causes the ghost to perform a random move every turn
    def randomMove(self, state):
        move = self.actions(state)[randint(0, len(self.actions(state)) - 1)]
        return self.takeAction(state, move)

    # Returns the move that takes Ghost closest to Pacman
    def takeActionShortestDistance(self, state, locOfPacman):
        #Positive means we want to move Right
        xDiff = locOfPacman[1] - self.location[1]
        #Positive means we want to move Down
        yDiff = locOfPacman[0] - self.location[0]

        print("Pacman: ", locOfPacman, "; Ghost: ", self.location, "; xDiff: ", xDiff, "; yDiff: ", yDiff)

        for action in Ghost.actions(self, state):
            print("in for loop")
            print(action)
            if (action == 'up' and yDiff < 0):
                print("Taking short distance action")
                return Ghost.takeAction(self, state, action)
            if (action == 'left' and xDiff < 0):
                print("Taking short distance action")
                return Ghost.takeAction(self, state, action)
            if (action == 'down' and yDiff > 0):
                print("Taking short distance action")
                return Ghost.takeAction(self, state, action)
            if (action == 'right' and xDiff > 0):
                print("Taking short distance action")
                return Ghost.takeAction(self, state, action)
        print("Taking random action in takeActionShortestDistance")
        return Ghost.randomMove(self, state)

    # Helps Intelligent Move in finding the best direction to take to get to Pacman
    def depthLimitedSearch(self, state, locOfPacman, actions, takeAction, depthLimit):
        if self.location == locOfPacman:
            print("bottom of DLS")
            return []

        if depthLimit == 0:
            return "cutoff"

        cutOffOccurred = False
        for action in actions(self, state):
            newState = takeAction(self, state, action)
            result = Ghost.depthLimitedSearch(self, newState, locOfPacman, actions, takeAction, depthLimit-1)
            if result is "cutoff":
                cutOffOccurred = True
            elif result is not "failure":
                result.insert(0, newState)
                return result
        if cutOffOccurred:
            return "cutoff"
        else:
            return "failure"

    # Causes the ghost to scan through the board, making the most intelligent shortest path decision
    def intelligentMove(self, state, locOfPacman, maxDepth=4):
        copyState = copy.deepcopy(state)
        if self.location == locOfPacman:
            return state
        for depth in range(maxDepth):
            result = Ghost.depthLimitedSearch(self, copyState, locOfPacman, Ghost.actions, Ghost.takeAction, depth)
            if result is not "cutoff" and not "failure":
                # Return the state that is the first state added. This is the best next move.
                return result[0]

        # If we get here, this means we were cutoff. Essentially, we couldn't find Pacman within maxDepth moves
        # At this point, we just want to make a move in the direction that Pacman is in
        print("Ghost did not find intelligent move. Running takeActionShortestDistance.")
        return Ghost.takeActionShortestDistance(self, copyState, locOfPacman)