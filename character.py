class CharacterHealth:
    """
        Status of a character.
    """
    HEALTHY = "healthy"
    INJURED = "injured"
    DEAD = "dead"

class Gender:
    """
        Gender of a character.
    """
    MALE = 1
    FEMALE = 2

class CharacterType:
    """
        Character type of a character.
    """

    HUMAN = "human"
    MONSTER = "monster"
  
class SubjectAdjective:
    """
        Adjectives to describe the characters.
    """
    ATTRACTIVE = "attractive"
    BEAUTIFUL = "beautiful"
    FETCHING = "fetching"  
    GROTESQUE = "grotesque"
    HANDSOME = "handsome"
    HIDEOUS = "hideous"
    PRETTY = "pretty"
    TERRIBLE = "terrible"
    UGLY = "ugly"
    VILE = "vile"


class Character:
    """
        Character in the story.
    """
    def __init__(self, ID, name, characterType, gender, appearance, alive, status, timesMoved, position, aware):
        self.ID = ID
        self.name = name
        self.characterType = characterType
        self.gender = gender
        self.appearance = appearance
        self.alive = alive
        self.status = status
        self.timesMoved = timesMoved
        self.position = position
        self.aware = aware

    def isHuman(self):
        """
            Brief: isHuman

            Checks to see if the character is a human.

            Returns a boolean based on whether or not the character is a human.
        """
        return self.characterType == CharacterType.HUMAN

    def isMonster(self):
        """
            Brief: isMonster

            Checks to see if the character is a monster.

            Returns a boolean based on whether or not the character is a monster.
        """
        return self.characterType == CharacterType.MONSTER

    def isHealthy(self):
        """
            Brief: isHealthy

            Checks to see if the character is healthy.

            Returns a boolean based on whether or not the character is healthy.
        """
        return self.status == CharacterHealth.HEALTHY

    def isInjured(self):
        """
            Brief: isInjured

            Checks to see if the character is injured.

            Returns a boolean based on whether or not the character is injured.
        """
        return self.status == CharacterHealth.INJURED

    def isDead(self):
        """
            Brief: isDead

            Checks to see if the character is dead.

            Returns a boolean based on whether or not the character is dead.
        """
        return self.status == CharacterHealth.DEAD
