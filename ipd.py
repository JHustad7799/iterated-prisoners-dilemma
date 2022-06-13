
import random
random.seed(31337)

# increase these symbolic constants when you implement
# the associated Prisoner subclasses
NUM_COOPERATOR = 2
NUM_DEFECTOR = 2
NUM_TITFORTAT = 2
NUM_GRIMTRIGGER = 2
NUM_COINFLIPPER = 2
NUM_DIEROLLER = 2

POINTS_BOTH_COOPERATE = 1
POINTS_BOTH_DEFECT = 0
POINTS_BETRAYER = 2
POINTS_BETRAYED = -1

GAMES_PER_MATCH = 200

def main():
    the_dilemma = Dilemma(POINTS_BOTH_COOPERATE,POINTS_BOTH_DEFECT,POINTS_BETRAYER,POINTS_BETRAYED)

    prisoners = []
    for i in range(NUM_COOPERATOR):
        prisoners.append(Cooperator())
    for i in range(NUM_DEFECTOR):
        prisoners.append(Defector())
    for i in range(NUM_TITFORTAT):
        prisoners.append(TitForTat())
    for i in range(NUM_GRIMTRIGGER):
        prisoners.append(GrimTrigger())
    for i in range(NUM_COINFLIPPER):
        prisoners.append(CoinFlipper())
    for i in range(NUM_DIEROLLER):
        prisoners.append(DieRoller())

    for i in range(len(prisoners)):
        for j in range(i+1,len(prisoners)):
            the_dilemma.play(prisoners[i],prisoners[j],GAMES_PER_MATCH)

    print("\n****RESULTS****")
    for prisoner in sorted(prisoners,reverse=True):
        print(prisoner)

class Prisoner:

    def __init__(self):
        self.points = 0

    def update(self,betrayed,round_points):
        # betrayed indicates if their partner betrayed the player last round. This variable is not used by all classes.
        self.points += round_points

    def match_reset(self):
        pass

    def get_name(self):
        return self.name
        
    def get_points(self):
        return self.points

    def __lt__(self,other):
        return self.points < other.points

    def __ge__(self,other):
        return self.points >= other.points

    def __str__(self):
        return f"{self.name}: {self.points} points"
                   
class Cooperator(Prisoner):
    # Always cooperates
    cooperators_created = 0
    
    def __init__(self):
        super().__init__()
        self.name = f"Cooperator {Cooperator.cooperators_created + 1}"
        Cooperator.cooperators_created += 1

    def play(self):
        return False
        
class Defector(Prisoner):
    # Always defects
    defectors_created = 0

    def __init__(self):
        super().__init__()
        self.name = f"Defector {Defector.defectors_created + 1}"
        Defector.defectors_created += 1

    def play(self):
        return True

class TitForTat(Prisoner):
    # This class cooperates in the first round then does what their opponent did last round.
    titfortats_created = 0
    
    def __init__(self):
        super().__init__()
        self.name = f"Tit For Tat {TitForTat.titfortats_created + 1}"
        TitForTat.titfortats_created += 1

    def match_reset(self):
        self.betrayed_last_round = False

    def update(self,betrayed,round_points):
        super().update(betrayed,round_points)
        self.betrayed_last_round = betrayed

    def play(self):
        return self.betrayed_last_round

class GrimTrigger(Prisoner):
    # This class cooperates until they are betrayed. Once they are betrayed they will always defect.
    grimtriggers_created = 0

    def __init__(self):
        super().__init__()
        self.name = f"Grim Trigger {GrimTrigger.grimtriggers_created + 1}"
        GrimTrigger.grimtriggers_created += 1

    def match_reset(self):
        self.was_betrayed = False

    def update(self,betrayed,round_points):
        super().update(betrayed,round_points)
        if betrayed:
            self.was_betrayed = True
        
    def play(self):
        return self.was_betrayed
        
class CoinFlipper(Prisoner):
    # Theoretically this class cooperates 50 percent of the time and defects the other 50 percent.
    coinflippers_created = 0

    def __init__(self):
        super().__init__()
        self.name = f"Coin Flipper {CoinFlipper.coinflippers_created + 1}"
        CoinFlipper.coinflippers_created += 1

    def play(self):
        if random.random() < 0.5:
            return True
        else:
            return False
        
class DieRoller(Prisoner):
    # Theoretically this class cooperates 1/6th of the time and defects the other 5/6ths.
    dierollers_created = 0

    def __init__(self):
        super().__init__()
        self.name = f"Die Roller {DieRoller.dierollers_created + 1}"
        DieRoller.dierollers_created += 1

    def play(self):
        if random.random() < (1/6):
            return True
        else:
            return False

class Dilemma:

    def __init__(self,both_coop_outcome,both_defect_outcome,betrayer_outcome,betrayed_outcome):
        self.both_coop_outcome = both_coop_outcome
        self.both_defect_outcome = both_defect_outcome
        self.betrayer_outcome = betrayer_outcome
        self.betrayed_outcome = betrayed_outcome

    def play(self,player1,player2,num_games):

        # some Prisoner classes track information from game to game
        # ensure this information is wiped clean at the start of each match
        player1.match_reset()
        player2.match_reset()

        # take note of each player's points at the start of each match
        # so that we can calculate how many points were won/lost by both players
        player1_starting_score = player1.get_points()
        player2_starting_score = player2.get_points()

        for i in range(num_games):
        
            player1_choice = player1.play()
            player2_choice = player2.play()

            # if A defects...
            if player1_choice:
                # ...and so does B
                if player2_choice:
                    player1.update(True,self.both_defect_outcome)
                    player2.update(True,self.both_defect_outcome)
                # ...and player B cooperates
                else:
                    player1.update(False,self.betrayer_outcome)
                    player2.update(True,self.betrayed_outcome)
            # if A cooperates...
            else:
                # ...and B defects
                if player2_choice:
                    player1.update(True,self.betrayed_outcome)
                    player2.update(False,self.betrayer_outcome)
                # ...and so does B
                else:
                    player1.update(False,self.both_coop_outcome)
                    player2.update(False,self.both_coop_outcome)

        # compare the starting scores we noted to the ending scores and print
        # a short description of the outcome
        player1_ending_score = player1.get_points()
        player2_ending_score = player2.get_points()
        change_in_player1_score = player1_ending_score-player1_starting_score
        change_in_player2_score = player2_ending_score-player2_starting_score
        print(f"{player1.get_name()} ({change_in_player1_score}) vs. {player2.get_name()} ({change_in_player2_score})")

if __name__ == "__main__":
    main()
