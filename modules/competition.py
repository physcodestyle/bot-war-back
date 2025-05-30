from modules.bot import Bot
from modules.game import Game
from modules.bot_factory import BotFactory


class Competition:
    def __init__(self, game_count: int, map_size: int):
        self.game_count = game_count
        self.map_size = map_size
        self.wins = []


    def play_game(self, bot_list: list[str]) -> bool:
        if self.game_count == 0:
            return False
        
        self._print_delimiter()
        self._print_state(f'There are {self.game_count} games remain...')
        self._print_delimiter()

        game = self._create_game(map_size=self.map_size, bot_list=bot_list)
        
        round_counter = 1
        while len(game.play_round()) > 1:
            self._print_state(f'Round #{round_counter}')
        
        self._print_delimiter()
        report = game.get_report()
        if len(report) > 0:
            self.wins.append(report[0])
            self._print_state(f'Winner: {report[0]}')
        else:
            self.wins.append('')
            self._print_state(f'Drawn game')
        self._print_delimiter()

        self.game_count -= 1
        return True


    def get_report(self) -> dict:
        win_dict = {}
        for win in self.wins:
            if win == '':
                if not '---' in dict.keys(win_dict):
                    win_dict['---'] = 1
                else: 
                    win_dict['---'] += 1
            else:
                if not win in dict.keys(win_dict):
                    win_dict[win] = 1
                else: 
                    win_dict[win] += 1
        return win_dict


    def _create_game(map_size: int, bot_list: list[str]) -> Game:
        bots = BotFactory.build(bot_list=bot_list)
        return Game(map_size=map_size, bots=bots)


    def _print_state(report_text):
        print(report_text)


    def _print_delimiter():
        print('------')