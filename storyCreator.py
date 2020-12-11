import random
import sys

from action import Action
from character import CharacterHealth, CharacterType, Gender, SubjectAdjective, Character
from database import Database
from story import Story    

def determineGender():
    """
        Brief: determineGender

        Randomly select a gender for a character.

        Returns the selected gender.
    """
    randomizer = random.randint(1,2)

    if(randomizer == 1):
        return Gender.MALE
    else:
        return Gender.FEMALE

def determineCharacterType():
    """
        Brief: determineCharacterType

        Randomly select a character type (monster or human) for a character.

        Returns the selected character type.
    """
    randomizer = random.randint(1,2)

    if(randomizer == 1):
        return CharacterType.HUMAN
    else:
        return CharacterType.MONSTER

def loadCharacters(fileName, storyState):
    """
        Brief: loadCharacters

        Read from a specified text file, containing names of characters, and
        generate a Character instance for each one. Character information
        like character type, gender, description and position they enter the 
        story world is randomly generated. Saves the characters to a list.

        Param: fileName is the name of the file
        Param: storyState is the state of the story

        Returns a list of Character instances called characters.
    """
    characters = []
    charactersInList = []

    f = open(fileName,  'r+')

    for line in f:
        characters.append(line[:-1].split(' '))

    ID = 0
    for character in characters:
        characterAdded = Character(ID, character[0], determineCharacterType(), 
                                   determineGender(), selectDescription(1), 
                                   True, CharacterHealth.HEALTHY, 0, 
                                   random.randint(1,4), False)

        charactersInList.append(characterAdded)

        if(characterAdded.isHuman()):
            storyState.numHumans += 1
        elif(characterAdded.isMonster()):
            storyState.numMonsters += 1

        ID += 1

    if(storyState.numHumans == 0):
        charactersInList.append(Character(ID, "The Human", CharacterType.HUMAN, 
                                determineGender(), selectDescription(1), 
                                True, CharacterHealth.HEALTHY, 0, 
                                random.randint(1,4), False))

        storyState.numHumans += 1
    elif(storyState.numMonsters == 0):
        charactersInList.append(Character(ID, "The Monster", CharacterType.MONSTER, 
                                determineGender(), selectDescription(1), 
                                True, CharacterHealth.HEALTHY, 0, 
                                random.randint(1,4), False))

        storyState.numMonsters += 1

    f.close()

    return charactersInList

def introduceWorld(storyState, characters):
    """
        Brief: introduceWorld

        Checks to see the number of monsters and humans, and returns a simple
        introduction to the storySequence list.

        Param: characters is a list of Character instances.

        Returns a list containing the introductory text of the story sequence.
    """
    storySequence = []

    storySequence.append("In this world there are monsters and humans.")

    if(storyState.numHumans == 1):
        storySequence.append(" A human must find " + str(storyState.numMonsters) + 
                             " monsters, and destroy them.")
    elif(storyState.numMonsters == 1):
        storySequence.append(" The humans must find the monster, and destroy it.")
    else:
        storySequence.append(" The " + str(storyState.numHumans) + 
                             " humans must find the " + str(storyState.numMonsters) + 
                             " monsters, and destroy them.")

    return storySequence

def introduceCharacters(characters):
    """
        Brief: introduceCharacters

        Checks to see t-he number of monsters and humans, and returns a list 
        containing a sentence for each character, describing them using the 
        randomly generated descriptions.

        Param: characters is a list of Character instances

        Returns a list containing the introductory text of the story sequence.
    """
    storySequence = []

    for character in characters:
        storySequence.append(character.name + " was a " + character.appearance + 
                             " " + character.characterType + ".")

    return storySequence

def concludeStory(storyState, characters):
    """
        Brief: concludeStory

        Saves the results of the story to the storySequence list.

        Param: storyState is the state of the story.
        Param: characters is the list of Character instances.

        Returns a list contaiing the conclusion of the story.
    """
    storySequence = []

    storySequence.append("\n\n")

    storySequence.append("Thus, the story ends.")

    if(storyState.numMonsters == storyState.numMonstersDead and storyState.numMonsters > 1):
        storySequence.append("The monsters were defeated.")
    elif(storyState.numMonsters == storyState.numMonstersDead):
        storySequence.append("The monsters was defeated.")
    else:
        storySequence.append("The humans had failed to defeat the monsters.")

    for character in characters:
        if(character.alive):
            storySequence.append(character.name + " survived.")
        elif(character.position == -1):
            storySequence.append(character.name + " escaped.")
        else:
            storySequence.append(character.name + " died.")

    return storySequence

def printSequence(storySequence):
    """
        Brief: printSequence

        Print the story sequence

        Param: storySequence is a list containing the introductions and 
        action strings performed by each characters.
    """
    storyString = ""

    for sequence in storySequence:
        if(storyString == ""):
            storyString = sequence
        else:
            storyString = storyString + " " + sequence

    print(storyString)    
    
def selectDescription(descriptionType):
    """
        Brief: selectDescription

        Select a description for the character.

        Param: descriptionType is used to differentiate between a description 
        for a character themselves, an action, and other features of the 
        character.

        Returns an adjective or adverb.
    """
    if(descriptionType == 1):
        words = [SubjectAdjective.ATTRACTIVE, SubjectAdjective.BEAUTIFUL,
		 SubjectAdjective.FETCHING, SubjectAdjective.GROTESQUE,
		 SubjectAdjective.HANDSOME, SubjectAdjective.HIDEOUS,
		 SubjectAdjective.PRETTY, SubjectAdjective.TERRIBLE,
		 SubjectAdjective.UGLY, SubjectAdjective.VILE]
	
	randomizer = random.randint(0, len(words) - 1)

        return words[randomizer]

