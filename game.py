import chess
import json

def save(game: Game, filename: str):
    game_data = game.get_dict()
    json_string = json.dump(game_data)
    file = open(filename, "w")
    file.write(json_string)
    file.close()

def load(game: Game, filename: str):
    file = open(filename, "r")
    json_string = file.read()
    game_data = json.parse(json_string)
    print(game_data)
    pass

game = Game()
game.play_game()
