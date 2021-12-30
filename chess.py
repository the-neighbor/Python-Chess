import numpy
import piece_moves
import copy
import json
import io

validate_coordinates = piece_moves.validate_coordinates
cast_ray = piece_moves.cast_ray

#POSITION CLASS STORES A GIVEN POSITION ON THE CHESS BOARD
#WHEN INITIALIZED, IT TAKES IN A POSITION AS EITHER A PAIR OF COORDINATES
#OR AS A STRING CONTAINING A BOARD POSITION IN CHESS NOTATION
#AND IT THEN CONVERTS THIS INTO AN OBJECT WHICH CONTAINS BOTH
#THE CHESS NOTATION OF THE POSITION AND A 2D VECTOR WITH THE POSITION COORDINATES
#THIS MAKES IT EASIER TO HANDLE CONVERSIONS BETWEEN THE TWO
#AND FACILITATES THE USE OF VECTOR OPERATIONS LIKE ADDITION AND MULTIPLICATION
#TO EASILY CALCULATE NEW BOARD POSITIONS FROM A STARTING POSITION AND A MOVEMENT VECTOR
class Position:
    def __init__(self, position):
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        self.chess_notation = ""
        self.vector = numpy.array([-1,-1])
        if isinstance(position, str):
            #POSITION CAN BE PROVIDED AS A STRING LIKE "A2"
            position = position.upper()
            if position[0] in XVALUES and position[1] in YVALUES:
                self.chess_notation = position
                x = XVALUES.index(position[0])
                y = YVALUES.index(position[1])
                self.vector = numpy.array([x,y])
        elif isinstance(position, (numpy.ndarray, list)):
            #POSITION CAN ALSO BE PROVIDED AS A VECTOR(NUMPY ARRAY)
            if position[0] in range(0,8) and position[1] in range(0,8):
                self.vector = position.copy()
                chess_notation = ""
                chess_notation += XVALUES[self.vector[0]]
                chess_notation += YVALUES[self.vector[1]]
                self.chess_notation = chess_notation
    def print(self):
        #PRINT BOTH FORMS OF THE NOTATION TO STDOUT
        print(self.chess_notation)
        #print(self.vector)
    def add_move(self, movement_vector):
        #USE THE VECTOR ADDITION PROVIDED BY NUMPY TO RETURN THE POSITION
        #YOU WOULD ARRIVE AT IF YOU FOLLOWED SOME MOVEMENT VECTOR FROM THIS ONE.
        if not isinstance(movement_vector, numpy.ndarray):
            movement_vector = numpy.array(movement_vector)
        return Position(self.vector + movement_vector)


