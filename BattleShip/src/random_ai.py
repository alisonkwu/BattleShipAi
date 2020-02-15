from typing import Dict, List, Tuple
from . import game_config, ship, board, orientation, move
from .ai_player import AIPlayer
from .player import Player
import random

class RandomAI(AIPlayer):
    opponents: List["Player"]
    ships: Dict[str, ship.Ship]

    def __init__(self, player_num: int, config: game_config.GameConfig, other_players: List["Player"]) -> None:
        super().__init__(player_num, config, other_players)
        self.possible_locations = self.get_coordinates()

    def init_name(self, player_num: int, other_players: List["Player"]) -> None:
        self.name = f'Random AI {player_num}'

    def get_coordinates(self) -> List[Tuple[int, int]] :
        possible_coords = []
        for row in range(self.board.num_rows):
            for col in range(self.board.num_cols):
                possible_coords.append((row, col))
        return possible_coords


    def get_move(self, the_board: "board.Board") -> move.Move:
        #possible_coordinates = the_board.get_coordinates()
        coords = random.choice(self.possible_locations)
        self.possible_locations.remove(coords)
        firing_location = move.Move.from_ai(self, coords)
        return firing_location



