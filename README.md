# Ready Set Bet - Simulator & Analysis

Ready Set Bet is a board game about horse racing.  The horses advance down the track based on dice rolls.  Players bet on which horses will win, place, or show.  The player whose wins the most money after four rounds is the winner.  The code in this repo run simulations of the game -- either from the beginning or from an intermediate state -- to determine what the best bets are to make.  For more information on the game itself, check out:

https://boardgamegeek.com/boardgame/351040/ready-set-bet

https://alderacstore.com/ready-set-bet/


## Installation

Installation on Linux:

```
git clone <repo name>
cd <repo name>
python -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Use

### Simulator

To try out the simulator, run 
```
jupyter notebook 
```
to launch a jupyter notebook session in your browser. Then, navigate to `notebooks` in your jupyter session and open `ReadySetBet_get_best_bets.ipynb`.  Finally, execute the cells to run a target simulation, pause it, and then run 1000 forward simulations of what might happen in the rest of the game.  Running subsequent cells will tell tell you the expected value of each bet, so you can pick the best one!


### Visualizing a Game

f you want to see what a game looks like, you can set `VISUALIZE = True`.  But visualization takes to long to simulate all 1000 games, so set `VISUALIZE = False` for performing the full set of simulations.  Alternatively, try just adding a new cell in the notebook that looks like this:

```python
seed(8) # change the seed to see a different game 
game = ReadySetBetGame()
game.play_game(visualize=True, time_step=0.5)
```
Then you watch a game play out.

### Example

Here's how a game looks:


```python
Step:20 Roll: 12
      ___________________________________________________
      |  |  |  |  |  |  |  |  |  |  |R |  |  |  |  |FINISH
2/3   ------2/                                     |
4     ---4                                         |
5     ---------------5                             |
6     6                                            |
7     ------------7                                |
8     ---8                                         |
9     ---------------9                             |
10    10                                           |
11/12 ------------11                               |
      |  |  |  |  |  |  |  |  |  |  |R |  |  |  |  |FINISH
      ___________________________________________________
```
In this game the 9 and 5 horses are tied for the lead and the 7 and 11/12 horses are tied for third.  Who should you bet on in this scenario?

Here are the top 10 best bets to make given the current state of the race, based on expected value:

```python
('5.showed.0', 3.996)
('9.showed.0', 3.936)
('9.placed.0', 3.236)
('9.won.0', 3.21)
('5.placed.0', 3.137)
('5.won.0', 3.03)
('5.showed.1', 2.994)
('9.showed.1', 2.904)
('9.won.1', 2.568)
('11/12.showed.0', 2.505)
```

Based on thi sanalysis, the best two bets are on on 5 and 9 to show (i.e. finish top 3).  That might be surprising as some players might put their money on those two to win or place (i.e. finish top 2).

Have fun!


## Analysis

To run the analysis of which horse wins and how often, use the ReadySetBet_get_placement_frequeny.ipynb notebook.  Or, if you just want to see the results, go to images, where you can see the placement frequencies based on N = 1000 simulations.  

Here are the speed/movement averages for each horse:


```
Average rolls per game 64.4

Average spaces moved per roll:
{
    "2/3": 0.102,
    "4": 0.101,
    "5": 0.131,
    "6": 0.156,
    "7": 0.168,
    "8": 0.153,
    "9": 0.134,
    "10": 0.106,
    "11/12": 0.1
}

Average spaces moved per game:
{
    "2/3": 6.6,
    "4": 6.5,
    "5": 8.4,
    "6": 10.1,
    "7": 10.8,
    "8": 9.8,
    "9": 8.6,
    "10": 6.8,
    "11/12": 6.4
}

Average Speed Normalized to Horse 7:
{
    "2/3": 61,
    "4": 60,
    "5": 78,
    "6": 93,
    "7": 100,
    "8": 91,
    "9": 80,
    "10": 63,
    "11/12": 60
}

Expected rolls per space moved:
{
    "2/3": 9.8,
    "4": 9.9,
    "5": 7.6,
    "6": 6.4,
    "7": 6.0,
    "8": 6.5,
    "9": 7.5,
    "10": 9.4,
    "11/12": 10.0
}
```