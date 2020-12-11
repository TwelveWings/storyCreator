import random
import sqlite3

from character import Character
from database import Database
from story import Story

class Action:
    """
        An action that is performed in the story.
    """

    ESCAPED = "escaped"
    INVESTIGATED = "investigated"
    RAN = "ran"
    ATTACKED = "attacked"

    def getAction(self, storyState, characters):
        """
            Brief: getAction

            Runs the minimax algorithm to determine the actions that each character will take.

            Param: storyState is the state of the story.
            Param: characters is a list of Character instances.
        """

        # The directions and values pass to the root
        actions = []
        values = []

        # Alpha and Beta initial values
        a = float("-inf")
        b = float("inf")

        for character in characters:
            actions.append([])
            values.append([])

        chosenActions = []

        # Determine the max value using the expectimax algorithm
        storyState.tension = self.getValue(storyState, characters, actions, values, 0, a, b)

        for character in characters:
            actionsAvail = actions[character.ID]
            valuesAvail = values[character.ID]

            if(character.isMonster()):
                chosenActions.append(actionsAvail[valuesAvail.index(max(valuesAvail))])
            else:
                chosenActions.append(actionsAvail[valuesAvail.index(min(valuesAvail))])

        return chosenActions

    def maxValue(self, state, characters, character, actions, values, level, a, b):
        """
          Looks at the successors of the current state and returns the
          maximum value from them. If level 0, creates a list containing
          the highest value from each successor.
        """

        value = float("-inf")

        # For all legal actions, determine the maximum value
        for action in self.getLegalActions(characters, character):
            nextState = self.generateSuccessors(state, characters, character, action)
            value = max(value, self.getValue(nextState, characters, actions, values, level + 1, a, b))

            actions[level].append(action)
            values[level].append(value)

            if(value > b):
                return value

            a = max(a, value)

        return value

    def minValue(self, state, characters, character, actions, values, level, a, b):
        """
          Looks at the successors of the current state and returns the
          maximum value from them. If level 0, creates a list containing
          the highest value from each successor.
        """

        value = float("inf")

        # For all legal actions, determine the minimum value
        for action in self.getLegalActions(characters, character):
            nextState = self.generateSuccessors(state, characters, character, action)

            value = min(value, self.getValue(nextState, characters, actions, values, level + 1, a, b))

            actions[level].append(action)
            values[level].append(value)

            if(value < a):
                return value

            b = min(b, value)

        return value

    def getValue(self, state, characters, actions, values, level, a, b):
        """
          Returns the maximum or minimum value of given states based on if the
          agent is a maximizer (Pacman) or a minimizer (Ghost)
        """

        # If the number of times each agent has acted is equal to the depth, we have
        # found the terminal node and should stop the algorithm.
        if(len(characters) == level):
            return state.tension

        # If the level is divisible by the number of agents, the agent is Pacman.
        # Otherwise, the agent is a ghost.
        if(characters[level].isMonster()):
            return self.maxValue(state, characters, characters[level], actions, values, level, a, b)
        else:
            return self.minValue(state, characters, characters[level], actions, values, level, a, b)

    def getLegalActions(self, characters, character):
        actions = [Action.INVESTIGATED]

        if(self.isConflict(characters, character) and character.aware):
            if(character.isHuman()):
                actions = [Action.ATTACKED, Action.INVESTIGATED, Action.RAN]
            elif(character.isMonster() and character.isInjured()):
                actions = [Action.ATTACKED, Action.RAN]
            else:
                actions = [Action.ATTACKED]
        elif(character.aware):
            if(character.isHuman()):
                actions = [Action.ESCAPED, Action.INVESTIGATED, Action.RAN]
            elif(character.isMonster() and character.isInjured()):
                actions = [Action.INVESTIGATED, Action.RAN]

        return actions

    def isConflict(self, characters, character):
        humansInPosition = 0
        monstersInPosition = 0

        for c in characters:
            if(c.ID == character.ID):
                continue
            elif(c.isHuman() and c.position == character.position):
                humansInPosition += 1
            elif(c.isMonster() and c.position == character.position):
                monstersInPosition += 1

        if((character.isMonster() and humansInPosition > 0)
           or (character.isHuman() and monstersInPosition > 0)):
            return True
        else:
            return False


    def generateSuccessors(self, state, characters, character, action):
        nextState = state

        dataConnection = Database()

        if(character.isMonster()):
            tensionModifier = 1 - dataConnection.getActionUsage(action, character.characterType)
        else:
            tensionModifier = 1 + dataConnection.getActionUsage(action, character.characterType)

        if(action == Action.ESCAPED):
            nextState = Story((state.tension - 1) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
        elif(action == Action.INVESTIGATED):
            if(self.isConflict(characters, character) and character.aware):
                nextState = Story((state.tension + 3) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
            elif(self.isConflict(characters, character)):
                nextState = Story((state.tension + 2) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
            else:
                nextState = Story((state.tension + 1) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
        elif(action == Action.RAN):
            if(character.isHuman() and self.isConflict(characters, character) and character.aware):
                nextState = Story((state.tension + 4) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
            elif(character.isMonster() and character.isInjured() and self.isConflict(characters, character) and character.aware):
                nextState = Story((state.tension - 1) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
        elif(action == Action.ATTACKED):
            if(character.isHuman() and self.isConflict(characters, character) and character.aware):
                nextState = Story((state.tension + 5) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)
            elif(character.isMonster() and character.isInjured() and self.isConflict(characters, character) and character.aware):
                nextState = Story((state.tension + 2) * tensionModifier, state.numHumans, state.numMonsters, state.numHumansDead, state.numEscaped, state.numMonstersDead, state.storyComplete)

        return nextState
