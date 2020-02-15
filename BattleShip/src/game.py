import itertools
from typing import Type
from . import game_config, player
from .humanplayer import HumanPlayer
from .ai_player import AIPlayer
from .board import Board
from .random_ai import RandomAI

class Game(object):

    def __init__(self, game_config_file: str, num_players: int = 2) -> None:
        super().__init__()
        self.game_config = game_config.GameConfig(game_config_file)
        self.players = []
        self.player_turn = 0
        self.setup_players(num_players)
        self.board = player.board


    def setup_players(self, num_players: int) -> None:
        for player_num in range(1, num_players + 1):
            player_type = self.pick_player_type()
            self.players.append(player_type(player_num, self.game_config, self.players))

    def pick_player_type(self) -> Type:
        possible_players = {
            'human': HumanPlayer, 'randomai': RandomAI
        }

        while True:
            picked_type = input(f'Pick one of {list(possible_players)} for your type: ').strip().lower()
            for name, type in possible_players.items():
                if name.startswith(picked_type):
                    return type
                else:
                    print(f'{picked_type} is not one of {list(possible_players)}')

    def play(self) -> None:
        active_player = self.players[0]
        for active_player in itertools.cycle(self.players):
            self.do_current_players_turn(active_player)
            if self.game_is_over():
                break
        print(f'{active_player} won the game!')

    def do_current_players_turn(self, cur_player: player.Player) -> None:
        self.display_gamestate(cur_player)
        while True:
            move = cur_player.get_move(self.board)
            move.make()
            if move.ends_turn():
                break

    @property
    def num_players(self) -> int:
        return len(self.players)

    def get_active_player(self) -> player.Player:
        return self.players[self.player_turn]

    def game_is_over(self) -> bool:
        return any(player_.all_ships_sunk() for player_ in self.players)

    def display_gamestate(self, cur_player: player.Player) -> None:
        cur_player.display_scanning_boards()
        cur_player.display_firing_board()
