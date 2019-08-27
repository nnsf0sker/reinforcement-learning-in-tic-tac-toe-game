import time
start = time.time()
from configs.player_configs.alice import AliceConfig
from configs.player_configs.bob import BobConfig
from configs.referee_configs.config_3x3 import RefereeConfig3x3 as referee_config
from game import Game
from referee import Referee

from players.reinforcement_learning_player import ReinforcementLearningPlayer
from players.human_player import HumanPlayer


referee = Referee(config=referee_config)
Alice = ReinforcementLearningPlayer(referee=referee, config=AliceConfig)
Bob = ReinforcementLearningPlayer(referee=referee, config=BobConfig)

game = Game(referee=referee)

# Training block
Alice.mode = 'train'
Bob.mode = 'train'
game.several_games(
    games_number=10**5,
    start_position='random',
    first_player=Alice,
    second_player=Bob)
print(time.time() - start)

# Try to play against human
# Alice.mode = 'play'
# human = HumanPlayer(referee=referee)
# game.several_games(
#     games_number=5,
#     start_position='clear',
#     first_player=Alice,
#     second_player=human
# )

Alice.save_weight_db()
