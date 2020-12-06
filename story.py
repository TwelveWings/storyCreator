class Story:
    """
        The story state
    """
    def __init__(self, tension, numHumans, numMonsters, numHumansDead, numEscaped, numMonstersDead, storyComplete):
        self.tension = tension
        self.numHumans = numHumans
        self.numMonsters = numMonsters
        self.numHumansDead = numHumansDead
        self.numEscaped = numEscaped
        self.numMonstersDead = numMonstersDead
        self.storyComplete = storyComplete