#PIECE CLASS STORES THE ATTRIBUTES OF A PARTICULAR PIECE. IT IS RESPONSIBLE FOR
#STORING WHAT KIND OF CHESS PIECE IT IS, AS WELL AS THE COLOR, AND USING THAT
#TO DETERMINE WHAT POTENTIAL MOVES CAN BE MADE FROM A GIVEN BOARD POSITION.
#IN OUR CASE, WE CURRENTLY USE THE PIECE CLASS TO STORE AND PRINT THE ASCII
#REPRESENTATION THAT CORROSPONDS TO THAT PIECE
class Piece:
    ascii = {
        'PAWN':"P",
        'ROOK':"R",
        'KNIGHT':"N",
        'BISHOP':"B",
        'KING':"K",
        'QUEEN':"Q"
    }
    def __init__(self, board, color="WHITE", piece="PAWN"):
        self.board = board
        self.color = color
        self.piece = piece
        self.move_counter = 0
        self.capture_counter = 0
        self.piece_moves = piece_moves.move_methods[self.piece]
    def piece_ascii(self):
        piece_str = ""
        piece_str += self.color[0]
        piece_str += self.get_ascii()
        return piece_str
    def get_ascii(self):
        return self.ascii[self.piece]
    def eval_moves(self, position):
        #REFACTOR THE EVAL
        moves = self.piece_moves(self, self.board, position)
        #print(moves)
        return_moves = {"moves":[], "captures":[]}
        for m in moves["moves"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A MOVE VECTOR TO THAT COORDINATE
            if self.color == "BLACK" and self.piece == "PAWN":
                m *= -1
            new_position = position.add_move(m)
            if validate_coordinates(new_position):
                return_moves["moves"].append(new_position)
        for c in moves["captures"]:
            #CREATE A COPY OF THE ORIGINAL COORDINATES
            #ADD THE X/Y VALUES OF A CAPTURE VECTOR TO THAT COORDINATE
            if self.color == "BLACK" and self.piece == "PAWN":
                c *= -1
            new_position = position.add_move(c)
            #print (new_position.chess_notation)
            if validate_coordinates(new_position):
                return_moves["captures"].append(new_position)
        return return_moves

class Spot:
    def __init__(self):
        self.state = "EMPTY"
        self.occupant = None
    def occupy(self, new_occupant):
        #OCCUPY SPOT WITH NEW PIECE
        self.occupant = new_occupant
        self.state = "FULL"
    def empty(self):
        #CLEAR SPOT
        self.occupant = None
        self.state = "EMPTY"
    def get_ascii(self):
        if self.state == "EMPTY":
            return "__"
        elif self.state == "FULL" and isinstance(self.occupant, Piece):
            return self.occupant.piece_ascii()
        else:
            return "??"

class Board:
    #THE CLASS FOR THE BOARD. RESPONSIBLE FOR STORING THE STATE OF THE GAME
    def __init__(self):
        #INITIALIZES AN INSTANCE OF THE BOARD CLASS BY INSTANTIATING AND CREATING
        #A 2D MATRIX OF SPOT CLASS INSTANCES
        self.state = [[Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()],
             [Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot(),Spot()]]
    def set_spot(self,x,y,value=None):
        #SETS A SPOT ON THE BOARD TO A PARTICULAR VALUE USING X-Y COORDINATES
        if type(value) is Piece:
            self.state[y][x].state = "FULL"
            self.state[y][x].occupant = value
        else:
            self.state[y][x].state = "EMPTY"
    def get_spot(self, x, y):
        return self.state[y][x]
    def setup_board(self):
        #PLACES ALL THE PIECES IN THEIR STARTING POSITION
        #FIRST PLACE THE WHITE PIECES
        self.set_spot(0,0,Piece(self, "WHITE","ROOK"))
        self.set_spot(7,0,Piece(self, "WHITE","ROOK"))
        self.set_spot(1,0,Piece(self, "WHITE","KNIGHT"))
        self.set_spot(6,0,Piece(self, "WHITE","KNIGHT"))
        self.set_spot(2,0,Piece(self, "WHITE","BISHOP"))
        self.set_spot(5,0,Piece(self, "WHITE","BISHOP"))
        self.set_spot(3,0,Piece(self, "WHITE","KING"))
        self.set_spot(4,0,Piece(self, "WHITE","QUEEN"))
        for i in range(0,8):
            self.set_spot(i,1,Piece(self, "WHITE","PAWN"))
        self.set_spot(0,7,Piece(self, "BLACK","ROOK"))
        self.set_spot(7,7,Piece(self, "BLACK","ROOK"))
        self.set_spot(1,7,Piece(self, "BLACK","KNIGHT"))
        self.set_spot(6,7,Piece(self, "BLACK","KNIGHT"))
        self.set_spot(2,7,Piece(self, "BLACK","BISHOP"))
        self.set_spot(5,7,Piece(self, "BLACK","BISHOP"))
        self.set_spot(3,7,Piece(self, "BLACK","KING"))
        self.set_spot(4,7,Piece(self, "BLACK","QUEEN"))
        for i in range(0,8):
            self.set_spot(i,6,Piece(self, "BLACK","PAWN"))
        return self
    def print_board(self):
        #PRINTS THE BOARD TO THE TERMINAL USING ASCII CHARACTERS
        board_str = "  "
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        index = 0
        for c in XVALUES:
            board_str += (c)
            board_str += "  "
        board_str += "\n"
        for y in self.state:
            board_str += (YVALUES[index])
            board_str += " "
            for x in y:
                board_str += x.get_ascii()
                board_str += " "
            board_str += '\n'
            index += 1
        board_str += '\n'
        print(board_str)
    def get_position(self, position):
        #RETURNS THE SPOT ON THE BOARD SPECIFIED BY A GIVEN POSITION IN CHESS NOTATION
        coordinate = self.translate_position(position)
        return self.get_spot(coordinate[0], coordinate[1])
    def get_spot_by_position(self, position):
        #RETURNS THE SPOT ON THE BOARD SPECIFIED BY A POSITION OBJECT
        return self.get_spot(position.vector[0], position.vector[1])
    def translate_position(self, position):
        #TAKES A GIVEN CHESS POSITION IN THE FORMAT "E7" AND CONVERTS IT
        #TO XY COORDINATES THAT CAN BE USED TO ACCESS THAT SPOT
        XVALUES = list("ABCDEFGH")
        YVALUES = list("87654321")
        x = XVALUES.index(position[0])
        y = YVALUES.index(position[1])
        return [x,y]
    def move(self, start, end):
        #TAKES TWO CHESS POSITIONS AND MOVES THE PIECE AT 'START' TO OCCUPY 'END'
        #THIS DOES NOT HANDLE VALIDATION BY CHECKING WHETHER OR NOT THE MOVE IS LEGAL.
        #THAT WILL BE CHECKED WITH ANOTHER FUNCTION BEFORE THIS ONE IS CALLED.
        start_spot = self.get_position(start)
        end_spot = self.get_position(end)
        end_spot.occupy(start_spot.occupant)
        end_spot.occupant.move_counter += 1
        start_spot.empty()
        pass
    def look_ahead(self, start, end):
        board_state = copy.deepcopy(self)
        board_state.move(start, end)
        return board_state
    def capture(self, start, end):
        #MOVES, BUT ALSO ADDS THE CAPTURED PIECE TO A LIST
        self.move(start, end)
        end_spot = self.get_position(end)
        end_spot.occupant.capture_counter += 1
    def check(self, color):
        #EVAL THE CURRENT STATE OF THE BOARD TO DETERMINE IF EITHER PLAYER HAS CHECK
        #IF NOT, RETURN FALSE, IF SO, RETURN THE PLAYER WHO HAS THE OTHER PLAYER IN CHECK
        check = False
        potential_captures = self.possible_captures(color)
        for c in potential_captures:
            #print(c)
            spot = self.get_spot_by_position(c)
            if spot and spot.state == "FULL" :
                if spot.occupant.color != color and spot.occupant.piece == "KING":
                    check = True
        return check
    def checkmate(self, color):
        #EVAL THE CURRENT STATE OF THE BOARD TO DETERMINE IF EITHER PLAYER HAS CHECKMATE
        #IF NOT, RETURN FALSE, IF SO, RETURN THE PLAYER WHO HAS CHECKMATE/THE WINNER
        opposing_color = "WHITE"
        if color == "WHITE":
            opposing_color = "BLACK"
        for move in self.all_valid_moves(opposing_color):
            future = self.look_ahead(move[0].chess_notation, move[1].chess_notation)
            #future.print_board()
            if not (future.check(color)):
                #print(move[0].chess_notation, move[1].chess_notation)
                return False
        return True
    def possible_selections(self, color):
        #RETURN AN ARRAY OF POSITIONS THAT ARE OCCUPIED BY A GIVEN SIDE
        possibilities = []
        for y in range(0,8):
            for x in range(0,8):
                current_spot = self.get_spot_by_position(Position([x,y]))
                if current_spot and current_spot.state == "FULL":
                    if current_spot.occupant.color == color:
                        possibilities.append(Position([x,y]))
        return possibilities
    def puts_self_in_check(self, color, start, end):
        opposing_color = "WHITE"
        if color == "WHITE":
            opposing_color = "BLACK"
        future = self.look_ahead(start, end)
        if future.check(opposing_color):
            return True
        return False
    def possible_moves(self, position):
        #PASSED IN A POSITION AS A PARAMETER, RETURN THE LIST OF POSSIBLE MOVES
        #THAT CAN BE MADE WITH THE PIECE ON THAT POSITION
        spot = self.get_spot_by_position(position)
        if spot and spot.state == "FULL":
            moves = spot.occupant.eval_moves(position)
            return moves
    def valid_moves(self, position):
        #RETURNS A DICTIONARY LIKE POSSIBLE MOVES BUT WITH THE MOVES AND CAPTURES PRE VALIDATED
        moves = self.possible_moves(position)
        valids = {'moves':[], 'captures':[]}
        spot = self.get_spot_by_position(position)
        piece = spot.occupant
        for m in moves['moves']:
            if self.validate_move(piece.color, position.chess_notation, m.chess_notation):
                valids['moves'].append(m)
        for c in moves['captures']:
            if self.validate_capture(piece.color, position.chess_notation, c.chess_notation):
                valids['captures'].append(c)
        return valids
    def spots_threatened(self, color):
        #GET ALL THE SPOTS CURRENTLY ON THE BOARD THAT ARE THREATENED BY A GIVEN COLOR
        movable_pieces = self.possible_selections(color)
        possibilities = []
        for p in movable_pieces:
            current_piece_moves = self.possible_moves(p)
            for m in current_piece_moves['captures']:
                spot = self.get_spot_by_position(m)
                if spot.state == "EMPTY" or spot.occupant.color != color:
                    possibilities.append(m)
        return possibilities
    def spots_occupied(self, color):
        return self.possible_selections(color)
    def spots_controlled(self, color):
        return [*self.spots_occupied(color),*self.spots_threatened(color)]
    def possible_captures(self, color):
        #get possible captures
        movable_pieces = self.possible_selections(color)
        possibilities = []
        for p in movable_pieces:
            current_piece_moves = self.possible_moves(p)
            for m in current_piece_moves['captures']:
                if self.validate_capture(color,p.chess_notation,m.chess_notation):
                    possibilities.append(m)
        return possibilities
    def all_possible_moves(self, color):
        #MAY BE REDUNDANT WITH THE VALID MOVES FUNCTIONS
        possibilities = []
        for piece_position in self.possible_selections(color):
            for target_position in self.possible_moves(piece_position):
                possibilities.append([piece_position, target_position])
        return possibilities
    def all_possible_captures(self, color):
        #MAY BE REDUNDANT NOW WITH THE VALID MOVES FUNCTION
        possibilities = []
        for piece_position in self.possible_selections(color):
            for target_position in self.possible_captures(piece_position):
                possibilities.append([piece_position, target_position])
        return possibilities
    def all_valid_moves(self, color):
        all_valids = []
        for piece_position in self.possible_selections(color):
            current_valids = self.valid_moves(piece_position)
            for target_position in current_valids['moves']:
                all_valids.append([piece_position, target_position])
            for target_position in current_valids['captures']:
                all_valids.append([piece_position, target_position])
        return all_valids
    def valid_position(self, position):
        return validate_coordinates(position)
    def validate_move(self, side, origin, destination):
        #CHECK THAT A MOVE IS VALID BY MAKING SURE THAT THE FOLLOWING CONDITIONS ARE MET:
        #THAT THE ORIGIN AND DESTINATION ARE BOTH VALID BOARD POSITIONS
        #THAT THE ORIGIN IS OCCUPIED BY A PIECE WHOSE COLOR == SIDE
        #THAT THE DESTINATION IS EMPTY
        origin = Position(origin)
        destination = Position(destination)
        if side and self.valid_position(origin) and self.valid_position(destination):
            origin_spot = self.get_spot_by_position(origin)
            destination_spot = self.get_spot_by_position(destination)
            if origin_spot.state == "FULL" and \
               origin_spot.occupant.color == side and \
               destination_spot.state == "EMPTY":
                if any(destination.chess_notation == d.chess_notation for d in self.possible_moves(origin)["moves"]):
                    return True
        return False
    def validate_capture(self, side, origin, destination):
        #CHECK THAT A CAPTURE IS VALID BY MAKING SURE THAT THE DESTINATION IS VALID AND OCCUPIED BY A PIECE OF THE OPPOSITE COLOR
        origin = Position(origin)
        destination = Position(destination)
        if side and self.valid_position(origin) and self.valid_position(destination):
            origin_spot = self.get_spot_by_position(origin)
            destination_spot = self.get_spot_by_position(destination)
            if origin_spot.state == "FULL" and \
               origin_spot.occupant.color == side and \
               destination_spot.state == "FULL" and \
               destination_spot.occupant.color != side:
                if any(destination.chess_notation == d.chess_notation for d in self.possible_moves(origin)["captures"]):
                    return True
        return False
    def get_list(self) -> list:
        board_list = []
        for i, line in enumerate(self.state):
            current_line = []
            for j, element in enumerate(line):
                current_line.append(element.get_ascii())
            board_list.append(current_line)
        return board_list

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.game_mode = ""
        self.player_color = ""
        self.welcome_message_path = "assets/title-screen.txt"
    def print_commands(self, commands: dict):
        #PRINT ALL COMMANDS IN A DICTIONARY PASSED IN AS A PARAMETER
        string = ""
        for index, (command, data) in enumerate(commands.items()):
            string += f"{command}"
            for p in data['params']:
                string += f" {p}"
            string += f"\n\t{data['description']}\n"
        print(string)
    def menu(self, commands: dict):
        #DISPLAYS A LIST OF COMMANDS, GETS A STRING REPRESENTING THE COMMAND AND ARGUMENTS
        #THEN USES THE COMMAND TO CALL A FUNCTION

        complete = False
        while not complete:
            print("Please enter one of the following commands: \n")
            self.print_commands(commands)
            command_string = input()
            command_array = command_string.split(" ")
            command = command_array[0]
            params = command_array[slice(1, len(command_array))]
            if command in commands and len(params) == len(commands[command]['params']):
                commands[command]['function'](*params)
                complete = True
    def start_game(self):
        welcome_message = ""
        with open(self.welcome_message_path, 'r') as file:
            welcome_message = file.read()
        print(welcome_message)
        print("What would you like to do?\n\n")
        commands = {
            "PvP":{
                'params':[],
                'description':"Starts a new game for two players",
                'function':self.play_game
            },
            "PvCPU":{
                'params':["<color>"],
                'description':"Starts a new game versus the CPU as <color>(BLACK, WHITE)",
                'function':self.play_vs_ai
            },
            "CPUvCPU":{
                'params':[],
                'description':"Starts a game where the CPU/AI plays against itself for your enjoyment!",
                'function':self.ai_vs_ai
            },
            "LOAD": {
                'params':["<filename>"],
                'description':"Loads a saved game from a file in the game directory called <filename>",
                'function':self.load
            }
        }
        self.menu(commands)
    def print_result(self, side: str, command_array: list):
        #PRINTS THE RESULT OF A PARTICULAR COMMAND
        recap_string = ""
        if command_array[0] in ["MOVE","CAPTURE"]:
            start_position = command_array[1]
            end_position = command_array[2]
            recap_string += f"{side} MOVES THEIR PIECE ON {start_position} TO "
            if command_array[0] == "MOVE":
                recap_string += end_position
            else:
                recap_string += f"CAPTURE {end_position}"
        print(f"{recap_string}\n")
        if self.board.check("BLACK"):
            print("BLACK HAS WHITE IN CHECK\n")
        elif self.board.check("WHITE"):
            print("WHITE HAS BLACK IN CHECK\n")
    def execute_command(self, side: str, command: str):
        #TAKES IN A COMMAND LINE STRING AND
        command_array = command.split()
        turn_complete = False
        if command_array[0] == "MOVE":
            #COMMAND TO HANDLE MOVING A PIECE FROM ONE TILE TO ANOTHER
            if self.board.validate_move(side, command_array[1], command_array[2]) \
            and not self.board.puts_self_in_check(side, command_array[1], command_array[2]):
                self.board.move(command_array[1], command_array[2])
                turn_complete = True
            else:
                print("Error")
        if command_array[0] == "CAPTURE":
            #COMMAND TO HANDLE CAPTURING ONE PIECE BY MOVING YOUR OWN PIECE.
            #SIMILAR VALIDATION TO THE MOVE COMMAND, JUST ALSO HAVE TO CHECK THAT THE TILE WE WANT
            #TO CAPTURE
            if self.board.validate_capture(side, command_array[1], command_array[2]) \
            and not self.board.puts_self_in_check(side, command_array[1], command_array[2]):
                self.board.capture(command_array[1], command_array[2])
                turn_complete = True
            else:
                print ("Error")
        if command_array[0] == "PIECES":
            for i in self.board.possible_selections(side):
                print (i.chess_notation)
        if command_array[0] == "SAVE":
            self.save(command_array[1])
        if command_array[0] == "LOAD":
            self.load(command_array[1])
        if turn_complete:
            self.print_result(side, command_array)
        return turn_complete
    def pvcpu_turn(self, color):
        if self.turn % 2:
            #ON ODD TURNS, BLACK GOES
            if color == "BLACK":
                self.take_turn("BLACK")
            else:
                self.execute_command("BLACK", self.ai("BLACK"))
        else:
            #ON EVEN TURNS, WHITE GOES
            if color == "WHITE":
                self.take_turn("WHITE")
            else:
                self.execute_command("WHITE", self.ai("WHITE"))
    def pvp_turn(self):
        if self.turn % 2:
            #ON ODD TURNS, BLACK GOES
            self.take_turn("BLACK")
        else:
            #ON EVEN TURNS, WHITE GOES
            self.take_turn("WHITE")
    def game_loop(self):
        while not (self.board.checkmate("BLACK") or self.board.checkmate("WHITE")):
            #TAKE THE TURN OF EACH PLAYER
            self.board.print_board()
            if self.game_mode == "PVCPU" or self.game_mode == "CPUVCPU":
                self.pvcpu_turn(self.player_color)
            elif self.game_mode == "PVP":
                self.pvp_turn()
            self.turn += 1
        self.win_message()
    def ai_vs_ai(self):
        self.board.setup_board()
        self.game_mode = "CPUVCPU"
        #PRINT THE STATE OF THE CHESS BOARD
        #SET A COUNTER FOR THE TURNS
        self.turn = 0
        #UNTIL WE REACH CHECKMATE
        self.game_loop()
    def play_vs_ai(self, color):
        #PLAY THE GAME VS THE AI
        #SETUP BOARD
        self.board.setup_board()
        self.game_mode = "PVCPU"
        self.player_color = color 
        #PRINT THE STATE OF THE CHESS BOARD
        #SET A COUNTER FOR THE TURNS
        self.turn = 0
        #UNTIL WE REACH CHECKMATE
        self.game_loop()
    def play_game(self):
        #FUNCTION TO INITIATE AND CARRY A GAME TO COMPLETION
        #SETUP THE CHESS BOARD WITH THE STARTING POSITION OF ALL THE PIECES
        self.board.setup_board()
        #PRINT THE STATE OF THE CHESS BOARD
        self.board.print_board()
        self.game_mode = "PVP"
        #SET A COUNTER FOR THE TURNS
        self.turn = 0
        #UNTIL WE REACH CHECKMATE
        self.game_loop()
    def win_message(self):
        for color in ["BLACK", "WHITE"]:
            if self.board.checkmate(color):
                winner = color
        message = f"CONGRATULATIONS {winner}, YOU WIN!\nFINAL SCORE: {self.score(self.board, winner)}"
        print(message)
    def take_turn(self, side):
    #TAKES IN A BOARD WITH THE CURRENT STATE OF A CHESS GAME
    #AND THE SIDE TO GO AS A BOOL (TRUE = BLACK, FALSE = WHITE)
    #GETS COMMAND (EX. MOVE E7 E5) USING GET_STRING() OR GET_INPUT()
    #USES SPLIT() TO BREAK THE COMMAND INTO THE NAME OF THE BOARD METHOD
    #TO BE CALLED AND THE ARGUMENTS/PARAMETERS FOR THAT FUNCTION CALL
        #BOOL SO WE KNOW WHEN THE TURN IS OVER
        turn_complete = False
        #UNTIL THE TURN IS COMPLETE, PROMPT FOR INPUT
        while not turn_complete:
            #PROMPT USER FOR INPUT
            command = input('%s: WHAT IS YOUR COMMAND?\n' % side)
            turn_complete = self.execute_command(side, command)
    def get_dict(self) -> dict:
        game_dict = {}
        game_dict['board'] = self.board.get_list()
        game_dict['turn'] = self.turn
        game_dict['mode'] = self.game_mode
        game_dict['player_color'] = self.player_color
        return game_dict
    def shorthand_to_piece(self, shorthand: str) -> Piece:
        #TRANSLATE FROM THE ASCII TO A PIECE
        piece_name = ""
        team_name = ""
        return_piece = None

        if shorthand[0] == "W":
            team_name = "WHITE"
        elif shorthand[0] == "B":
            team_name = "BLACK"
        for index, (piece, letter) in enumerate(pieces_ascii.items()):
            if shorthand[1] == letter:
                piece_name = piece
                return_piece = (Piece(self.board, team_name, piece_name))
        return return_piece
    def load_board_from_data(self, board_data: list):
        #USE THE BOARD STATE AS DESCRIBED IN THE SAVE FILE
        for y, line in enumerate(board_data):
            for x, spot in enumerate(line):
                self.board.set_spot(x,y,self.shorthand_to_piece(spot))
        pass
    def save(self, filename: str):
        game_data = self.get_dict()
        file = open(filename, "w")
        json.dump(game_data, file)
        file.close()
    def load(self, filename: str):
        file = open(filename, "r")
        game_data = json.load(file)
        self.turn = game_data['turn']
        self.game_mode = game_data['mode']
        self.player_color = game_data['player_color']
        self.load_board_from_data(game_data['board'])
        self.board.print_board()
        self.game_loop()
    def score(self, board, color: str):
        player_score = 0
        player_score += len(board.spots_occupied(color))
        player_score += len(board.spots_threatened(color)) * 4
        if board.check(color):
            player_score *= 2
        if board.checkmate(color):
            player_score *= 10
        return player_score

    def ai(self, color: str) -> str:
        #MAKES A DECISION FOR THE TURN BASED ON THE COLOR AND THE score
        highest_score = 0
        highest_command = ""
        for piece in self.board.possible_selections(color):
            moves = self.board.valid_moves(piece)
            for move in moves['moves']:
                hypothetical = self.board.look_ahead(piece.chess_notation, move.chess_notation)
                current_score = self.score(hypothetical, color)
                opposing_color = "WHITE"
                if color == "WHITE":
                    opposing_color = "BLACK"
                if current_score >= highest_score and not hypothetical.check(opposing_color):
                    highest_score = current_score
                    highest_command = "MOVE " + piece.chess_notation + " " + move.chess_notation
            for capture in moves['captures']:
                hypothetical = self.board.look_ahead(piece.chess_notation, capture.chess_notation)
                current_score = self.score(hypothetical, color)
                opposing_color = "WHITE"
                if color == "WHITE":
                    opposing_color = "BLACK"
                if current_score >= highest_score and not hypothetical.check(opposing_color):
                    highest_score = current_score
                    highest_command = "CAPTURE " + piece.chess_notation + " " + capture.chess_notation
        return highest_command

pieces_ascii = {
    'PAWN':"P",
    'ROOK':"R",
    'KNIGHT':"N",
    'BISHOP':"B",
    'KING':"K",
    'QUEEN':"Q"
    }
teams_ascii = {
    'WHITE':"W",
    'BLACK':"B"
}

game = Game()
game.start_game()

