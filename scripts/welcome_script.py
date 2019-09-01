from configs.player_configs.alice import AliceConfig  # Конфиг первого игрока
from configs.player_configs.bob import BobConfig  # Конфиг второго игрока
from configs.referee_configs.config_3x3 import RefereeConfig3x3 as referee_config  # Модель обычного поля 3x3
from game import Game  # Класс управления игроками и полем
from referee import Referee  # Класс, унифицирующий модель поля для обоих игроков

from players.reinforcement_learning_player import ReinforcementLearningPlayer  # Класс самообучающегося игрока
from players.human_player import HumanPlayer  # Чтобы человек смог поиграть против игрока


referee = Referee(config=referee_config)
Alice = ReinforcementLearningPlayer(referee=referee, config=AliceConfig)  # Первый игрок
Bob = ReinforcementLearningPlayer(referee=referee, config=BobConfig)  # Второй игрок

game = Game(referee=referee)

# Training block
Alice.mode = 'train'  # Следующая игра для Алисы будет тренировочной
Bob.mode = 'train'  # Следующая игра для Боба будет тренировочной
# Будет совершено 10^5 игр, со случайной начальной позицией, где за 'x' будет играть Алиса, а за 'o' - Боб
game.several_games(games_number=10 ** 5, start_position='random', first_player=Alice, second_player=Bob)

# Try to play against human
Alice.mode = 'play'  # Следующая игра для Алисы будет по-настоящему (не тренировка)
human = HumanPlayer(referee=referee)  # Игрок, которым будет упарвлять человек
# Будет совершено 5 игры, на изначально пустом поле, где за 'x' будет играть Алиса, а за 'o' - человек
game.several_games(games_number=5, start_position='clear', first_player=Alice, second_player=human)

Alice.save_weight_db()  # Алиса всё, чему она научилась сохраняет
