import sqlite3

from character import CharacterType
from story import Story

class Database:
    """
        Connection to the database file.
    """
    def createDBAndTables(self):
        """
            Brief: createDBAndTables

            Creates two tables (if they do not already exist) to store the
            amount of times an outcomes has occurred.
        """
        conn = self.openConnection()

        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS action_likelihood 
                     (action VARCHAR(100) PRIMARY KEY,
                     times_used INT DEFAULT 0,
                     percentage DOUBLE DEFAULT 0,
                     UNIQUE(action));
            ''') 

        c.execute('''CREATE TABLE IF NOT EXISTS story_outcomes 
                     (winner VARCHAR(10) PRIMARY KEY,
                     times_won INT DEFAULT 0,
                     UNIQUE(winner));
            ''')    

        self.closeConnection(conn)

    def insertRecords(self):
        """
            Brief: insertRecords

            Inserts records into the two tables created (unless the rows have already been
            inserted).
        """
        conn = self.openConnection()

        c = conn.cursor()

        c.execute('''INSERT OR IGNORE INTO action_likelihood (action, times_used, percentage)
                     VALUES ('escaped', 0, 0);''')

        c.execute('''INSERT OR IGNORE INTO action_likelihood (action, times_used, percentage)
                     VALUES ('investigated', 0, 0);''')

        c.execute('''INSERT OR IGNORE INTO action_likelihood (action, times_used, percentage)
                     VALUES ('ran', 0, 0);''')

        c.execute('''INSERT OR IGNORE INTO action_likelihood (action, times_used, percentage)
                     VALUES ('attacked', 0, 0);''')

        c.execute('''INSERT OR IGNORE INTO story_outcomes (winner, times_won)
                     VALUES ('monster', 0);''')
 
        c.execute('''INSERT OR IGNORE INTO story_outcomes (winner, times_won)
                     VALUES ('human', 0);''')

        self.closeConnection(conn)

    def determinePercent(self, action):
        """
            Brief: determinePercent

            Finds the percentage of times an action has been used.

            Param: action is the action that is being referenced.

            Returns the percentage.
        """
        conn = self.openConnection()

        c = conn.cursor()

        c.execute('''SELECT *
                     FROM [action_likelihood];''')

        actionTotal = 0
        allActionTotal = 0

        for row in c.fetchall():   
            if(row[1] > 0):
                allActionTotal += row[1]
                if(row[0] == action):
                    actionTotal = row[1]

        if(allActionTotal > 0):
            percent = actionTotal / float(allActionTotal)
        else:
            percent = 0.0

        self.closeConnection(conn)

        return percent

    def updateAction(self, action):
        """
            Brief: updateAction

            Updates the amount of times an action has been used and its percentage.

            Param: action is the action being referenced.
        """
        conn = self.openConnection()

        c = conn.cursor()

        c.execute('''UPDATE [action_likelihood]
                     SET [times_used] = [times_used] + 1
                     WHERE [action] = ?''', (action,))

        c.execute('''UPDATE [action_likelihood]
                     SET [percentage] = ?
                     WHERE [action] = ?''', (self.determinePercent(action), action))

        self.closeConnection(conn)

    def updateOutcome(self, storyState):
        """
            Brief: updateOutcome

            Updates the 'winner' of the story. This is used for reference and to observe
            the results of all the outcomes.

            Param: storyState is the state of the story.
        """
        conn = self.openConnection()

        c = conn.cursor()

        if(storyState.numHumansDead == storyState.numHumans):
            winner = CharacterType.MONSTER
        else:
            winner = CharacterType.HUMAN

        c.execute('''UPDATE [story_outcomes]
                     SET [times_won] = [times_won] + 1
                     WHERE [winner] = ?''', (winner,))

        self.closeConnection(conn)
 
    def closeConnection(self, conn):
        """
            Brief: closeConnection

            Closes the connection to the database.

            Param: conn is the connection to the database.
        """
        conn.commit()
        conn.close()

    def openConnection(self):
        """
            Brief: openConnection

            Opens the connection to the database.

            Returns the connection to the database.
        """
        conn = sqlite3.connect("outcomes.db")

        return conn

    def getActionUsage(self, action):
        """
            Brief: getActionUsage

            Gets the percentage of times an action has been used.

            Param: action is the action being referenced.

            Returns the percentage.
        """
        conn = self.openConnection()

        c = conn.cursor()

        t = (action,)

        c.execute('''SELECT [percentage]
                 FROM [action_likelihood]
                 WHERE [action] = ?''', t)

        percentage = c.fetchone()[0]


        self.closeConnection(conn)

        return percentage

    def getOutcomes(self):
        """
            Brief: getOutcomes

            Prints out the outcomes of the each story.
        """
        conn = self.openConnection()

        c = conn.cursor()

        c.execute('''SELECT *
                     FROM  [story_outcomes];''')

        outcomes = c.fetchall()

        print("\n\n")

        for outcome in outcomes:
            print("%s: %s" % (outcome[0], outcome[1]))