def actionOutcome(storyState, characters, character, action):
    """
        Brief: actionOutcome

        Updates the storyState and character information based on the given action.

        Param: storyState is the state of the story
        Param: characters is a list of Character instances
        Param: character is the particular character performing the action.
        Param: action is the action that is being processed.

        Returns a string detailing the action performed and their results.
    """
    actionString = character.name + " " + action + " "
    if(action == Action.ATTACKED):
        randomizer = random.randint(1,100)

        if(isConflict(characters, character)):
            for otherCharacter in characters:
                if(otherCharacter.ID == character.ID 
                   or not otherCharacter.alive):
                    continue
                elif(character.isHuman() and otherCharacter.isMonster() 
                     and randomizer < 31):
                    storyState.numMonstersDead += 1
                    otherCharacter.alive = False
                    actionString += "the monster, " + otherCharacter.name + ", killing it. "
                    break
                elif(character.isHuman() and otherCharacter.isMonster() 
                     and randomizer > 30):
                    actionString += "the monster, " + otherCharacter.name + ", but failed to kill it. "
                    break
                elif(character.isMonster() and otherCharacter.isHuman()
                     and randomizer > 30):
                    storyState.numHumansDead += 1
                    otherCharacter.alive = False

                    if(otherCharacter.gender == Gender.MALE):
                        actionString = character.name + " " + action + " " + otherCharacter.name + ", killing him. "
                    else:
                        actionString = character.name + " " + action + " " + otherCharacter.name + ", killing her. "
                    break
                elif(character.isMonster() and otherCharacter.isHuman()
                     and character.alive and randomizer < 31):
                    if(otherCharacter.gender == Gender.MALE):
                        actionString += otherCharacter.name + ", but he managed to get away. "
                    else:
                        actionString += otherCharacter.name + ", but she managed to get away. "
                    break

    elif(action == Action.ESCAPED):
        randomizer = random.randint(1,100)

        if(randomizer < 11):
            character.position = -1
            storyState.numEscaped += 1
            actionString += "from the monsters' domain. "
        else:
            actionString = character.name + " attempted to escape from the monster' domain, but failed. "
    elif(action == Action.INVESTIGATED):
        randomizer = random.randint(1,3)
        findRandomizer = random.randint(1,2)

        if(randomizer == 1 and (character.position > 1 and character.position < 4)): 
            character.position -= 1
        elif(randomizer == 2 and (character.position > 1 and character.position < 4)): 
            character.position += 1
        elif(randomizer == 3):
            character.position = character.position
        elif(character.position == 1): 
            character.position = 2
        elif(character.position == 4): 
            character.position = 3

        if(findRandomizer == 1 and isConflict(characters, character)):
            character.aware = True
        
            for otherCharacter in characters:
                if(character.isHuman() and otherCharacter.isMonster()):
                    actionString += "finding the monster, " + otherCharacter.name + ". "
                    break
                elif(character.isMonster() and otherCharacter.isHuman()):
                    actionString = " The monster, " + character.name + ", " + action + " finding " + otherCharacter.name + ". "
        elif(findRandomizer > 1 or not isConflict(characters, character)):
            actionString += "finding nothing."
    elif(action == Action.RAN):
        randomizer = random.randint(1,2)

        if(randomizer == 1 and character.position > 2):
            character.position -= 2
        elif(randomizer == 2 and character.position < 3):
           character.position += 2

        if(character.isHuman()):
            actionString += "fleeing in terror. "
        else:
            actionString += "fleeing to tend to its wounds. "

    return actionString


def isConflict(characters, character):
    """
        Brief: isConflict

        Checks to see if the position the character is currently in is occupied
        by the opposite character type.

        Param: characters is a list of Character instances
        Param: character is the particular character being used as a reference.

        Returns a boolean based on whether or not there is a  conflict or not.
    """
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

if __name__ == '__main__':
    storyState = Story(0.0, 0, 0, 0, 0, 0, False)

    characters = loadCharacters(sys.argv[1], storyState)

    # Create DB and Table that will be used to store outcomes
    dataConnection = Database()

    dataConnection.createDBAndTables()
    dataConnection.insertRecords()

    storySequence = []

    # Introduce world
    storySequence = introduceWorld(storyState, characters)

    storySequence.append("\n\n")

    printSequence(storySequence)

    # Introduce characters to the story.
    storySequence = introduceCharacters(characters)

    printSequence(storySequence)

    storySequence = []

    # Characters act building tension
    while(not storyState.storyComplete):
        storySequence.append("\n\n")

        a = Action()

        characterActions = a.getAction(storyState, characters)

        for i in range(len(characterActions)):
            if(characterActions[i] == Action.ATTACKED 
               and not isConflict(characters, characters[i])):
                continue
            elif(characters[i].alive
                 and characters[i].position > -1):
                storySequence.append(actionOutcome(storyState, characters, characters[i], characterActions[i]))

                # Store results to database to determine the likelihood of actions
                dataConnection.updateAction(characterActions[i], characters[i].characterType)

            if((storyState.numHumansDead + storyState.numEscaped) == storyState.numHumans 
                or storyState.numMonstersDead == storyState.numMonsters):
                storyState.storyComplete = True
                break

        printSequence(storySequence)

        storySequence = []

    # Story concludes
    storySequence = concludeStory(storyState, characters)

    printSequence(storySequence)

    dataConnection.updateOutcome(storyState)
    dataConnection.getOutcomes()
    print("ATTACK: %s" % dataConnection.getActionUsage("attacked", "human"))
    print("ESCAPE: %s" % dataConnection.getActionUsage("escaped", "human"))
    print("INVESTIGATE: %s" % dataConnection.getActionUsage("investigated", "human"))
    print("RAN: %s" % dataConnection.getActionUsage("ran", "human"))
